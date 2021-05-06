# _*_ coding: utf-8 _*_
# Date: 2021-5-1
# Author: Qianqian Peng
# Reference: Genetic Algorithm for Traveling Salesman Problem with Modified Cycle Crossover Operator

import random


class PMX:
    def __init__(self):
        pass

    def cross(self, parent1: list, parent2: list):
        cut_pos1 = random.randint(1, len(parent1) - 3)
        cut_pos2 = random.randint(1, len(parent2) - 2)
        while cut_pos1 >= cut_pos2:
            cut_pos2 = random.randint(1, len(parent2) - 2)
        offspring1 = [-100] * len(parent1)
        offspring2 = [-100] * len(parent2)
        for i in range(cut_pos1, cut_pos2 + 1):
            offspring1[i] = parent2[i]
            offspring2[i] = parent1[i]
        for i in range(len(offspring1)):
            if cut_pos1 <= i <= cut_pos2:
                continue
            if parent1[i] not in offspring1[cut_pos1:cut_pos2 + 1]:
                offspring1[i] = parent1[i]
            if parent2[i] not in offspring2[cut_pos1:cut_pos2 + 1]:
                offspring2[i] = parent2[i]
        for i in range(len(offspring1)):
            if cut_pos1 <= i <= cut_pos2:
                continue
            else:
                if offspring1[i] < 0:
                    self.set_city(offspring1, offspring2, parent1, i)
                if offspring2[i] < 0:
                    self.set_city(offspring2, offspring1, parent2, i)
        return offspring1, offspring2

    def set_city(self, offspring1: list, offspring2: list, parent1: list, pos: int):
        candidate = parent1[pos]
        while candidate in offspring1:
            candidate = offspring2[offspring1.index(candidate)]
        offspring1[pos] = candidate


class OX:
    def __init__(self):
        pass

    def cross(self, parent1: list, parent2: list):
        cut_pos1 = random.randint(1, len(parent1) - 3)
        cut_pos2 = random.randint(1, len(parent2) - 2)
        while cut_pos1 >= cut_pos2:
            cut_pos2 = random.randint(1, len(parent2) - 2)
        offspring1 = [-100] * len(parent1)
        offspring2 = [-100] * len(parent2)
        for i in range(cut_pos1, cut_pos2 + 1):
            offspring1[i] = parent1[i]
            offspring2[i] = parent2[i]
        candidate1 = parent2[cut_pos2 + 1:] + parent2[:cut_pos2 + 1]
        candidate2 = parent1[cut_pos2 + 1:] + parent1[:cut_pos2 + 1]
        self.set_city(candidate1, offspring1, cut_pos2)
        self.set_city(candidate2, offspring2, cut_pos2)
        return offspring1, offspring2

    def set_city(self, candidate: list, offspring: list, cut_pos2):
        cur_pos = (cut_pos2 + 1) % len(offspring)
        for i in range(len(candidate)):
            tem = candidate.pop(0)
            if tem not in offspring:
                offspring[cur_pos] = tem
                cur_pos = (cur_pos + 1) % len(offspring)


class CX2:
    def __init__(self):
        pass

    def cross(self, parent1, parent2):
        final_offspring1 = []
        final_offspring2 = []
        finish_tag = False
        while not finish_tag:
            parent1, parent2, offspring1, offspring2, finish_tag = self.cross_partial(parent1, parent2)
            final_offspring1 += offspring1
            final_offspring2 += offspring2
        return final_offspring1, final_offspring2

    def cross_partial(self, parent1, parent2):
        finish_tag = False
        offspring1 = [-100] * len(parent1)
        offspring2 = [-100] * len(parent2)
        offspring1[0] = parent2[0]
        cur_pos1 = 1
        cur_pos2 = 0
        while cur_pos1 < len(offspring1) or cur_pos2 < len(offspring2):
            if cur_pos2 < cur_pos1:
                candidate = parent2[parent1.index(parent2[parent1.index(offspring1[cur_pos1 - 1])])]
                if candidate not in offspring2:
                    offspring2[cur_pos2] = candidate
                    cur_pos2 += 1
                else:
                    break
            else:
                candidate = parent2[parent1.index(offspring2[cur_pos2 - 1])]
                if candidate not in offspring1:
                    offspring1[cur_pos1] = candidate
                    cur_pos1 += 1
                else:
                    break
        offspring1 = offspring1[:cur_pos1]
        offspring2 = offspring2[:cur_pos2]
        city1_not_in_city2 = list(set(offspring1).difference(set(offspring2)))
        city2_not_in_city1 = list(set(offspring2).difference(set(offspring1)))
        random.shuffle(city1_not_in_city2)
        random.shuffle(city2_not_in_city1)
        offspring1 += city2_not_in_city1
        offspring2 += city1_not_in_city2
        cur_pos1 += len(city2_not_in_city1)
        cur_pos2 += len(city1_not_in_city2)
        if cur_pos1 >= len(parent1) and cur_pos2 >= len(parent2):
            finish_tag = True
        self.pop_exist_city(parent1, offspring2)
        self.pop_exist_city(parent2, offspring1)
        return parent1, parent2, offspring1, offspring2, finish_tag

    def pop_exist_city(self, parent: list, offspring: list):
        for i in range(len(parent)):
            tem = parent.pop(0)
            if tem not in offspring:
                parent.append(tem)
        return parent


if __name__ == "__main__":
    # test PMX
    print("*" * 10, "test PMX:", "*" * 10)
    parent1 = [2, 3, 7, 1, 6, 0, 5, 4]
    parent2 = [3, 1, 4, 0, 5, 7, 2, 6]
    pmx = PMX()
    print("paren1: ", parent1)
    print("parent2: ", parent2)
    print("offspring: ", pmx.cross(parent1, parent2))

    # test OX
    print("*" * 10, "test OX", "*" * 10)
    parent1 = [2, 3, 7, 1, 6, 0, 5, 4]
    parent2 = [3, 1, 4, 0, 5, 7, 2, 6]
    ox = OX()
    print("paren1: ", parent1)
    print("parent2: ", parent2)
    print("offspring: ", ox.cross(parent1, parent2))

    # test CX2
    print("*" * 10, "test CX2", "*" * 10)
    cx2 = CX2()
    parent1 = [2, 3, 7, 1, 6, 0, 5, 4]
    parent2 = [3, 1, 4, 0, 5, 7, 2, 6]
    # print("paren1: ", parent1)
    # print("parent2: ", parent2)
    print("offspring: ", cx2.cross(parent1, parent2))
    parent1 = [0, 1, 2, 3, 4, 5, 6, 7]
    parent2 = [1, 6, 4, 7, 3, 0, 5, 2]
    # parent1 = [6, 3, 4, 5, 0, 1, 2,7]
    # parent2 = [3, 0, 6, 4, 2, 1, 5,7]
    print('\n')
    print("paren1: ", parent1)
    print("parent2: ", parent2)
    # print("*"*20)
    print("offspring: ", cx2.cross(parent1, parent2))
