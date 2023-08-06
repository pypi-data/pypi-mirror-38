#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: Firework.py
# @time: 2018/9/26 3:34
# @Software: PyCharm

from slapy.swarm.util.Individual import Individual
import numpy as np


npr = np.random
npa = np.array


class Firework(Individual):
    def __init__(self, chromosome=None, dim=2, bound=None, fitness_function=None, *, fitness_value=-np.inf,
                 scope=None, son_number=0, sons=None, init_method='random', **kwargs):
        super().__init__(chromosome, dim, bound, fitness_function, fitness_value=fitness_value, init_method=init_method,
                         **kwargs)
        self.sons = sons if sons else []
        self.scope = scope
        self.son_number = son_number if son_number else 0

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

    def fitness(self, *args, **kwargs):
        return super().fitness(*args, **kwargs)