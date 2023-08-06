#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: BFOEngine.py
# @time: 2018/10/29 15:22
# @Software: PyCharm


import numpy as np
from slapy.swarm.bfo import Bacterial
from slapy.swarm.util import Engine
from copy import deepcopy
import matplotlib.pyplot as plt
import copy

npa = np.array
npr = np.random

class BFOEngine(Engine):
    """
    The class for baterial foraging optimization algorithm
    """
    def __init__(self, population_size=100, steps=100, eps=0.01, dim=2, bound=[0, 1], fitness_function=None, *,
                 Nre=20, Nc=10, Ns=4, C=50, ped=0.25, d_attract=0.2, w_attract=0.2, d_repellant=0.2, w_repellant=0.2, init_method='rand', min_fitness_value=-np.inf, agents=None, **kwargs):
        super().__init__(population_size, steps, eps, dim, bound, fitness_function, init_method=init_method,
                         min_fitness_value=min_fitness_value, agents=agents, **kwargs)

        """
        population_size: population population_size
        dim: dimension of variables
        bound: boundaries of variables
        param: algorithm required parameters, it is a list which is consisting of [Ned, Nre, Nc, Ns, C, ped, d_attract, w_attract, d_repellant, w_repellant]
        """
        self.agents = []
        self.gbestPopulation = []
        self.accuFitness = np.zeros(self.population_size)
        self.fitness_value = np.zeros(self.population_size)
        # self.trace = np.zeros(
        #     (self.params[0] * self.Nre * self.Nc, 2))
        self.Nre, self.Nc, self.Ns, self.C, self.ped, self.d_attract, self.w_attract, self.d_repellant, self.w_repellant = Nre, Nc, Ns, C, ped, d_attract, w_attract, d_repellant, w_repellant
        self.best = []
        self.mean = []
        self.max = []
    def initialize(self):
        """
        initialize the population
        """
        for i in range(0, self.population_size):
            ind = Bacterial(**self.__dict__)
            # ind.generate()
            self.agents.append(ind)
        self.evaluate()
        bestIndex = np.argmax(self.fitness_value)
        self.gbest = copy.deepcopy(self.agents[bestIndex])
    def evaluate(self):
        """
        evaluation of the population fitnesses
        """
        self.fitness_value = npa(self.fitness())

    def sortPopulation(self):
        """
        sort population according descending order
        """
        self.agents.sort(reverse=True)

    def update(self):
        """
        evolution process of baterial clony foraging algorithm
        """
        for j in range(0, self.Nre):
            for k in range(0, self.Nc):
                self.chemotaxls()
                self.evaluate()
                bestIndex = np.argmax(self.fitness_value)
                best = copy.deepcopy(self.fitness_value[bestIndex])
                if best > self.gbest.fitness_value:
                    self.gbest = copy.deepcopy(self.agents[bestIndex])
                self.avefitness = np.mean(self.fitness_value)
                self.max.append(best)
                self.best.append(self.gbest.fitness_value)
                self.mean.append(self.avefitness)
            self.reproduction()
        self.eliminationAndDispersal()

    def chemotaxls(self):
        """
        chemotaxls behavior of baterials
        """
        for i in range(0, self.population_size):
            tmpInd = copy.deepcopy(self.agents[i])
            self.fitness_value[i] += self.communication(tmpInd)
            Jlast = self.fitness_value[i]
            rnd = npr.uniform(low=-1, high=1.0, size=self.dim)
            phi = rnd / np.linalg.norm(rnd)
            tmpInd.chromosome += self.C * phi
            tmpInd.transboundary()
            tmpInd.fitness()
            m = 0
            while m < self.Ns:
                if tmpInd.fitness_value > Jlast:
                    Jlast = tmpInd.fitness_value
                    self.agents[i] = copy.deepcopy(tmpInd)
                    # print m, Jlast
                    tmpInd.fitness_value += self.communication(tmpInd)
                    tmpInd.chromosome += self.C * phi
                    tmpInd.transboundary()
                    tmpInd.fitness()
                    m += 1
                else:
                    break
            self.fitness_value[i] = Jlast
            self.accuFitness[i] += Jlast

    def communication(self, ind):
        """
        cell to cell communication
        """
        terms = npa([np.sum((ind.chromosome - agent.chromosome) ** 2) for agent in self.agents])
        terms1 = self.d_attract * np.exp(-1 * self.w_attract * terms)
        terms2 = self.d_repellant * np.exp(-1 * self.w_repellant * terms)
        Jcc = np.sum(terms2) - np.sum(terms1)
        return Jcc

    def reproduction(self):
        """
        reproduction of baterials
        """
        self.sortPopulation()
        self.agents[self.population_size // 2:] = self.agents[:self.population_size // 2]

    def eliminationAndDispersal(self):
        """
        elimination and dispersal of baterials
        """
        rnd = npr.random(self.population_size)
        ind = np.where(rnd < self.ped)[0]
        params = deepcopy(self.__dict__)
        params.pop('init_method')
        for each in ind:
            self.agents[each] = Bacterial(init_method='random', **params)

    def analysis(self):
        """
        plot the result of the baterial clony foraging algorithm
        """
        print("Optimal solution is:")
        print(self.gbest.chromosome)
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
