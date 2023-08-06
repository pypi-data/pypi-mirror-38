#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: Cuckoo.py
# @time: 2018/10/18 9:46
# @Software: PyCharm


from slapy.swarm.util import Individual
import numpy as np

npa = np.array
npr = np.random


class Cuckoo(Individual):
    def __init__(self, chromosome=None, dim=2, bound=None, fitness_function=None, *, min_fitness_value=-np.inf,
                 alpha=0.1, init_method='random', transboundary_rules='random', **kwargs):
        super().__init__(chromosome, dim, bound, fitness_function, min_fitness_value=min_fitness_value,
                         init_method=init_method, transboundary_rules=transboundary_rules, **kwargs)
        self.alpha = alpha  # 步长因子

    def update(self, *args, **kwargs):
        pass

    def __str__(self):
        super().__str__()
