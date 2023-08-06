#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: FOEngine.py
# @time: 2018/9/4 18:23
# @Software: PyCharm

from slapy.swarm.util import Engine
import numpy as np


class FOAEngine(Engine):
    def __init__(self, population_size=100, steps=100, eps=0.01, dim=2, bound=[0, 1], fitness_function=None, *,
                 init_method='rand', min_fitness_value=-np.inf, agents=None, **kwargs):
        super().__init__(population_size, steps, eps, dim, bound, fitness_function, init_method=init_method,
                         min_fitness_value=min_fitness_value, agents=agents, **kwargs)

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        d = np.sqrt(self.chromosome[0, :] ** 2 + self.chromosome[1, :] ** 2)
        s = 1 / d

        smell = self.fitness_function(s)

    def analysis(self, *args, **kwargs):
        super().analysis(*args, **kwargs)

    def record(self, *args, **kwargs):
        super().record(*args, **kwargs)
