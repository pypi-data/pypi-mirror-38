#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: AFAS.py
# @time: 2018/9/11 2:39
# @Software: PyCharm


import numpy as np

import copy
from slapy.swarm.util import Individual

class AFASIndividual(Individual):

    """class for AFSIndividual"""

    def __init__(self, chromosome=None, dim=2, bound=None, fitness_function=None, *, fitness_value=-np.inf,
                 init_method='random', **kwargs):
        super().__init__(chromosome, dim, bound, fitness_function, fitness_value=fitness_value, init_method=init_method,
                         **kwargs)