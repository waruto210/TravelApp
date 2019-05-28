from tabu import TabuSearch
from label import label
import numpy as np
from routes import TravelRoute


class TabuAlgorithm:
    def __init__(self, adj_matrix):
        self.adj_matrix = list(adj_matrix)

    def cal_routes_count(self):
        """
        计算adj_matrix的所有邻接点之间的路径数量
        :return: ret[i][j]表城市i到j的线路数量
        """
        ret: list = []
        for index in range(31):
            ret.append([])

        for index in range(31):
            for j in range(31):
                route = self.adj_matrix[index][j]
                train: list = route['train']
                air: list = route['air']
                bullet: list = route['bullet']
                ret[index].append(len(train) + len(air) + len(bullet))
        return ret
    
    def search_by_tabu(self, from_to: list, depart_time: int, time_limit: int, vehicle: str = '') -> tuple:
        """
        禁忌搜索算法分别搜索长度为1, 2, 3的路
        :param from_to: 起点, 终点
        :param depart_time: 最早出发时间
        :param time_limit: 时间限制
        :param vehicle: 优先交通工具
        :return: 最优路径及其价格开销
        """
        # 禁忌搜索参数
        max_iteration: int = 200
        candidates_num: int = 20
        tabu_length: int = 15
        # 计算路线数
        routes_count = self.cal_routes_count()
        # 起点终点
        from_to = [label[from_to[0]], label[from_to[1]]]
        # 分别记录开销,经过城市,城市间路线序号,最终结果
        scores = []
        pass_cities = []
        routes_num = []
        result = []
        for route_length in range(1, 4):
            search = TabuSearch(adj_matrix=self.adj_matrix, from_to=from_to, depart_time=depart_time,
                                time_limit=time_limit, routes_count=routes_count,
                                max_iteration=max_iteration, candidates_num=candidates_num,
                                tabu_length=tabu_length, route_length=route_length, vehicle=vehicle)
            a, b, c = search.go()
            scores.append(a)
            pass_cities.append(b)
            routes_num.append(c)
        # 对开销排序,取开销最小的线路方案
        sorted_scores_index = np.argsort(scores)
        from_to = pass_cities[sorted_scores_index[0]]
        routes = routes_num[sorted_scores_index[0]]
        # 获取最优路径的长度
        route_l = sorted_scores_index[0] + 1

        for i in range(route_l):
            f = from_to[i]
            t = from_to[i + 1]
            route_num = routes[i]
            real_routes: dict = self.adj_matrix[f][t]
            train: list = real_routes['train']
            air: list = real_routes['air']
            bullet: list = real_routes['bullet']
            # 找到路径序号对应的真实路径
            if route_num < len(train):
                one_route: dict = train[route_num]
            elif len(train) <= route_num < len(train) + len(air):
                route_num = route_num - len(train)
                one_route: dict = air[route_num]
            else:
                route_num = route_num - len(train) - len(air)
                one_route: dict = bullet[route_num]
            # 生成路径对象
            code: str = one_route['number']
            price: int = one_route['price']
            des: str = one_route['to']
            depart_time: int = one_route['depart_time']
            duration: int = one_route['length_time']
            by: str = one_route['type']
            seg = TravelRoute(by=by, code=code, price=price, des=des, depart_time=depart_time, duration=duration)
            result.append(seg)
        return result, np.min(scores)
