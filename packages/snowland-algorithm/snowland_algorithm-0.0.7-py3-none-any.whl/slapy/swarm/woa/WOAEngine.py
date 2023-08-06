#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: WOAEngine.py
# @time: 2018/9/24 1:21
# @Software: PyCharm

from slapy.swarm.util.Engine import Engine
import numpy as np
npa = np.array
npr = np.random
from matplotlib import pylab as plt
from slapy.swarm.woa.Whales import Whales


class WOAEngine(Engine):
    def __init__(self, population_size=100, steps=100, eps=0.01, dim=2, bound=[0, 1], fitness_function=None, *,
                 init_method='rand', min_fitness_value=-np.inf, agents=None, **kwargs):
        super().__init__(population_size, steps, eps, dim, bound, fitness_function, init_method=init_method,
                         min_fitness_value=min_fitness_value, agents=agents, **kwargs)
        self.fitness_function = lambda x: fitness_function(x)
        self.leader_pos = np.zeros(self.dim)


    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        if self.agents is None:
            self.agents = [Whales(population_size=self.population_size, steps=self.steps, **(self.__dict__)) for _ in range(self.population_size)]
        self.gbest = self.agents[0]
        self.mean = []
        self.best = []
        self.max = []

    def update(self, *args, **kwargs):
        fit = self.fitness()
        leader_ind = np.argmax(fit)
        self.gbest = self.agents[leader_ind]

        super().update(agents=self.agents, leader_pos=self.gbest.chromosome)


    def analysis(self, *args, **kwargs):
        print('-' * 15)
        print("best:", self.best)
        print("mean:", self.mean)
        print("max:", self.max)
        print('-' * 15)
        # plt.ioff()
        plt.figure(1)
        plt.plot(self.gbest.chromosome[0], self.gbest.chromosome[1], 'ro')
        plt.figure(2)
        plt.title('itor in each steps')
        plt.plot(self.mean, 'b-', label='mean')
        plt.plot(self.max, 'g-', label='max')
        plt.plot(self.best, 'r-', label='best')
        plt.xlabel("Iteration")
        plt.ylabel("function value")
        plt.title("WOA for function optimization")
        plt.legend()
        plt.show()
        print(self.gbest)

    def record(self, *args, **kwargs):
        super().record(*args, **kwargs)
        fitness_list = npa([each.fitness() for each in self.agents])
        self.mean.append(np.mean(fitness_list))
        self.max.append(np.max(fitness_list))
        self.best.append(np.max(self.max))
        # plt.clf()
        # ax = plt.subplot(111)
        # [plt.plot(each.chromosome[0], each.chromosome[1], 'g*') for each in self.agents]
        # plt.plot(self.gbest.chromosome[0], self.gbest.chromosome[1], 'ro')
        # plt.pause(0.2)