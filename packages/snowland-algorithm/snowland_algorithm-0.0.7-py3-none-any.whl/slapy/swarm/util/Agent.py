#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: Node.py
# @time: 2018/8/28 11:32
# @Software: PyCharm


from .Individual import Individual
from .Engine import Engine
import numpy as np

npr = np.random
npa = np.array


class Agent(Individual, Engine):
    def __init__(self,
                 steps=100,
                 eps=0.01,
                 chromosome=None,
                 dim=2,
                 bound=None,
                 fitness_function=None,
                 *,
                 fitness_value=-np.inf,
                 init_method='random',
                 transboundary_rules='bound',
                 **kwargs):
        self.steps = steps
        self.eps = eps
        if chromosome:
            self._chromosome = chromosome
            self.dim = len(chromosome)
            if bound:
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
                bound = npa([[0, 1] * self.dim])
            self.bound = bound
        else:
            self.dim = dim
            if bound:
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
                bound = npa([[0, 1] for _ in range(self.dim)])
            self.bound = bound
            if init_method == 'rand' or init_method == 'random':
                self._chromosome = npr.random(dim) * (bound[:, 1] - bound[:, 0]).flatten() + bound[:, 0].flatten()
            else:
                self._chromosome = npr.randn(dim) * (bound[:, 1] - bound[:, 0]).flatten() + bound[:, 0].flatten()
        self._fitness_value = fitness_value
        self.fitness_function = fitness_function
        self.transboundary_rules = transboundary_rules

    def update(self, *args, **kwargs):
        return super(Agent, self).update(*args, **kwargs)

    def initialize(self, *args, **kwargs):
        pass

    def record(self, *args, **kwargs):
        pass

    def analysis(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        self.initialize(*args, **kwargs)
        for i in range(self.steps):
            self.fitness(*args, **kwargs)
            self.record(*args, **kwargs)
            self.update(*args, **kwargs)
        self.fitness(*args, **kwargs)
        self.record(self, *args, **kwargs)
        self.analysis(*args, **kwargs)
