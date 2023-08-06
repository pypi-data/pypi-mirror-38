#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: Whales.py
# @time: 2018/9/24 1:08
# @Software: PyCharm


from slapy.swarm.util.Individual import Individual
import numpy as np

npr = np.random
npa = np.array


class Whales(Individual):
    def __init__(self, chromosome=None, dim=2, bound=None, fitness_function=None, *, fitness_value=-np.inf,
                 init_method='random', itor=0, steps=None, population_size=None, agents=None,
                 **kwargs):
        super().__init__(chromosome, dim, bound, fitness_function, fitness_value=fitness_value, init_method=init_method,
                         **kwargs)
        # self.leader_pos = np.zeros(self.dim) if leader_pos is None else leader_pos
        self.population_size = population_size
        self.agents = agents
        self.itor = itor
        self.steps = steps if steps is not None else 100

    def update(self, agents, leader_pos, *args, **kwargs):
        a = 2 - self.itor * ((2) / self.steps)
        # a decreases linearly from 2 to 0 in Eq.(2.3)

        # a2 linearly dicreases from -1 to - 2 to calculate in Eq.(3.12)
        a2 = -1 + self.itor * ((-1) / self.steps)

        r1, r2 = npr.random(2)
        A = 2 * a * r1 - a
        C = 2 * r2  # Eq.(2.4) in the paper

        b = 1  # parameters in Eq.(2.5)
        l = (a2 - 1) * npr.rand() + 1  # parameters in Eq.(2.5)

        p = npr.random()
        if p > 0.5:
            distance2Leader = np.abs(leader_pos - self.chromosome)  # Eq.(2.5)
            self.chromosome = distance2Leader * np.exp(b * l) * np.cos(l * 2 * np.pi) + leader_pos
        elif np.abs(A) > 1:
            rand_leader_index = npr.randint(self.population_size, size=self.dim)
            rand_chromosome = npa([agents[index].chromosome[i] for i, index in enumerate(rand_leader_index)])
            D_X_rand = np.abs(C * rand_chromosome - self.chromosome)  # Eq.(2.7)
            self.chromosome = rand_chromosome - A * D_X_rand  # Eq.(2.8)
        else:
            D_Leader = np.abs(C * leader_pos - self.chromosome)  # Eq.(2.1)
            self.chromosome = leader_pos - A * D_Leader  # Eq.(2.2)

        self.transboundary()
        self.itor += 1
