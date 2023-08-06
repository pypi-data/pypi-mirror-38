#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: Glowworm.py
# @time: 2018/8/4 18:07
# @Software: PyCharm

from slapy.swarm.util import Individual
import numpy as np
from scipy.spatial.distance import euclidean

npr = np.random
npa = np.array


class Glowworm(Individual):
    def __init__(self, chromosome=None, dim=2, bound=None, fitness_function=None, *, fitness_value=-np.inf,
                 init_method='random', rho=0.1, s=0.5, gamma=0.1, beta=0.1, rs=1, nt=8, l0=None, **kwargs):
        super().__init__(chromosome, dim, bound, fitness_function, fitness_value=fitness_value, init_method=init_method,
                         **kwargs)

        self.rho = rho  # 荧光素消失率
        self.gamma = gamma  # 荧光素更新率
        self.beta = beta  # 动态决策域更新率
        self.rs = rs  # 萤火虫感知域
        self.nt = nt  # 领域阈值
        self.r = npr.rand() * self.rs  # 决策半径
        self.s = s  # 初始化步长
        if l0:
            self.l = l0
        elif init_method == 'rand' or init_method == 'random':
            self.l = npr.rand()  # 亮度均匀分布
        else:
            self.l = npr.randn()  # 亮度高斯分布

    def update(self, glowworms: list, self_ind, *args, **kwargs):
        neighbors = self.get_neighbors(glowworms, self_ind)
        if neighbors:
            lights = npa([each[1].l for each in neighbors])
            p = lights / np.sum(lights)
            cumsum_p = np.cumsum(p)
            r = npr.rand()
            ind = np.sum(r > cumsum_p)

            self.chromosome = self.chromosome + self.s * (neighbors[ind][1].chromosome - self.chromosome) / (euclidean(neighbors[ind][1].chromosome, self.chromosome) + 1e-6)

            ind_low = self.chromosome < self.bound[:, 0]
            self.chromosome[ind_low] = self.bound[ind_low, 0]
            ind_high = self.chromosome > self.bound[:, 1]
            self.chromosome[ind_high] = self.bound[ind_high, 1]
        self.r = min(self.rs, max(0, self.r + self.beta * self.nt - len(neighbors)))
        self.l = (1 - self.rho) * self.l + self.gamma * self.fitness()

    def get_neighbors(self, glowworms: list, self_ind):
        neighbors = []
        for ind, each_glowworm in enumerate(glowworms):
            if self.l <= each_glowworm.l and euclidean(self.chromosome, each_glowworm.chromosome) <= self.r and ind != self_ind:
                neighbors.append((ind, each_glowworm))
        return neighbors
