#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: sfla.py
# @time: 2018/9/9 0:47
# @Software: PyCharm

from slapy.swarm.sfla import Frog
from slapy.swarm.util import Engine
import numpy as np

npr = np.random
npa = np.array


class SFLAEngine(Engine):
    def __init__(self, population_size=100, steps=100, eps=0.01, dim=2, bound=[0, 1], fitness_function=None, *,
                 class_number=25, class_steps=25, smax=0.7, init_method='rand', min_fitness_value=-np.inf, agents=None, **kwargs):
        super().__init__(population_size, steps, eps, dim, bound, fitness_function, init_method=init_method,
                         min_fitness_value=min_fitness_value, agents=agents, **kwargs)
        self.class_number = class_number  # 组内最大数量
        self.class_steps = class_steps  # 组内最大迭代次数
        self.smax = smax  # 最大步长
        self.mean = []
        self.max = []
        self.best = []
        self.gbest = None

    def fitness(self, *args, **kwargs):
        return super().fitness(*args, **kwargs)


    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

    def analysis(self, *args, **kwargs):
        super().analysis(*args, **kwargs)

    def record(self, *args, **kwargs):
        super().record(*args, **kwargs)
