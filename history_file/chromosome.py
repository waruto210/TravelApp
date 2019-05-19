import random as rd


class Chromosome:
    def __init__(self, start: int, des: int, route_length: int, routes_count: list):
        self.route_length = route_length
        self.cities: list = []
        self.routes: list = []
        self.fitness = 0
        self.start = start
        self.des = des
        self.routes_conut = routes_count
        # 随机生成中间城市
        self.cities.append(start)
        self.cities.append(des)
        for i in range(route_length - 1):
            while True:
                city = rd.randint(0, 30)
                if (city not in self.cities) and (routes_count[self.cities[0]][city] > 0) and \
                        (routes_count[city][self.cities[1]] > 0):
                    self.cities.insert(1, city)
                    break
        for i in range(route_length):
            f = self.cities[i]
            t = self.cities[i + 1]
            # print("f: " + str(f) + " t: " + str(t))
            # print(routes_count[f][t])
            route_num: int = rd.randint(0, routes_count[f][t] - 1)
            self.routes.append(route_num)

    def cal_fitness(self, adj_matrix: list, depart_time: int, time_limit: int):
        total_cost: int = 0
        go_time = depart_time
        for i in range(self.route_length):
            f = self.cities[i]
            t = self.cities[i + 1]
            route_num = self.routes[i]
            routes: dict = adj_matrix[f][t]
            train: list = routes['train']
            air: list = routes['air']
            # print("Routes_count: " + str(self.routes_conut[f][t]) + "route_num: " + str(route_num))
            if route_num >= len(train):
                route_num = route_num - len(train)
                r: dict = air[route_num]
            else:
                r: dict = train[route_num]
            d_time = r['depart_time']
            l_time = r['length_time']
            if d_time >= go_time:
                cost = d_time + l_time - go_time
            else:
                cost = d_time + l_time + (24 - go_time)
            go_time = (go_time + cost) % 24
            total_cost = total_cost + cost

        if total_cost > time_limit:
            fitness = 0.001
        else:
            fitness = 10000. / total_cost
        self.fitness = fitness
        return fitness

    # 城市和路线变异
    def mutate1(self, routes_count: list):
        # print("mutate1")
        pos: int = rd.randint(1, self.route_length - 1)
        f = self.cities[pos - 1]
        t = self.cities[pos + 1]

        while True:
            city = rd.randint(0, 30)
            if city not in self.cities and routes_count[f][city] > 0 and routes_count[city][t] > 0:
                break
        self.cities[pos] = city

        self.routes[pos - 1] = rd.randint(0, routes_count[f][city] - 1)
        self.routes[pos] = rd.randint(0, routes_count[city][t] - 1)

    def mutate2(self, routes_count: list):
        pos: int = rd.randint(0, self.route_length - 1)
        f = self.cities[pos]
        t = self.cities[pos + 1]
        while True:
            r_num: int = rd.randint(0, routes_count[f][t] - 1)
            if r_num != self.routes[pos]:
                break
        self.routes[pos] = r_num
