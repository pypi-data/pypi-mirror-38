#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: FAEngine.py
# @time: 2018/8/16 18:13
# @Software: PyCharm

from matplotlib import pylab as plt
from slapy.swarm.util import Engine
from slapy.swarm.fa import Firefly
from copy import deepcopy
import numpy as np

npa = np.array
npr = np.random


class FAEngine(Engine):
    def __init__(self, population_size=100, steps=100, eps=0.01, dim=2, bound=[0, 1], fitness_function=None, *,
                 alpha0=0.25, beta0=1, beta_min=0.1, l0=0.5, gamma0=1, init_method='rand', min_fitness_value=-np.inf,
                 agents=None, **kwargs):
        super().__init__(population_size, steps, eps, dim, bound, fitness_function, init_method=init_method,
                         min_fitness_value=min_fitness_value, agents=agents, **kwargs)
        self.alpha = alpha0
        self.beta = beta_min
        self.beta0 = beta0
        self.gamma = gamma0
        self.gamma0 = gamma0
        self.l0 = l0
        self.l = l0
        bound = npa(self.bound)
        self.__scale = bound[:,1]-bound[:,0]

    def initialize(self, *args, **kwargs):
        plt.ion()
        if self.agents is None:
            self.agents = [Firefly(**(self.__dict__)) for _ in range(self.population_size)]
        self.gbest = self.agents[0]
        self.r_list = []
        self.mean = []
        self.max = []
        self.best = []

    def update(self, *args, **kwargs):
        self.agents.sort(reverse=True)
        [self.agents[i].update(self.agents[:i], i) for i in range(self.population_size)]

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
        plt.title("FA for function optimization")
        plt.legend()
        plt.show()
        print(self.gbest)

    def record(self, *args, **kwargs):
        fitness_list = npa([each.fitness() for each in self.agents])
        self.mean.append(np.mean(fitness_list))
        self.max.append(np.max(fitness_list))
        self.best.append(np.max(self.max))
        plt.clf()
        ax = plt.subplot(111)
        [plt.plot(each.chromosome[0], each.chromosome[1], 'g*') for each in self.agents]
        plt.plot(self.gbest.chromosome[0], self.gbest.chromosome[1], 'ro')
        plt.pause(0.2)

    def getS(self, r):
        return self.s0 * np.exp(-self.beta * r * r)

    def getGamma(self, r):
        return self.gamma0 * np.exp(-self.beta * r * r)
