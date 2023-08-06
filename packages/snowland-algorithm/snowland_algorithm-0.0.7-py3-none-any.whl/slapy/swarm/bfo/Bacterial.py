#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: Bacterial.py
# @time: 2018/10/29 15:23
# @Software: PyCharm


import numpy as np
from slapy.swarm.util import Individual

npr = np.random

class Bacterial(Individual):
    """
    individual of baterial clony foraging algorithm
    """
    def __init__(self, chromosome=None, dim=2, bound=None, fitness_function=None, *, min_fitness_value=-np.inf,
                 init_method='random', transboundary_rules='random', **kwargs):
        super().__init__(chromosome, dim, bound, fitness_function, min_fitness_value=min_fitness_value,
                         init_method=init_method, transboundary_rules=transboundary_rules, **kwargs)

        self.trials = 0
