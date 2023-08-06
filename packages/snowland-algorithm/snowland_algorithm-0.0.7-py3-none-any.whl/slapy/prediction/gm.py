#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: gm.py
# @time: 2018/9/2 17:44
# @Software: PyCharm


# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 19:23:24 2016

@author: DaiPW
"""

import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from slapy.prediction.util import PredictionModel

npa = np.array
npm = np.matrix


class GM_1_1_model(PredictionModel):

    def __init__(self, x=None, a=0, u=0):
        self.a, self.u = a, u
        self.x = npm(x)
        self.train()
        self.res = None

    def train(self):
        cumsum_x = np.cumsum(self.x)
        C = -(cumsum_x[0, :-1] + cumsum_x[0, 1:]) / 2
        # Calculate parameters
        E = np.vstack((C, np.ones(C.shape[1])))
        c = (E * E.T).I * E * self.x[0, 1:].T
        self.a, self.u = c[0, 0], c[1, 0]

    def draw(self, n=3):
        g, n = (self.predict(n), n) if self.res is None else (self.res, len(self.res) - self.x.shape[1] + 1)
        plt.plot(np.linspace(0, self.x.shape[1] - 1, self.x.shape[1]), self.x.tolist()[0], 'b-')
        plt.plot(np.linspace(1, self.x.shape[1] + n - 1, self.x.shape[1] + n - 1), g, 'r-')
        plt.show()

    def predict(self, n=3):
        length = self.x.shape[1]
        v = np.linspace(0, length + n - 1, length + n)
        f = (self.x[0, 0] - self.u / self.a) / np.exp(self.a * v) + self.u / self.a
        g = f[1:] - f[:-1]
        self.res = g
        return g

    def epsilon(self):
        g = self.predict(0) if self.res is None else deepcopy(self.res[:self.x.shape[1] - 1])
        eps = g - npa(self.x).flatten()[1:]
        return np.hstack((npa([0]), eps))

    def rho(self):
        g = self.predict(0) if self.res is None else deepcopy(self.res[:self.x.shape[1] - 1])
        lmd = g[:-1] / g[1:]
        return 1 - (1 - self.a / 2) * lmd / (1 + self.a / 2)

    def delta(self):
        return self.epsilon() / npa(self.x).flatten()

    e = epsilon
