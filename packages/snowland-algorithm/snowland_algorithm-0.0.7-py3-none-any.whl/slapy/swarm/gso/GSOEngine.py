#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: GSOEngine.py
# @time: 2018/8/4 18:06
# @Software: PyCharm

from matplotlib import pylab as plt
from slapy.swarm.util import Engine
from slapy.swarm.gso import Glowworm
from copy import deepcopy
import numpy as np

npa = np.array
npr = np.random


class GSOEngine(Engine):
    """
    GSO算法求最大值
    """

    def __init__(self, population_size=100, steps=100, eps=0.01, dim=2, bound=[0, 1], fitness_function=None, *,
                 init_method='rand', min_fitness_value=-np.inf, rho=0.4, s=0.3, gamma=0.6, beta=0.8, rs=0.1, nt=4,
                 l0=None, agents=None, **kwargs):
        super().__init__(population_size, steps, eps, dim, bound, fitness_function, init_method=init_method,
                         min_fitness_value=min_fitness_value,
                         agents=agents, **kwargs)
        self.rho = rho  # 荧光素消失率
        self.gamma = gamma  # 荧光素更新率
        self.beta = beta  # 动态决策域更新率
        self.rs = rs  # 萤火虫感知域
        self.nt = nt  # 领域阈值
        self.s = s  # 初始步长
        self.r = npr.rand() * self.rs
        if l0:
            self.l = l0
        elif init_method == 'rand' or init_method == 'random':
            self.l = npr.rand()  # 亮度均匀分布
        else:
            self.l = npr.randn()  # 亮度高斯分布
        self.r_list = []
        self.mean = []
        self.max = []
        self.best = []
        self.gbest = None

    def initialize(self, *args, **kwargs):
        plt.ion()
        if self.agents is None:
            self.agents = [Glowworm(**(self.__dict__)) for _ in range(self.population_size)]
        self.gbest = self.agents[0]

    def update(self, *args, **kwargs):
        print(len(self.best))
        for ind in range(len(self.agents)):
            self.agents[ind].update(self.agents, ind)
            if self.agents[ind].fitness() > self.gbest.fitness_value:
                self.gbest = deepcopy(self.agents[ind])

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
        plt.title("GSO for function optimization")
        plt.legend()
        plt.show()
        print(self.gbest)

    def record(self, *args, **kwargs):
        fitness_list = npa([each.fitness() for each in self.agents])
        self.mean.append(np.mean(fitness_list))
        self.max.append(np.max(fitness_list))
        self.best.append(np.max(self.max))
        self.r_list.append([each.r for each in self.agents])
        plt.clf()
        ax = plt.subplot(111)
        [plt.plot(each.chromosome[0], each.chromosome[1], 'g*') for each in self.agents]
        plt.plot(self.gbest.chromosome[0], self.gbest.chromosome[1], 'ro')
        [ax.add_patch(plt.Circle(xy=each.chromosome, radius=each.r, alpha=0.5, edgecolor='r', fill=False)) for each in
         self.agents]
        plt.pause(0.2)
