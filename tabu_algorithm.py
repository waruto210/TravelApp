from tabu import TabuSearch
from label import label
import numpy as np
from routes import TravelRoute


class TabuAlgorithm:
    def __init__(self, adj_matrix):
        self.adj_matrix = list(adj_matrix)

    def cal_routes_count(self):
        """

        :return:
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

        :param from_to:
        :param depart_time:
        :param time_limit:
        :param vehicle:
        :return:
        """
        # 禁忌搜索参数
        max_iteration: int = 200
        candidates_num: int = 20
        tabu_length: int = 15

        routes_count = self.cal_routes_count()
        from_to = [label[from_to[0]], label[from_to[1]]]
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
        sorted_scores_index = np.argsort(scores)
        from_to = pass_cities[sorted_scores_index[0]]
        routes = routes_num[sorted_scores_index[0]]
    
        route_l = sorted_scores_index[0] + 1
        for i in range(route_l):
            f = from_to[i]
            t = from_to[i + 1]
            route_num = routes[i]
            real_routes: dict = self.adj_matrix[f][t]
            train: list = real_routes['train']
            air: list = real_routes['air']
            bullet: list = real_routes['bullet']
            if route_num < len(train):
                one_route: dict = train[route_num]
            elif len(train) <= route_num < len(train) + len(air):
                route_num = route_num - len(train)
                one_route: dict = air[route_num]
            else:
                route_num = route_num - len(train) - len(air)
                one_route: dict = bullet[route_num]
            code: str = one_route['number']
            price: int = one_route['price']
            des: str = one_route['to']
            depart_time: int = one_route['depart_time']
            duration: int = one_route['length_time']
            by: str = one_route['type']
            seg = TravelRoute(by=by, code=code, price=price, des=des, depart_time=depart_time, duration=duration)
            result.append(seg)
        return result, np.min(scores)
