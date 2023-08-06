#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: AFASEngine.py
# @time: 2018/9/11 2:44
# @Software: PyCharm

from slapy.swarm.util import Engine
from slapy.swarm.afas.AFASIndividual import AFASIndividual
import numpy as np
from copy import deepcopy
from matplotlib import pylab as plt
from scipy.spatial.distance import euclidean

npa = np.array
npr = np.random

class AFASEngine(Engine):
    def __init__(self, population_size=100, steps=100, eps=0.01, dim=2, bound=[0, 1], fitness_function=None, *,
                 init_method='rand',try_number=100, serch_length=1,delta=0.618, step=0.1, min_fitness_value=-np.inf, agents=None, **kwargs):
        super().__init__(population_size, steps, eps, dim, bound, fitness_function, init_method=init_method,
                         min_fitness_value=min_fitness_value, agents=agents, **kwargs)
        self.serch_length = serch_length  # 搜索半径
        self.try_number = try_number  # 种群内迭代次数
        self.delta = delta  # 拥挤度

    def fitness(self, *args, **kwargs):
        return super().fitness(*args, **kwargs)

    def initialize(self, *args, **kwargs):
        self.mean = []
        self.max = []
        self.best = []
        if self.agents is None:
            self.agents = [AFASIndividual(**(self.__dict__)) for _ in range(self.population_size)]

        self.gbest = self.agents[0]
        for each in self.agents:
            if each > self.gbest:
                self.gbest = deepcopy(each)
        self.fitness_value = self.fitness()
        bestIndex = np.argmax(self.fitness)
        self.best.append(self.fitness_value[bestIndex])
        self.gbest = deepcopy(self.agents[bestIndex])
        self.avefitness = np.mean(self.fitness_value)
        # self.trace[self.t, 0] = (1 - self.best.fitness) / self.best.fitness
        # self.trace[self.t, 1] = (1 - self.avefitness) / self.avefitness
        # print("Generation %d: optimal function value is: %f; average function value is %f" % (
            # self.t, self.trace[self.t, 0], self.trace[self.t, 1]))

    def update(self, *args, **kwargs):
        for i in range(0, self.population_size):
            xi1 = self.huddle(self.agents[i])
            xi2 = self.follow(self.agents[i])
            if xi1.fitness > xi2.fitness:
                self.agents[i] = xi1
                self.fitness[i] = xi1.fitness
            else:
                self.agents[i] = xi2
                self.fitness[i] = xi2.fitness
        best = np.max(self.fitness)
        bestIndex = np.argmax(self.fitness)
        if best > self.best.fitness:
            self.best = deepcopy(self.population[bestIndex])

    def analysis(self, *args, **kwargs):
        super().analysis(*args, **kwargs)
        # print("Optimal function value is: %f; " % self.trace[self.t, 0])
        # print("Optimal solution is:")
        print(self.gbest.chromosome)
        # x = np.arange(0, self.MAXGEN)
        # y1 = self.trace[:, 0]
        # y2 = self.trace[:, 1]
        # plt.plot(x, y1, 'r', label='optimal value')
        # plt.plot(x, y2, 'g', label='average value')
        plt.xlabel("Iteration")
        plt.ylabel("function value")
        plt.title("Artificial Fish Swarm algorithm for function optimization")
        plt.legend()
        plt.show()

    def record(self, *args, **kwargs):
        super().record(*args, **kwargs)
        self.avefitness = np.mean(self.fitness_value)
        # self.trace[self.t, 0] = (1 - self.best.fitness) / self.best.fitness
        # self.trace[self.t, 1] = (1 - self.avefitness) / self.avefitness
        # print("Generation %d: optimal function value is: %f; average function value is %f" % (
        #     self.t, self.trace[self.t, 0], self.trace[self.t, 1]))

    def forage(self, x):
        """
        artificial fish foraging behavior
        """
        newInd = deepcopy(x)
        found = False
        for i in range(0, self.params[3]):
            indi = self.randSearch(x, self.params[0])
            if indi.fitness() > x.fitness():
                newInd.chromosome = x.chromosome + npr.random(self.dim) * self.params[1] * self.lennorm * (
                        indi.chromosome - x.chromosome) / euclidean(indi.chromosome, x.chromosome)
                newInd = indi
                found = True
                break
        if not (found):
            newInd = self.randSearch(x)
        return newInd

    def randSearch(self, x):
        """
        artificial fish random search behavior
        """
        searLen = self.search_length
        ind = deepcopy(x)
        ind.chromosome += np.random.uniform(-1, 1,
                                       self.dim) * searLen * self.lennorm
        ind_low = ind.chromosome < self.bound[:, 0]
        ind.chromosome[ind_low] = self.bound[ind_low, 0]
        ind_high = ind.chromosome > self.bound[:, 1]
        ind.chromosome[ind_high] = self.bound[ind_high, 1]
        self.fitness_function(ind.chromosome)
        return ind

    def huddle(self, x):
        """
        artificial fish huddling behavior
        """
        newInd = deepcopy(x)
        dist = self.distance(x)
        index = []
        # for i in range(1, self.population_size):
        #     if 0 < dist[i] < self.params[0] * self.lennorm:
        #         index.append(i)
        # index = [i for i, agent in enumerate(self.agents) if 0 < dist[i] < self.params[0] * self.lennorm]
        # TODO check
        index = [i for i, agent in enumerate(self.agents) if 0 < dist[i] < self.serch_length * self.lennorm]
        nf = len(index)
        if nf > 0:
            xc = np.zeros(self.dim)
            for i in range(0, nf):
                xc += self.population[index[i]].chromosome
            xc = xc / nf
            cind = AFASIndividual(self.dim, self.bound)
            cind.chromosome = xc
            if (cind.fitness() / nf) > (self.params[2] * x.fitness()):
                xnext = x.chromosome + np.random.random(
                    self.dim) * self.params[1] * self.lennorm * (xc - x.chromosome) / np.linalg.norm(xc - x.chromosome)
                ind_low = xnext < self.bound[:, 0]
                xnext[ind_low] = self.bound[ind_low, 0]
                ind_high = xnext > self.bound[:, 1]
                xnext[ind_high] = self.bound[ind_high, 1]
                newInd.chromosome = xnext
                self.fitness_value(newInd)
                # print "hudding"
                return newInd
            else:
                return self.forage(x)
        else:
            return self.forage(x)

    def follow(self, x):
        """
        artificial fish following behivior
        """
        newInd = deepcopy(x)
        dist = self.distance(x)
        index = []
        for i in range(1, self.population_size):
            if dist[i] > 0 and dist[i] < self.params[0] * self.lennorm:
                index.append(i)
        nf = len(index)
        if nf > 0:
            best = -np.inf
            bestIndex = 0
            for i in range(0, nf):
                if self.population[index[i]].fitness > best:
                    best = self.population[index[i]].fitness
                    bestIndex = index[i]
            if (self.population[bestIndex].fitness / nf) > (self.params[2] * x.fitness):
                xnext = x.chromosome + npr.random(
                    self.dim) * self.params[1] * self.lennorm * (
                                self.population[bestIndex].chromosome - x.chromosome) / np.linalg.norm(
                    self.agents[bestIndex].chromosome - x.chromosome)

                ind_low = xnext < self.bound[:, 0]
                xnext[ind_low] = self.bound[ind_low, 0]
                ind_high = xnext > self.bound[:, 1]
                xnext[ind_high] = self.bound[ind_high, 1]
                newInd.chromosome = xnext
                self.fitness_function(newInd.chromosome)
                # print "follow"
                return newInd
            else:
                return self.forage(x)
        else:
            return self.forage(x)

    def distance(self, x: AFASIndividual):
        """
        return the distance array to a individual
        """
        return npa([euclidean(x.chromosome, each.chromosome) for each in self.agents])
