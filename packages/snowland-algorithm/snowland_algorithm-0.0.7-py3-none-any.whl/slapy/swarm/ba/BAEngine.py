#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: BAEngine.py
# @time: 2018/9/5 2:06
# @Software: PyCharm

from slapy.swarm.util import Engine
from slapy.swarm.ba.Bat import Bat
import numpy as np
from matplotlib import pylab as plt
from copy import deepcopy

npa = np.array
npr = np.random


class BAEngine(Engine):
    def __init__(self, population_size=100, steps=100, eps=0.01, dim=2, bound=[0, 1], fitness_function=None, *,
                 a=0.25, r=0.5, v=None, qmin=0, qmax=2, init_method='rand', min_fitness_value=-np.inf, agents=None,
                 **kwargs):
        super().__init__(population_size, steps, eps, dim, bound, fitness_function, init_method=init_method,
                         min_fitness_value=min_fitness_value, agents=agents, **kwargs)
        self.a = a  # loudness
        self.r = r  # pulse rate
        self.v = v if v is not None else npr.rand(self.dim)
        self.qmin = qmin
        self.qmax = qmax

    def initialize(self, *args, **kwargs):
        self.mean = []
        self.max = []
        self.best = []
        if self.agents is None:
            self.agents = [Bat(**(self.__dict__)) for _ in range(self.population_size)]

        self.gbest = self.agents[0]
        for each in self.agents:
            if each > self.gbest:
                self.gbest = deepcopy(each)

    def update(self, *args, **kwargs):
        super().update(self.gbest.chromosome, *args, **kwargs)
        for each in self.agents:
            if each.fitness_value > self.gbest.fitness_value:
                self.gbest = deepcopy(each)

    def analysis(self, *args, **kwargs):
        print('-' * 15)
        print("best:", self.best)
        print("mean:", self.mean)
        print("max:", self.max)
        print('-' * 15)
        plt.ioff()
        plt.figure(1)
        plt.plot(self.gbest.chromosome[0], self.gbest.chromosome[1], 'ro')
        plt.figure(2)
        plt.title('itor in each steps')
        plt.plot(self.mean, 'b-', label='mean')
        plt.plot(self.max, 'g-', label='max')
        plt.plot(self.best, 'r-', label='best')
        plt.xlabel("Iteration")
        plt.ylabel("function value")
        plt.title("BA for function optimization")
        plt.legend()
        plt.show()
        print(self.gbest)

    def record(self, *args, **kwargs):
        fitness_list = npa([each.fitness() for each in self.agents])
        self.mean.append(np.mean(fitness_list))
        self.max.append(np.max(fitness_list))
        self.best.append(np.max(self.max))
