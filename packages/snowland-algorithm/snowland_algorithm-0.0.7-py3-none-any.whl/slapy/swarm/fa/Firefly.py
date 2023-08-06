#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: Firefly.py
# @time: 2018/8/16 18:14
# @Software: PyCharm

from slapy.swarm.util import Individual
from scipy.spatial.distance import euclidean
from copy import deepcopy
import numpy as np

npr = np.random
npa = np.array


class Firefly(Individual):
    def __init__(self, chromosome=None, dim=2, bound=None, fitness_function=None, *, alpha0=0.025, l0=None, beta0=1, gamma=1,
                 beta_min=0.2, fitness_value=-np.inf, init_method='random', **kwargs):
        super().__init__(chromosome, dim, bound, fitness_function, fitness_value=fitness_value, init_method=init_method,
                         **kwargs)
        self.alpha = alpha0  # highly random
        self.beta_min = beta_min  # minimum value of beta
        self.beta0 = beta0  # the constant number for cal beta
        self.l = l0  # the light
        self.gamma = gamma  # Absorption coefficient
        bound = npa(self.bound)
        self.__scale = bound[:, 1] - bound[:, 0]

    def distance(self, firefly):
        return euclidean(self.chromosome, firefly.chromosome)

    def update(self, glowworms: list, self_ind, *args, **kwargs):
        for neighbor in glowworms:
            r = euclidean(self.chromosome, neighbor.chromosome)
            beta = (self.beta0 - self.beta_min) * np.exp(-self.gamma * r * r) + self.beta_min
            tmpf = self.alpha * (npr.rand(self.dim) - 0.5) * self.__scale
            self.chromosome = self.chromosome * (1 - beta) + neighbor.chromosome * beta + tmpf
            self.transboundary()
