#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: Fly.py
# @time: 2018/9/5 2:05
# @Software: PyCharm


from slapy.swarm.util import Individual
import numpy as np

npr = np.random
npa = np.array


class Fly(Individual):
    def __init__(self, chromosome=None, dim=2, bound=None, fitness_function=None, *, fitness_value=-np.inf,
                 init_method='random', **kwargs):
        if chromosome is not None:
            super._chromosome = chromosome
            super.dim = len(chromosome)
            if bound is not None or []:
                bound = npa(bound)
                if len(bound.shape) == 1:
                    bound = np.repeat([bound], super.dim, axis=0)
                else:
                    m, n = bound.shape
                    if m == 1:
                        bound = np.repeat([bound], super.dim, axis=0)
                    else:
                        if super.dim is not m:
                            raise ValueError('size bound not match dim')
            else:
                bound = npa([[0, 1] for _ in range(super.dim)])
            super.bound = bound
        else:
            super.dim = dim
            if bound is not None or []:
                bound = npa(bound)
                if len(bound.shape) == 1:
                    bound = np.repeat([bound], self.dim, axis=0)
                else:
                    m, n = bound.shape
                    if m == 1:
                        bound = np.repeat(bound, self.dim, axis=0)
                    else:
                        if super.dim is not m:
                            raise ValueError('size bound not match dim')
            else:
                bound = npa([[0, 1] for _ in range(self.dim)])
            super.bound = bound
            if init_method == 'rand' or init_method == 'random':
                super._chromosome = npr.random(2, dim) - 1
            else:
                super._chromosome = npr.randn(2, dim) - 1
        super._fitness_value = fitness_value
        super.fitness_function = fitness_function


def update(self, *args, **kwargs):
    pass
