#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# colony.py (0.2.1)
#
# Developed in 2018 by Travis Kessler <travis.j.kessler@gmail.com>
#

# Stdlib imports
from copy import deepcopy
from multiprocessing import Pool

# 3rd party, open src. imports
from numpy.random import choice

# ApisOptimizer imports
from apisoptimizer import Bee
from apisoptimizer import Parameter


class Colony:

    def __init__(self, num_employers, objective_fn, obj_fn_args=None,
                 num_processes=1):
        '''
        Colony object: optimizes parameters for supplied objective function

        Args:
            num_employers (int): number of employer bees (and initial food)
            objective_fn (callable): user supplied function to determine
                                     fitness
            obj_fn_args (any): any additional arguments for user's objective
                               function
            num_processes (int): number of concurrent processes for bee eval
        '''

        if not callable(objective_fn):
            raise ValueError('Supplied objective function not callable!')
        self.__obj_fn = objective_fn
        self.__obj_fn_args = obj_fn_args
        self.__num_employers = num_employers
        self.__params = []
        self.__bees = []
        self.__num_processes = num_processes
        self.__best_fitness = 0
        self.__best_params = None

    @property
    def best_fitness(self):
        '''
        Fitness score of best performing bee so far
        '''

        return self.__best_fitness

    @property
    def best_parameters(self):
        '''
        Parameters of best performing bee so far
        '''

        return self.__best_params

    def add_param(self, name, min_val, max_val):
        '''
        Add a parameter for the Colony to optimize

        Args:
            name (str): name of the parameter
            min_val (int or float): minimum value allowed
            max_val (int or float): maximum value allowed
        '''

        self.__params.append(Parameter(name, min_val, max_val))

    def initialize(self):
        '''
        Finds initial positions for employers, deploys onlookers to
        neighboring positions of employers with good fitness
        '''

        if len(self.__params) == 0:
            raise Exception(
                'Parameters must be added before bee positions are found'
            )

        if self.__num_processes > 1:
            emp_process_pool = Pool(processes=self.__num_processes)
            emp_results = []

        self.__bees = []

        # Generate employer bees
        for _ in range(self.__num_employers):

            param_dict = self.__create_param_dict()

            if self.__num_processes > 1:
                emp_results.append(emp_process_pool.apply_async(
                    self._start_process,
                    [param_dict, self.__obj_fn, self.__obj_fn_args]
                ))

            else:
                self.__bees.append(Bee(
                    param_dict,
                    self.__obj_fn(param_dict, self.__obj_fn_args),
                    len(self.__params) * self.__num_employers,
                    is_employer=True
                ))

        if self.__num_processes > 1:
            emp_process_pool.close()
            emp_process_pool.join()
            onl_process_pool = Pool(processes=self.__num_processes)
            onl_results = []
            for bee in emp_results:
                self.__bees.append(Bee(
                    bee.get()[0],
                    bee.get()[1],
                    len(self.__params) * self.__num_employers,
                    is_employer=True
                ))

        # Calculate probabilities of employer being chosen by onlookers
        employer_probabilities = self.__calc_bee_probs()

        # Generate onlooker bees
        onlookers = []
        for _ in range(self.__num_employers):

            chosen_employer = choice(self.__bees, p=employer_probabilities)
            neighbor_food = chosen_employer.mutate()

            if self.__num_processes > 1:
                onl_results.append(onl_process_pool.apply_async(
                    self._start_process,
                    [neighbor_food, self.__obj_fn, self.__obj_fn_args]
                ))

            else:
                onlookers.append(Bee(
                    neighbor_food,
                    self.__obj_fn(neighbor_food, self.__obj_fn_args),
                    len(self.__params) * self.__num_employers
                ))

        if self.__num_processes > 1:
            onl_process_pool.close()
            onl_process_pool.join()
            for bee in onl_results:
                onlookers.append(Bee(
                    bee.get()[0],
                    bee.get()[1],
                    len(self.__params) * self.__num_employers
                ))

        # Append onlookers to employers
        self.__bees.extend(onlookers)
        self.__determine_best_bee()

    def search(self):
        '''
        Run the colony's search/follow/abandon process, creates next
        generation of bees
        '''

        if len(self.__bees) == 0:
            raise Exception('Initial bee positions must be generated first')

        bee_probabilities = self.__calc_bee_probs()

        next_generation = []

        if self.__num_processes > 1:
            new_calculations = Pool(processes=self.__num_processes)
            new_employer_results = []
            new_onlooker_results = []
            new_position_results = []
            current_positions = []

        for bee in self.__bees:

            # If bee is marked for abandonment
            if bee.abandon:

                # If the bee is an employer, scout for new food source
                if bee.is_employer:

                    new_food = self.__create_param_dict()

                    if self.__num_processes > 1:
                        new_employer_results.append(
                            new_calculations.apply_async(
                                self._start_process,
                                [
                                    new_food,
                                    self.__obj_fn,
                                    self.__obj_fn_args
                                ]
                            )
                        )

                    else:
                        next_generation.append(Bee(
                            new_food,
                            self.__obj_fn(new_food, self.__obj_fn_args),
                            len(self.__params) * self.__num_employers,
                            is_employer=True
                        ))

                    continue

                # Otherwise, bee is an onlooker, choose a bee to work near
                else:
                    chosen_bee = choice(self.__bees, p=bee_probabilities)
                    neighbor_food = chosen_bee.mutate()

                    if self.__num_processes > 1:
                        new_onlooker_results.append(
                            new_calculations.apply_async(
                                self._start_process,
                                [
                                    neighbor_food,
                                    self.__obj_fn,
                                    self.__obj_fn_args
                                ]
                            )
                        )

                    else:
                        next_generation.append(Bee(
                            neighbor_food,
                            self.__obj_fn(
                                neighbor_food,
                                self.__obj_fn_args
                            ),
                            len(self.__params) * self.__num_employers
                        ))

                    continue

            # Not marked for abandonment, search for a food source near
            #   its current one
            neighbor_food = bee.mutate()

            if self.__num_processes > 1:
                current_positions.append(bee)
                new_position_results.append(new_calculations.apply_async(
                    self._start_process,
                    [neighbor_food, self.__obj_fn, self.__obj_fn_args]
                ))

            else:
                obj_fn_val = self.__obj_fn(
                    neighbor_food,
                    self.__obj_fn_args
                )

                # If new food is better than current food
                if bee.is_better_food(obj_fn_val):
                    if bee.is_employer:
                        bee = Bee(
                            neighbor_food,
                            obj_fn_val,
                            len(self.__params) * self.__num_employers,
                            is_employer=True
                        )
                    else:
                        bee = Bee(
                            neighbor_food,
                            obj_fn_val,
                            len(self.__params) * self.__num_employers
                        )

                # New food not better, check if food source is exhausted
                #   (if exhausted, mark for abandonment)
                else:
                    bee.check_abandonment()

                next_generation.append(bee)

        # If multiprocessing, finish processes, run comparisons, create
        #   next generation
        if self.__num_processes > 1:

            new_calculations.close()
            new_calculations.join()

            for bee in new_employer_results:
                next_generation.append(Bee(
                    bee.get()[0],
                    bee.get()[1],
                    len(self.__params) * self.__num_employers,
                    is_employer=True
                ))

            for bee in new_onlooker_results:
                next_generation.append(Bee(
                    bee.get()[0],
                    bee.get()[1],
                    len(self.__params) * self.__num_employers
                ))

            for idx, bee in enumerate(current_positions):
                if bee.is_better_food(new_position_results[idx].get()[1]):
                    if bee.is_employer:
                        next_generation.append(Bee(
                            new_position_results[idx].get()[0],
                            new_position_results[idx].get()[1],
                            len(self.__params) * self.__num_employers,
                            is_employer=True
                        ))
                    else:
                        next_generation.append(Bee(
                            new_position_results[idx].get()[0],
                            new_position_results[idx].get()[1],
                            len(self.__params) * self.__num_employers
                        ))

                else:
                    bee.check_abandonment()
                    next_generation.append(bee)

        # New bees = bees generated this iteration
        self.__bees = next_generation
        self.__determine_best_bee()

    @staticmethod
    def _start_process(param_dict, obj_fn, obj_fn_args):
        '''
        Static method: starts a process to evalutate parameters

        Args:
            param_dict (dictionary): dictionary of Parameter objects
            obj_fn (callable): objective function for evaluating Parameters
            obj_fn_args (any): any additional arguments for obj_fn

        Returns:
            tuple: (param_dict, value derived from objective function)
        '''

        obj_fn_val = obj_fn(param_dict, obj_fn_args)
        return (param_dict, obj_fn_val)

    def __determine_best_bee(self):
        '''
        Determines if any bee from the current generation has performed better
        than the best bee so far; updates object properties
        '''

        for bee in self.__bees:
            if bee.fitness_score > self.__best_fitness:
                self.__best_fitness = bee.fitness_score
                params = {}
                for param in bee.param_dict:
                    params[param] = bee.param_dict[param].value
                self.__best_params = params

    def __ave_bee_fitness(self):
        '''
        Returns average fitness of entire colony
        '''

        return sum(b.fitness_score for b in self.__bees) / len(self.__bees)

    def __calc_bee_probs(self):
        '''
        Determines probabilities that bees will be followed by onlookers

        Returns:
            list: list of probabilities (float), sum = 1
        '''

        bee_probabilities = []
        for bee in self.__bees:
            bee_probabilities.append(
                bee.fitness_score / sum(b.fitness_score for b in self.__bees)
            )
        return bee_probabilities

    def __create_param_dict(self):
        '''
        Generates a new parameter dictionary, random assignments for each
        Colony parameter

        Returns:
            dictionary: dictionary of parameter names and Parameter objects
        '''

        param_dict = {}
        for param in self.__params:
            param_dict[param.name] = deepcopy(param)
            param_dict[param.name].generate_rand_val()
        return param_dict
