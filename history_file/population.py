from history_file.chromosome import Chromosome
from label import label
import random as rd
import copy


class Population:
    def __init__(self, adj_matrix: list, cities: list, depart_time: int, time_limit: int, routes_count: list,
                 route_length: int = 4, pop_size: int = 100, p_mutation: float = 0.8):
        """
        :param cities:
        :param routes_count:
        :param route_length:
        :param pop_size:
        :param p_mutation:
        """
        self.adj_matrix = adj_matrix
        self.depart_time = depart_time
        self.time_limit = time_limit
        self.cities = cities
        self.routes_count: list = routes_count
        self.p_mutation: float = p_mutation
        self.route_length: int = route_length
        self.pop_size: int = pop_size
        self.pop: list = self.init_pop()

    def init_pop(self):
        start: int = label[self.cities[0]]
        des: int = label[self.cities[1]]
        pop: list = []
        for i in range(self.pop_size):
            new_chromosome: Chromosome = Chromosome(start=start, des=des, route_length=self.route_length, routes_count=self.routes_count)
            pop.append(new_chromosome)
        for i in range(self.pop_size):
            pop[i].cal_fitness(adj_matrix=self.adj_matrix, depart_time=self.depart_time, time_limit=self.time_limit)
        return pop

    def mutation(self, age: int):
        if age < 30:
            for i in range(1, self.pop_size):
                pro = rd.random()
                if pro < self.p_mutation:
                    self.pop[i].mutate1(routes_count=self.routes_count)
                    self.pop[i].cal_fitness(adj_matrix=self.adj_matrix, depart_time=self.depart_time, time_limit=self.time_limit)
        else:
            for i in range(1, self.pop_size):
                pro = rd.random()
                if pro < self.p_mutation:
                    self.pop[i].mutate2(routes_count=self.routes_count)
                    self.pop[i].cal_fitness(adj_matrix=self.adj_matrix, depart_time=self.depart_time, time_limit=self.time_limit)

    def selection(self):
        all_fitness: list = [float] * self.pop_size
        acc_fitness: list = [float] * self.pop_size
        sum_fit: float
        for i in range(self.pop_size):
            all_fitness[i] = self.pop[i].fitness
            if i == 0:
                sum_fit = all_fitness[i]
            else:
                sum_fit = sum_fit + all_fitness[i]
        for i in range(self.pop_size):
            if i == 0:
                acc_fitness[i] = all_fitness[i] / sum_fit
            else:
                acc_fitness[i] = (all_fitness[i] / sum_fit) + acc_fitness[i - 1]

        self.pop[0] = self.get_best()
        for i in range(1, self.pop_size):
            pro = rd.random()
            # print("Pro: " + str(pro))
            for j in range(self.pop_size):
                if pro <= acc_fitness[j]:
                    for k in range(1, self.route_length):
                        self.pop[i].cities[k] = self.pop[j].cities[k]
                    for k in range(self.route_length):
                        self.pop[i].routes[k] = self.pop[j].routes[k]
                    self.pop[i].fitness = self.pop[j].fitness

    def get_best(self):
        best_index: int = 0
        best_fit = -1
        for i in range(self.pop_size):
            if self.pop[i].fitness > best_fit:
                best_fit = self.pop[i].fitness
                best_index = i
        ret = copy.deepcopy(self.pop[best_index])
        return ret
