#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: Bat.py
# @time: 2018/9/5 2:06
# @Software: PyCharm


from slapy.swarm.util import Individual
import numpy as np

npr = np.random


class Bat(Individual):
    def __init__(self, chromosome=None, dim=2, bound=None, fitness_function=None, *, fitness_value=-np.inf,
                 a=0.25, r=0.5, v=None, qmin=0, qmax=2, init_method='random', **kwargs):
        super().__init__(chromosome, dim, bound, fitness_function, fitness_value=fitness_value, init_method=init_method,
                         **kwargs)
        self.qmax = qmax
        self.qmin = qmin
        self.v = v if v is not None else npr.rand(self.dim)
        self.a = a
        self.r = r

    def update(self, best_chromosome, *args, **kwargs):
        q = self.qmin + (-self.qmax + self.qmin) * npr.rand()
        self.v += (self.chromosome - best_chromosome) * q
        s = self.chromosome + self.v
        if npr.rand() > self.r:
            s = best_chromosome + 0.01 * npr.randn(self.dim)
        f_new = self.fitness_function(s)
        if f_new > self.fitness_value and npr.rand() < self.a:
            self.chromosome = s
            self.fitness_value = f_new
