#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: SAEngine.py
# @time: 2018/8/30 9:21
# @Software: PyCharm

from slapy.swarm.util import Agent
import numpy as np

npa = np.array
npr = np.random
from matplotlib import pylab as plt
from copy import deepcopy


class SAEngine(Agent):
    def __init__(self, steps=1000, eps=0.01, chromosome=None, dim=2, bound=None, fitness_function=None, *,
                 fitness_value=-np.inf, init_method='random', t0=10, r=0.05, k=100, d=0.95, **kwargs):
        super(SAEngine, self).__init__(steps, eps, chromosome, dim, bound, fitness_function,
                                       fitness_value=fitness_value,
                                       init_method=init_method, **kwargs)
        self.t = t0  # 初始温度
        self.r = r  # 更新半径
        self.k = k  # Metropolis 接收准则参数
        self.d = d  # 降温系数

    def update(self, *args, **kwargs):
        super(SAEngine, self).update(*args, **kwargs)
        new_agent_chromosome = deepcopy(self.chromosome)
        ind = npr.randint(2,size=self.dim)
        new_agent_chromosome[ind] += np.random.rand(self.dim) * self.r - self.r / 2
        new_agent_fitness = self.fitness_function(new_agent_chromosome)
        if self.fitness_value < new_agent_fitness:
            self.chromosome = new_agent_chromosome
        elif npr.rand() < np.exp((-self.fitness_value + new_agent_fitness) / (self.k * self.t)):
            self.chromosome = new_agent_chromosome
        self.fitness()
        self.t *= self.d

    def initialize(self, *args, **kwargs):
        super(SAEngine, self).initialize(*args, **kwargs)
        self.gbest = deepcopy(self)
        self.best = []
        self.path = []
        self.t_list = []

    def record(self, *args, **kwargs):
        super(SAEngine, self).record(*args, **kwargs)
        self.path.append(deepcopy(self.chromosome))
        self.best.append(self.fitness_value)
        self.t_list.append(self.t)
        self.gbest = self.gbest if self.gbest.fitness_value > self.fitness_value else deepcopy(self)

    def analysis(self, *args, **kwargs):
        super(SAEngine, self).analysis(*args, **kwargs)
        print('-' * 15)
        print("best:", self.best)
        print('-' * 15)
        print("path:", self.path)
        print('-' * 15)
        plt.figure(1)
        path = npa(self.path)
        plt.plot(path[:, 0], path[:, 1], 'r+-')
        plt.figure(2)
        plt.title('itor in each steps')
        plt.plot(self.best, 'r-', label='best')
        # plt.plot(self.t_list, 'r-')
        plt.xlabel("Iteration")
        plt.ylabel("function value")
        plt.show()
        print(self.gbest)

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)
