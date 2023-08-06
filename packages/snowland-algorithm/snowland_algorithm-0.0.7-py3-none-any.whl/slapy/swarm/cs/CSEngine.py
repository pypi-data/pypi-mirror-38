#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: CSEngine.py
# @time: 2018/10/18 4:03
# @Software: PyCharm


from slapy.swarm.util import Engine
from slapy.swarm.cs.Cuckoo import Cuckoo
import numpy as np
from copy import deepcopy
from functools import reduce
from scipy.special import gamma
npr = np.random
npa = np.array
from matplotlib import pylab as plt


class CSEngine(Engine):
    def __init__(self, population_size=100, steps=100, eps=1e-6, dim=2, bound=[0, 1], fitness_function=None, *,
                 pa=0.2, pc=0.6, alpha=0.01,
                 init_method='rand', min_fitness_value=-np.inf, agents=None, transboundary_rules='bound', **kwargs):
        super().__init__(population_size, steps, eps, dim, bound, fitness_function, init_method=init_method,
                         min_fitness_value=min_fitness_value, agents=agents, transboundary_rules=transboundary_rules,
                         **kwargs)
        self.agents = []
        self.pa = pa  #
        self.pc = pc  #
        self.alpha = alpha
        if self.agents is None or self.agents == []:
            self.agents = [Cuckoo(**(self.__dict__)) for _ in range(self.population_size)]
        self.gbest = reduce(lambda a, b: a if a > b else b, self.agents)


    def update(self, *args, **kwargs):
        self.get_cuckoos()
        self.empty_nest()
        self.gbest = reduce(lambda a, b: a if a > b else b, self.agents)

    def empty_nest(self):
        ind = npr.rand(self.population_size) > self.pa
        a = npr.choice(self.agents, self.population_size - np.sum(ind))
        b = npr.choice(self.agents, self.population_size - np.sum(ind))
        index_ab = 0
        # for ind, agent in enumerate(self.agents):
        #     if npr.rand() > self.pa:  # 窝是否被发现
        #         a, b = npr.choice(self.agents, 2, False)
        #         agent.chromosome += npr.rand(self.dim) * (b.chromosome-a.chromosome)
        #         agent.transboundary()
        #         new_agents.append(agent)
        #     else:
        #         new_agents.append(agent)
        # self.agents = new_agents[:]
        rand = npr.rand()
        for i, agent in enumerate(self.agents):
            if not ind[i]:
                tmp = deepcopy(agent)
                tmp.chromosome += rand * (a[index_ab].chromosome - b[index_ab].chromosome)
                if tmp.fitness() > self.agents[i].fitness():
                    self.agents[i] = tmp
                index_ab += 1
                self.agents[i].transboundary()


        # self.agents = [each for i, each in enumerate(self.agents) if ind[i]]
        # for ind, agent in enumerate(a):
        #     self.agents.append(npr.rand(self.dim) * (agent.chromosome - b[ind].chromosome))
        # [self.agents[i].transboundary() for i in range(self.population_size)]

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.mean = []
        self.best = []
        self.max = []
        if __debug__:
            self.pre = self.agents[:]
            self.color = npr.rand(self.population_size,3)
    def get_cuckoos(self):
        beta = 3 / 2
        sigma = (gamma(1 + beta) * np.sin(np.pi * beta / 2) / (gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (1 / beta)
        for ind, agent in enumerate(self.agents):
            u = npr.randn(self.dim) * sigma
            v = npr.randn(self.dim)
            step = u / np.abs(v) ** (1 / beta)
            # In the next equation, the difference factor (s-best) means that
            # when the solution is the best solution, it remains unchanged.
            stepsize = self.alpha * step * (agent.chromosome - self.gbest.chromosome)
            # Here the factor 0.01 comes from the fact that L/100 should the typical
            # step size of walks/flights where L is the typical lenghtscale
            # otherwise, Levy flights may become too aggresive/efficient,
            # which makes new solutions (even) jump out side of the design domain
            # (and thus wasting evaluations).
            # Now the actual random walks or flights
            self.agents[ind].chromosome += stepsize * npr.randn(self.dim)
            self.agents[ind].transboundary()

    def record(self, *args, **kwargs):
        super().record(*args, **kwargs)
        fitness_list = npa([each.fitness() for each in self.agents])
        self.mean.append(np.mean(fitness_list))
        self.max.append(np.max(fitness_list))
        self.best.append(np.max(self.max))
        if __debug__:
            x = [each.chromosome[0] for each in self.agents]
            y = [each.chromosome[1] for each in self.agents]

            x1 = [each.chromosome[0] for each in self.pre]
            y1 = [each.chromosome[1] for each in self.pre]
            for ind in range(self.population_size):
                plt.plot([x1[ind],x[ind]], [y1[ind], y[ind]], '-', color=self.color[ind,:])
            plt.plot(self.gbest.chromosome[0], self.gbest.chromosome[1], 'ro')

            plt.pause(1)
            self.pre = deepcopy(self.agents)


    def analysis(self, *args, **kwargs):
        super().analysis(*args, **kwargs)
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
        plt.title("CS for function optimization")
        plt.legend()
        plt.show()
        print(self.gbest.chromosome)

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)
