#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: 
# @file: CSOPartical.py
# @time: 2018/7/30 21:07
# @Software: PyCharm

from slapy.swarm.util import Individual
import numpy as np

npr = np.random


class CSOParticle(Individual):

    def __init__(self,
                 chromosome=None,
                 dim=2,
                 fitness_value=-np.inf,
                 init_method='randn',
                 fitness_function=None,
                 v0=None,
                 vmax=None,
                 pbest=None,
                 w=0.8,
                 c1=2,
                 c2=2,
                 phi=0.2,
                 *args, **kwargs):
        super().__init__(chromosome=chromosome, dim=dim,
                         fitness_value=fitness_value,
                         fitness_function=fitness_function,
                         init_method=init_method,
                         *args, **kwargs)
        self.v = v0 if v0 else npr.rand()
        self.phi = phi

    def update(self, winner, center, *args, **kwargs):
        co1 = npr.rand(self.dim)
        co2 = npr.rand(self.dim)
        co3 = npr.rand(self.dim)
        self.v = co1 * self.v + \
                 co2 * (winner - self.chromosome) + \
                 self.phi * co3 * (center - self.chromosome)
        self.chromosome += self.v
        ind_high = self.chromosome > self.bound[:, 1]
        self.chromosome[ind_high] = self.bound[ind_high, 1]
        ind_low = self.chromosome < self.bound[:, 0]
        self.chromosome[ind_low] = self.bound[ind_low, 0]
