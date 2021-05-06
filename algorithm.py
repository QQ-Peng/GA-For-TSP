# _*_ coding: utf-8 _*_
# Date: 2021-5-1
# Author: Qianqian Peng
# Reference: Genetic Algorithm for Traveling Salesman Problem with Modified Cycle Crossover Operator

import random
import copy
import numpy as np
from cross import *


def init_population(cn: int, ps: int, uniq=True):
    '''
    :param cn: city number
    :param ps: population size
    :param uniq: Whether duplicate individuals are allowed to be produced
    '''
    Population = []
    base = list(range(cn))
    while len(Population) < ps:
        random.shuffle(base)
        if uniq:
            if base not in Population:
                Population.append(copy.deepcopy(base))
        else:
            Population.append(copy.deepcopy(base))
    return Population


def cal_distance(distance_matrix, city1: int, city2: int):
    return distance_matrix[city1][city2]


def cal_fitness(path, distance_matrix):
    if type(path[0]) is int:
        dis = 0
        for i in range(0, len(path) - 1):
            dis += cal_distance(distance_matrix, path[i], path[i + 1])
        dis += cal_distance(distance_matrix, path[-1], path[0])
        return 1 / dis
    if type(path[0]) is list:
        all_fitness = []
        for one_path in path:
            dis = 0
            for i in range(0, len(one_path) - 1):
                dis += cal_distance(distance_matrix, one_path[i], one_path[i + 1])
            dis += cal_distance(distance_matrix, one_path[-1], one_path[0])
            all_fitness.append(1 / dis)
        return all_fitness

def randIdx(minIdx, maxIdx, num=2, uniq=True):
    '''
    :param minIdx:
    :param maxIdx:
    :param num: 1 or 2
    :return:
    '''
    if num == 1:
        return random.randint(minIdx,maxIdx)
    elif num == 2:
        choice1 = random.randint(minIdx, maxIdx)
        choice2 = random.randint(minIdx, maxIdx)
        if uniq:
            while choice1 == choice2:
                choice2 = random.randint(minIdx, maxIdx)
        return choice1, choice2
    else:
        raise ValueError("the index number must be 1 or 2")

def selection_reproduction(population, fitness, ps):
    # print("in selection")
    # print("population size: {}".format(len(population)))
    population_next = []
    population_size = len(population)
    n = 0
    while n < population_size / 2:
        choice1, choice2 = randIdx(0,population_size - 1)
        p = random.random()
        if p < ps:
            choice = choice1 if fitness[choice1] > fitness[choice2] else choice2
        else:
            choice = choice1 if fitness[choice1] < fitness[choice2] else choice2
        if population[choice] not in population_next:
            population_next.append(population[choice])
            n += 1
    # print("population size: {}".format(len(population_next)))
    return population_next


def crossover(population, crossover_method, min_population_size=20, max_population_size=300):
    # print("*"*20)
    # print("in crossover")
    # print("population size: {}".format(len(population)))
    population_next = []
    not_selected = list(range(len(population)))
    while len(not_selected) > 0:
        choice1 = randIdx(0, len(population) - 1, 1)  # 从整个种群中选择
        choice2 = randIdx(0,len(not_selected) - 1, 1)  # 从还未配对的群体中选择
        while choice1 == not_selected[choice2]:
            choice1 = randIdx(0, len(population) - 1, 1)
        parent_1 = copy.deepcopy(population[choice1])
        parent_2 = copy.deepcopy(population[not_selected[choice2]])
        p = random.random()
        # 控制种群规模，让已经交配过的parent有一定概率再次交配，以免随着代数的增加，规模减小至1
        if p > 0.4:
            not_selected.pop(choice2)
            if choice1 in not_selected:
                not_selected.pop(not_selected.index(choice1))
        offspring1, offspring2 = crossover_method(parent_1, parent_2)
        population_next += [offspring1, offspring2]
    # print("population size: {}".format(len(population_next)))
    while len(population_next) < min_population_size:
        choice1, choice2 = randIdx(0, len(population)-1)
        parent_1 = copy.deepcopy(population[choice1])
        parent_2 = copy.deepcopy(population[choice2])
        offspring1, offspring2 = crossover_method(parent_1, parent_2)
        population_next += [offspring1, offspring2]
    # print("population size: {}".format(len(population_next)))
    # 控制群体规模，防止规模太大
    if len(population_next) > max_population_size:
        step = int(len(population_next)/max_population_size)
        population_next2 = []
        i = 0
        while i < len(population_next):
            population_next2.append(population_next[i])
            i += step
        population_next = population_next2
    # print("population size: {}".format(len(population_next)))
    # print("*" * 20)
    return population_next


def mutation(population, pm):
    # print("in mutation")
    # print("population size: {}".format(len(population)))
    population_next = []
    for i in range(len(population)):
        p = random.random()
        if p < pm:
            parent = population[i]
            mut_pos1, mut_pos2 = randIdx(0,len(parent) - 1)
            tem = parent[mut_pos1]
            parent[mut_pos1] = parent[mut_pos2]
            parent[mut_pos2] = tem
            population_next.append(parent)
        else:
            population_next.append(population[i])
    # print("population size: {}".format(len(population_next)))
    return population_next


def generation_iter(population, distance_matrix, pm, ps, cross_mh, max_generation,min_population_size=20,max_population_size=300):
    min_len = []
    for _ in range(max_generation):
        fitness = cal_fitness(population, distance_matrix)
        min_len.append(int(1 / max(fitness)))
        population = selection_reproduction(population, fitness, ps)
        population = crossover(population, cross_mh.cross,min_population_size,max_population_size)
        population = mutation(population, pm)

    return min(min_len)


if __name__ == "__main__":
    city_num = 7
    population_size = 30
    min_population_size = 20
    max_population_size = 300
    max_generation = 10
    optimal_value = 159
    runs = 30
    pm = 0.1
    ps = 0.8
    cities = [0, 1, 2, 3, 4, 5, 6]
    distance = [[0, 34, 36, 37, 31, 33, 35],
                [34, 0, 29, 23, 22, 25, 24],
                [36, 29, 0, 17, 12, 18, 17],
                [37, 23, 17, 0, 32, 30, 29],
                [31, 22, 12, 32, 0, 26, 24],
                [33, 25, 18, 30, 26, 0, 19],
                [35, 24, 17, 29, 24, 19, 0]]

    cross_mh_pmx = PMX()
    cross_mh_ox = OX()
    cross_mh_cx2 = CX2()
    all_min_pmx = []
    all_min_ox = []
    all_min_cx2 = []
    for _ in range(runs):
        min_len = []
        population_pmx = init_population(city_num, population_size)
        population_ox = copy.deepcopy(population_pmx)
        population_cx2 = copy.deepcopy(population_pmx)
        min_len_pmx = generation_iter(population_pmx, distance, pm, ps, cross_mh_pmx, max_generation, min_population_size, max_population_size)
        min_len_ox = generation_iter(population_ox, distance, pm, ps, cross_mh_ox, max_generation, min_population_size, max_population_size)
        min_len_cx2 = generation_iter(population_cx2, distance, pm, ps, cross_mh_cx2, max_generation, min_population_size, max_population_size)
        all_min_pmx.append(min_len_pmx)
        all_min_ox.append(min_len_ox)
        all_min_cx2.append(min_len_cx2)
    print("*" * 10, "mean value", "*" * 10)
    print("pmx: {}".format(np.mean(np.array(all_min_pmx))))
    print("ox: {}".format(np.mean(np.array(all_min_ox))))
    print("cx2: {}".format(np.mean(np.array(all_min_cx2))))
    print("*" * 10, "max value", "*" * 10)
    print("pmx: {}".format(max(all_min_pmx)))
    print("ox: {}".format(max(all_min_ox)))
    print("cx2: {}".format(max(all_min_cx2)))
    print("*" * 10, "best value number", "*" * 10)
    print("pmx: {}/{}".format(all_min_pmx.count(optimal_value), len(all_min_pmx)))
    print("ox: {}/{}".format(all_min_ox.count(optimal_value), len(all_min_ox)))
    print("cx2: {}/{}".format(all_min_cx2.count(optimal_value), len(all_min_cx2)))

    # min_path = 100000000
    # n = 0
    # for i in range(7):
    #     # cur_len = 0
    #     for j in range(7):
    #         if j in [i]:
    #             continue
    #         else:
    #             for a in range(7):
    #                 a = 6 - a
    #                 if a in [i, j]:
    #                     continue
    #                 else:
    #                     for b in range(7):
    #                         if b in [i, j, a]:
    #                             continue
    #                         else:
    #                             for c in range(7):
    #                                 if c in [i, j, a, b]:
    #                                     continue
    #                                 else:
    #                                     for d in range(7):
    #                                         if d in [i, j, a, b, c]:
    #                                             continue
    #                                         else:
    #                                             for e in range(7):
    #                                                 n += 1
    #                                                 if e in [i, j, a, b, c, d]:
    #                                                     continue
    #                                                 else:
    #                                                     cur_len = distance[i][j] + distance[j][a] + distance[a][b] + \
    #                                                               distance[b][c] + distance[c][d] + distance[d][e]
    #                                                     cur_len += distance[i if i <= e else e][e if e > i else i]
    #                                                     if cur_len < min_path:
    #                                                         min_path = cur_len
    #                                                         print(i, "->", j, "->", a, "->", b, "->", c, "->", d, "->",
    #                                                               e)
    #                                                         print(min_path)
