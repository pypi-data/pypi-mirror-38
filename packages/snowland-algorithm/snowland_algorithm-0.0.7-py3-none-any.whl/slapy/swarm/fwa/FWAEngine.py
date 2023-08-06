#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: FWAEngine.py
# @time: 2018/9/26 3:33
# @Software: PyCharm

from scipy.spatial.distance import pdist, squareform
from slapy.swarm.util.Engine import Engine
from slapy.swarm.fwa.Firework import Firework
import numpy as np
from copy import deepcopy
from matplotlib import pylab as plt

npr = np.random
npa = np.array


class FWAEngine(Engine):
    def __init__(self, population_size=10, steps=100, eps=0.01, dim=2, bound=[0, 1], fitness_function=None, *,
                 init_method='rand', min_fitness_value=-np.inf, agents=None,
                 coef_explosion_amplitude=40, max_sparks_num=40, min_sparks_num=2, coef_spark_num=50,
                 gaussian_number=10, transboundary_rules='mod', **kwargs):
        super().__init__(population_size, steps, eps, dim, bound, fitness_function, init_method=init_method,
                         min_fitness_value=min_fitness_value, agents=agents, transboundary_rules=transboundary_rules,
                         **kwargs)
        #
        # self.total_fiteval_times = total_fiteval_times
        self.coef_explosion_amplitude = coef_explosion_amplitude
        self.max_sparks_num = max_sparks_num
        self.min_sparks_num = min_sparks_num
        self.coef_spark_num = coef_spark_num
        self.total_fiteval_times = 0
        self.gaussian_number = gaussian_number
        self.seed_gaussian_agents = []

    def fitness(self, *args, **kwargs):
        return super().fitness(*args, **kwargs)

    def minimize(self, fn):
        return super().minimize(fn)

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        if self.agents is None: self.agents = [Firework(**(self.__dict__)) for _ in range(self.population_size)]
        self.gbest = self.agents[0]
        self.mean = []
        self.best = []
        self.max = []
        self.total_fiteval_times = 0

    def update(self, *args, **kwargs):
        self._sonsnum_cal()
        self._scope_cal()
        # generate the sparks, based on the sparks number and explosion amplitude of each firework
        self._sons_generate()
        # perform the gaussian mutation of seeds
        self._seed_gauss_mutation()  # all the seeds
        # select the next iteration
        self._select_next_iteration_on_entropy()

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
        plt.title("FWA for function optimization")
        plt.legend()
        plt.show()
        print(self.gbest)

    def record(self, *args, **kwargs):
        super().record(*args, **kwargs)
        fitness_list = npa([each.fitness() for each in self.agents])
        self.mean.append(np.mean(fitness_list))
        self.max.append(np.max(fitness_list))
        self.best.append(np.max(self.max))


    def _sonsnum_cal(self):
        """
        确定烟花数量
        :return:
        """
        fitness_array = npa([each.fitness() for each in self.agents])
        fitness_sub_max = np.max(fitness_array, axis=0) - fitness_array
        fitness_sub_max_sum = np.sum(fitness_sub_max)
        sonnum_temp = (fitness_sub_max + self.eps) / (fitness_sub_max_sum + self.eps)
        sonnum_temp = np.round(sonnum_temp * self.coef_spark_num).astype(np.int32)
        ind_low = sonnum_temp < self.min_sparks_num
        sonnum_temp[ind_low] = self.min_sparks_num
        ind_high = sonnum_temp > self.max_sparks_num
        sonnum_temp[ind_high] = self.max_sparks_num
        for ind, _ in enumerate(self.agents):
            self.agents[ind].son_number = sonnum_temp[ind]

    def _scope_cal(self):
        """
        通过范围确定烟花数量
        :return:
        """
        fitness_array = self.fitness()
        fitness_sub_best = np.abs(np.min(fitness_array, axis=0) - fitness_array)
        fitness_sub_best_sum = np.sum(fitness_sub_best)
        scope_array = self.coef_explosion_amplitude * (fitness_sub_best + self.eps) / (fitness_sub_best_sum + self.eps)
        ind_low = scope_array < self.min_sparks_num
        scope_array[ind_low] = self.min_sparks_num
        ind_high = scope_array > self.max_sparks_num
        scope_array[ind_high] = self.max_sparks_num
        for ind, _ in enumerate(self.agents):
            self.agents[ind].scope = scope_array[ind]

    def _sons_generate(self):
        """
        生成烟花
        :return:
        """
        for i, agent in enumerate(self.agents):
            self.agents[i].sons = [deepcopy(agent) for _ in range(agent.son_number)]
            for j, _ in enumerate(agent.sons):
                # dimens_select = npr.randint(0, 2, self.dim, dtype=bool)  # select dimens_select
                dimens_select = np.ones(self.dim, dtype=bool)  # select dimens_select
                offset = (npr.rand(self.dim)[dimens_select] * 2 - 1) * agent.scope  # Calculate the displacement:
                self.agents[i].sons[j].chromosome[dimens_select] += offset
                # ind = np.any(self.bound[:, 0] < son.chromosome < self.bound[:, 1])
                self.agents[i].sons[j].transboundary()

    def _seed_gauss_mutation(self):
        """
        通过高斯生成烟花
        :return:
        """
        gaussian_number = self.gaussian_number
        if gaussian_number > self.population_size:
            raise ValueError('gaussian_number should lower than population_size')
        self.seed_gaussian_agents = npr.choice(self.agents, gaussian_number, replace=False)
        for ind, agent in enumerate(self.seed_gaussian_agents):
            coef_gaussian = npr.normal(1, 1, (gaussian_number, self.dim))
            # dim_mutation = npr.randint(0, 2, self.dim, dtype=bool)
            dim_mutation = np.ones(self.dim, dtype=bool)
            self.seed_gaussian_agents[ind].chromosome[dim_mutation] *= coef_gaussian[ind][dim_mutation]
            self.seed_gaussian_agents[ind].transboundary()

    def _select_next_iteration_on_entropy(self):
        """
        筛选
        :return:
        """
        all_agents = deepcopy(self.agents)
        sons = []
        [sons.extend(agent.sons) for agent in self.agents]
        all_agents.extend(sons)
        # [all_agents.extend(agent.sons) for agent in self.agents]
        all_agents.extend(self.seed_gaussian_agents)

        # ax = plt.subplot(111)
        # [plt.plot(each.chromosome[0], each.chromosome[1], 'g*') for each in sons]
        # [plt.plot(each.chromosome[0], each.chromosome[1], 'b*') for each in self.seed_gaussian_agents]
        # [plt.plot(each.chromosome[0], each.chromosome[1], 'r*') for each in self.agents]
        # plt.plot(self.gbest.chromosome[0], self.gbest.chromosome[1], 'r+')
        # plt.pause(10)
        # if __debug__:
        plt.clf()
        ax = plt.subplot(111)

        for agent in self.agents:
            color = npr.rand(3)
            plt.plot(agent.chromosome[0], agent.chromosome[1], '>', color=color)
            [plt.plot(son.chromosome[0], son.chromosome[1], '*', color=color) for son in agent.sons]
        [plt.plot(agent.chromosome[0], agent.chromosome[1], 'b*') for agent in self.seed_gaussian_agents]
        plt.plot(self.gbest.chromosome[0], self.gbest.chromosome[1], 'ro')
        plt.pause(0.2)

        seed_fitness = [each.fitness() for each in all_agents]
        best_ind = np.argmax(seed_fitness)
        self.gbest = all_agents[best_ind]

        chromosome_matrix = npa([each.chromosome for each in all_agents])
        norm_matrix = squareform(pdist(chromosome_matrix))

        # compute the sum distance for a spark to others
        distance_array = np.sum(norm_matrix, axis=0)
        sum_distance_array = np.sum(distance_array)

        # probobility computation
        probability_select_particle = distance_array / sum_distance_array
        sum_probability = np.cumsum(probability_select_particle)
        rand = npr.rand(self.population_size)
        self.agents = [all_agents[np.sum(rand[i] > sum_probability)] for i in range(self.population_size)]
        for ind, _ in enumerate(self.agents):
            self.agents[ind].sons = []
            self.agents[ind].seed_gaussian_agents = []
