#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: Frog.py
# @time: 2018/9/9 0:48
# @Software: PyCharm

from slapy.swarm.util import Individual
import numpy as np
class Frog(Individual):
    def __init__(self, chromosome=None, dim=2, bound=None, fitness_function=None, *, fitness_value=-np.inf,
                 init_method='random', **kwargs):
        super().__init__(chromosome, dim, bound, fitness_function, fitness_value=fitness_value, init_method=init_method,
                         **kwargs)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)