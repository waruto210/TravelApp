import random
import sys
import numpy as np


class TabuSearch:
    def __init__(self, adj_matrix: list, from_to: list, depart_time: int, time_limit: int,
                 routes_count: list, max_iteration: int = 1, candidates_num: int = 200,
                 tabu_length: int = 2, route_length: int = 4, vehicle: str = ''):
        """

        :param adj_matrix: 临街矩阵
        :param from_to: 起点终点
        :param depart_time: 最早出发时间
        :param time_limit: 时间限制
        :param routes_count: 城市间路径数量
        :param max_iteration: 最大迭代次数
        :param candidates_num: 候选集大小
        :param tabu_length: 禁忌表长度
        :param route_length: 路径长度
        """
        self.iteration = 0
        self.max_iteration = max_iteration
        self.candidates_num = candidates_num
        self.tabu_length = tabu_length
        self.route_length = route_length
        self.from_to = from_to
        self.adj_matrix = list(adj_matrix)
        self.depart_time = depart_time
        self.time_limit = time_limit
        self.routes_count = routes_count
        self.vehicle = vehicle

        # 记录开销最小的路线
        self.best_cities = []
        self.best_routes = []
        self.best_score = sys.maxsize
        # 记录禁忌搜索算法当前路线
        self.cities_now = []
        self.routes_now = []
        # 禁忌表
        self.tabu_list = []
        # 候选集
        self.candidates_list = [tuple] * candidates_num
        self.scores = [int] * candidates_num
        # 初始化线路
        self.init()

    def init(self):
        start: int = self.from_to[0]
        destination: int = self.from_to[1]
        # 先加入起点终点
        self.cities_now.append(start)
        self.cities_now.append(destination)
        # 生成途径城市
        for i in range(self.route_length - 1):
            while True:
                city = random.randint(0, 30)
                # 城市必须重复且城市间必须有路线
                if (city not in self.cities_now) and (self.routes_count[self.cities_now[0]][city] > 0) and \
                        (self.routes_count[city][self.cities_now[1]] > 0):
                    self.cities_now.insert(1, city)
                    break
        # 生成城市间路线序号
        for i in range(self.route_length):
            f = self.cities_now[i]
            t = self.cities_now[i + 1]
            # print("f: " + str(f) + " t: " + str(t))
            # print(routes_count[f][t])
            low, high = self.low_high(f, t)
            if low == high:
                route_num = low
            else:
                route_num: int = random.randint(low, high)
            self.routes_now.append(route_num)
        # 初始化最优路线，防止最优路线没有更新过，返回空值
        self.best_cities = list(self.cities_now)
        self.best_routes = list(self.routes_now)

    def low_high(self, f: int, t: int):
        """
        用于计算起点，终点间在指定交通方式下的路径序号范围
        :param f: 起点
        :param t: 终点
        :return: 路径序号范围,low, high
        """
        # 获取火车和飞机线路
        train_routes = self.adj_matrix[f][t]['train']
        air_routes = self.adj_matrix[f][t]['air']

        if self.vehicle == '':
            low = 0
            high = self.routes_count[f][t] - 1
        elif self.vehicle == 'train':
            low = 0
            high = len(train_routes) - 1
        elif self.vehicle == 'air':
            low = len(train_routes)
            high = len(train_routes) + len(air_routes) - 1
        else:
            low = len(train_routes) + len(air_routes)
            high = self.routes_count[f][t] - 1
        # 无法满足交通工具要求，则取消交通工具要求
        if high < low:
            low = 0
            high = self.routes_count[f][t] - 1
        return low, high

    def generate_candi(self):
        """
        生成候选集
        """
        for i in range(self.candidates_num):
            cities = list(self.cities_now)
            routes = list(self.routes_now)
            # 城市及线路序号变换
            if self.iteration < self.max_iteration * 0.66 and self.route_length > 1:
                pos: int = random.randint(1, self.route_length - 1)
                f = cities[pos - 1]
                t = cities[pos + 1]
                # 随机产生新城市
                while True:
                    city = random.randint(0, 30)
                    if city not in cities and self.routes_count[f][city] > 0 \
                            and self.routes_count[city][t] > 0:
                        break
                cities[pos] = city
                # 随机生成城市间线路序号
                low1, high1 = self.low_high(f, city)
                if low1 == high1:
                    routes[pos - 1] = low1
                else:
                    # print("low1 ", low1, "high1 ", high1)
                    routes[pos - 1] = random.randint(low1, high1)
                low2, high2 = self.low_high(city, t)
                if low2 == high2:
                    routes[pos] = low2
                else:
                    routes[pos] = random.randint(low2, high2)
            # 城市间线路序号变换
            else:
                if self.route_length > 1:
                    pos = random.randint(0, self.route_length - 1)
                else:
                    pos = 0
                f = self.cities_now[pos]
                t = self.cities_now[pos + 1]
                low, high = self.low_high(f, t)
                if low == high:
                    routes[pos] = low
                else:
                    routes[pos] = random.randint(low, high)
            self.candidates_list[i] = (cities, routes)

    def cal_score(self, cities: list, routes: list):
        """
        计算某路线分数，低于时间限制为费用，高于时间限制为sys.maxsize
        :param cities: 经过的城市
        :param routes: 城市间线路序号
        :return: 返回分数
        """
        # print(cities, routes_)
        time_cost: int = 0
        money_cost: int = 0
        go_time = self.depart_time
        for i in range(self.route_length):
            f = cities[i]
            t = cities[i + 1]
            route_num = routes[i]
            real_routes: dict = self.adj_matrix[f][t]
            train: list = real_routes['train']
            air: list = real_routes['air']
            bullet: list = real_routes['bullet']
            # print("Routes_count: " + str(self.routes_conut[f][t]) + "route_num: " + str(route_num))
            
            # 确定路径序号所属交通工具
            if route_num < len(train):
                one_route: dict = train[route_num]
            elif len(train) <= route_num < len(train) + len(air):
                route_num = route_num - len(train)
                one_route: dict = air[route_num]
            else:
                route_num = route_num - (len(train) + len(air))
                # print(route_num)
                one_route: dict = bullet[route_num]
            # 计算时间,费用
            d_time = one_route['depart_time']
            l_time = one_route['length_time']
            if d_time >= go_time:
                cost = d_time + l_time - go_time
            else:
                cost = d_time + l_time + (24 - go_time)
            go_time = (go_time + cost) % 24
            time_cost = time_cost + cost
            money_cost += one_route['price']
        if time_cost > self.time_limit:
            # print("too big")
            score = sys.maxsize
        else:
            score = money_cost
        return score

    def mov(self):
        """
        禁忌搜索算法运行
        """
        # 生成候选集
        self.generate_candi()
        # 计算候选集分数
        for i in range(self.candidates_num):
            cities, routes = self.candidates_list[i]
            self.scores[i] = self.cal_score(cities, routes)
        # 对分数索引排序,升序
        sorted_scores_index = np.argsort(self.scores)
        # print(self.scores)
        # print(sorted_scores_index)
        for i in range(self.candidates_num):
            # 候选者不在禁忌表中
            if self.candidates_list[sorted_scores_index[i]] not in self.tabu_list:
                # 如果分数更优,更新当前最优分数,线路.
                if self.scores[sorted_scores_index[i]] < self.best_score:
                    self.best_score = self.scores[sorted_scores_index[i]]
                    self.best_cities = list(self.candidates_list[sorted_scores_index[i]][0])
                    self.best_routes = list(self.candidates_list[sorted_scores_index[i]][1])
                # 用不在禁忌表中的分数最优线路更新当前线路
                self.cities_now = list(self.candidates_list[sorted_scores_index[i]][0])
                self.routes_now = list(self.candidates_list[sorted_scores_index[i]][1])
                self.tabu_list.append(self.candidates_list[sorted_scores_index[i]])
                if len(self.tabu_list) > self.tabu_length:
                    del self.tabu_list[0]
                break
        # 迭代次数加1
        self.iteration += 1

    def go(self):
        for i in range(self.max_iteration):
            self.mov()
            # print('------after iteration ', i, ', the best score is ', self.best_score)
        return self.best_score, self.best_cities, self.best_routes
