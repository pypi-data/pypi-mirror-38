#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: Agent.py
# @time: 2018/7/29 14:35
# @Software: PyCharm

from abc import ABCMeta, abstractmethod
import numpy as np

npr = np.random
npa = np.array


class Individual(object):
    __metaclass__ = ABCMeta

    def __init__(self, chromosome=None, dim=2, bound=None, fitness_function=None, *,
                 min_fitness_value=-np.inf, init_method='random', transboundary_rules='bound', **kwargs):
        self._init_function(chromosome, dim, bound, fitness_function,
                            min_fitness_value=min_fitness_value, init_method=init_method,
                            transboundary_rules=transboundary_rules, **kwargs)

    @property
    def chromosome(self):
        return self._chromosome

    @chromosome.setter
    def chromosome(self, chromosome):
        self._chromosome = chromosome

    @property
    def fitness_value(self):
        return self._fitness_value

    @fitness_value.setter
    def fitness_value(self, fitness_value):
        self._fitness_value = fitness_value

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def fitness(self, *args, **kwargs):
        self._fitness_value = self.fitness_function(self._chromosome)
        return self._fitness_value

    def init_chromosome(self, init_method):
        """

        :param init_method:
        :return:
        """
        if init_method == 'rand' or init_method == 'random':
            self._chromosome = npr.random(self.dim) * (self.bound[:, 1] - self.bound[:, 0]).flatten() + self.bound[:,
                                                                                                        0].flatten()
        elif init_method == 'randn':
            self.chromosome = npr.randn(self.dim) * (self.bound[:, 1] - self.bound[:, 0]).flatten() + self.bound[:,
                                                                                                      0].flatten()
        elif init_method == 'randint':
            self.chromosome = npr.random(self.dim) * (self.bound[:, 1] - self.bound[:, 0]).flatten() + self.bound[:,
                                                                                                       0].flatten()
            self.chromosome = self.chromosome.astype(np.int)
        elif init_method == 'rand_permutation' or init_method == 'permutation':
            self.chromosome = npr.permutation(self.dim)
        else:
            raise NameError('init_method not found')

    def _init_function(self, chromosome=None, dim=2, bound=None, fitness_function=None, *,
                       min_fitness_value=-np.inf, init_method='random', transboundary_rules='bound', **kwargs):
        if chromosome is not None:
            self._chromosome = chromosome
            self.dim = len(chromosome)
            if bound is not None or []:
                bound = npa(bound)
                if len(bound.shape) == 1:
                    bound = np.repeat([bound], self.dim, axis=0)
                else:
                    m, n = bound.shape
                    if m == 1:
                        bound = np.repeat([bound], self.dim, axis=0)
                    else:
                        if self.dim is not m:
                            raise ValueError('size bound not match dim')
            else:
                bound = npa([0, 1] * self.dim)
            self.bound = bound
        else:
            self.dim = dim
            if bound is not None or []:
                bound = npa(bound)
                if len(bound.shape) == 1:
                    bound = np.repeat([bound], self.dim, axis=0)
                else:
                    m, n = bound.shape
                    if m == 1:
                        bound = np.repeat(bound, self.dim, axis=0)
                    else:
                        if self.dim is not m:
                            raise ValueError('size bound not match dim')
            else:
                bound = npa([[0, 1] * self.dim])
            self.bound = bound
            self.init_chromosome(init_method)
        self._fitness_value = min_fitness_value
        self.fitness_function = fitness_function
        self.transboundary_rules = transboundary_rules

    def transboundary(self):
        if self.transboundary_rules is 'bound':
            ind_low = self.chromosome < self.bound[:, 0]
            self.chromosome[ind_low] = self.bound[ind_low, 0]
            ind_high = self.chromosome > self.bound[:, 1]
            self.chromosome[ind_high] = self.bound[ind_high, 1]
        elif self.transboundary_rules is 'mod':
            ind = (self.bound[:, 0] > self.chromosome) + (self.chromosome > self.bound[:, 1]).astype(bool)
            self.chromosome[ind] = self.bound[ind, 0] + np.remainder(
                np.abs(self.chromosome[ind]), self.bound[ind, 1] - self.bound[ind, 0])
        elif self.transboundary_rules is 'random' or self.transboundary_rules is 'rand':
            ind = (self.bound[:, 0] > self.chromosome) + (self.chromosome > self.bound[:, 1]).astype(bool)
            self.chromosome[ind] = npr.rand(sum(ind)) * (self.bound[ind, 1] - self.bound[ind, 0]) + self.bound[ind, 0]
        else:
            raise NameError("transboundary_rules need in ('bound', 'mod', 'random)")

    def __gt__(self, agent):
        return self._fitness_value > agent.fitness_value

    def __lt__(self, agent):
        return self._fitness_value < agent.fitness_value

    def __cmp__(self, agent):
        return self.fitness_value - agent.fitness_value

    def __str__(self):
        return str(self.__class__) + '(chromosome: ' + str(self.chromosome) + ', fitness_value: ' + str(
            self.fitness_value) + ')'
