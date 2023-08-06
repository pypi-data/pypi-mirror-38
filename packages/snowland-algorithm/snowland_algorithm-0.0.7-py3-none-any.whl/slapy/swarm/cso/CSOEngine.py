# !/user/bin/env/python
# -*- coding: utf-8 -*-
# @Time    : 
# @Author  : 保定新梦想网络科技有限公司 A.Star
# @Site    : www.bdxinmengxiang.com
# @file    : engine.py
# @time    : 2018/4/9 12:04
# @Software: PyCharm

from slapy.swarm.util import Engine
from slapy.swarm.cso.CSOParticle import CSOParticle
from copy import deepcopy
from matplotlib import pylab as plt
import numpy as np

npa = np.array
npr = np.random


class CSOEngine(Engine):

    def __init__(self, population_size=100,
                 steps=100,
                 eps=0.01,
                 dim=2,
                 fitness_function=None,
                 # ch=None,
                 # min_fitness_value=-np.inf,
                 # v0=None,
                 # vmax=None,
                 agents=None,
                 *args, **kwargs):
        super().__init__(population_size=population_size, steps=steps,
                         eps=eps, dim=dim, fitness_function=fitness_function,
                         agents=agents, *args, **kwargs)
        self._floor_half_popsize = self.population_size // 2

    def initialize(self, *args, **kwargs):
        self.mean = []
        self.max = []
        self.best = []
        if self.agents is None:
            self.agents = [CSOParticle(**(self.__dict__)) for _ in range(self.population_size)]

        self.gbest = self.agents[0]
        for each in self.agents:
            if each > self.gbest:
                self.gbest = deepcopy(each)

    def update(self, *args, **kwargs):
        npr.shuffle(self.agents)
        agent_matrix = npa([each.chromosome for each in self.agents])
        center = np.mean(agent_matrix, axis=0)
        # dic = self.agents[0].__dict__
        # center = [CSOParticle(mean_agent, **dic)]# * self._floor_half_popsize
        winner = []
        loser = []
        for ind in range(self._floor_half_popsize):
            if self.agents[ind] > self.agents[ind + self._floor_half_popsize]:
                winner.append(self.agents[ind])
                loser.append(self.agents[ind + self._floor_half_popsize])
            else:
                winner.append(self.agents[ind + self._floor_half_popsize])
                loser.append(self.agents[ind])
        [each_loser.update(winner=winner[ind].chromosome, center=center) for ind, each_loser in enumerate(loser)]
        ind_best = -1
        for ind, each_loser in enumerate(loser):
            if each_loser.fitness() > self.gbest.fitness_value:
                ind_best = ind
        if ind_best != -1:
            self.gbest = deepcopy(loser[ind_best])
        winner.extend(loser)
        self.agents = winner

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
        plt.title("CSO for function optimization")
        plt.legend()
        plt.show()
        print(self.gbest)

    def record(self, *args, **kwargs):
        fitness_list = npa([each.fitness() for each in self.agents])
        self.mean.append(np.mean(fitness_list))
        self.max.append(np.max(fitness_list))
        self.best.append(np.max(self.max))
