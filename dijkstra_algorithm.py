from label import label
import sys
from routes import TravelRoute
import numpy as np


class Dijkstra:
    def __init__(self, adj_matrix: list):
        self.adj_matrix = list(adj_matrix)

    @staticmethod
    def cal_weight_by_price(train_route: list, air_route: list, bullet_route: list, vehicle: str = ''):
        """

        :param train_route: 火车线路集合
        :param air_route: 飞机线路集合
        :param bullet_route: 动车线路集合
        :param vehicle: 优先交通工具
        :return: 权最小的线路
        """
        min_price = [sys.maxsize] * 3
        min_dict = [{}] * 3
        # 找到权最小火车班次
        if vehicle == '' or vehicle == 'train':
            for way in train_route:
                price: int = way['price']
                if price < min_price[0]:
                    min_price[0] = price
                    min_dict[0] = way
        # 找到权最小飞机班次
        if vehicle == '' or vehicle == 'air':
            for way in air_route:
                price: int = way['price']
                if price < min_price[1]:
                    min_price[1] = price
                    min_dict[1] = way
        # 找到权最小动车班次
        if vehicle == '' or vehicle == 'bullet':
            for way in bullet_route:
                price: int = way['price']
                if price < min_price[2]:
                    min_price[2] = price
                    min_dict[2] = way
        # 返回二者中小者
        min_index: int = int(np.argmin(min_price))
        return min_dict[min_index], min_price[min_index]

    @staticmethod
    def cal_weight_by_time(d_time: int, train_route: list, air_route: list, bullet_route: list, vehicle: str = ''):
        """
        
        :param d_time: 最早出发时间
        :param train_route: 火车线路集合
        :param air_route: 飞机线路集合
        :param bullet_route: 动车线路集合
        :param vehicle: 优先交通工具
        :return: 权最小的值
        """

        min_time = [sys.maxsize] * 3
        min_dict = [{}] * 3
        # 找到权最小火车班次
        if vehicle == '' or vehicle == 'train':
            for way in train_route:
                depart_time: int = way['depart_time']
                length_time: int = way['length_time']

                if depart_time >= d_time:  # 当天可乘该班次
                    length = length_time + depart_time - d_time
                else:  # 当天不可乘该班次
                    length = length_time + depart_time + (24 - d_time)
                if length < min_time[0]:
                    min_time[0] = length
                    min_dict[0] = way

        # 找到权最小的飞机班次
        if vehicle == '' or vehicle == 'air':
            for way in air_route:
                depart_time: int = way['depart_time']
                length_time: int = way['length_time']
                if depart_time >= d_time:  # 当天可乘该班次
                    length = length_time + depart_time - d_time
                else:  # 当天不可乘该班次
                    length = length_time + depart_time + (24 - d_time)

                if length < min_time[1]:
                    min_time[1] = length
                    min_dict[1] = way

        # 找到权最小的飞机班次
        if vehicle == '' or vehicle == 'bullet':
            for way in bullet_route:
                depart_time: int = way['depart_time']
                length_time: int = way['length_time']
                if depart_time >= d_time:  # 当天可乘该班次
                    length = length_time + depart_time - d_time
                else:  # 当天不可乘该班次
                    length = length_time + depart_time + (24 - d_time)

                if length < min_time[2]:
                    min_time[2] = length
                    min_dict[2] = way
        min_index: int = int(np.argmin(min_time))
        # 返回三者中权小者班次
        return min_dict[min_index], min_time[min_index]

    def search_by_dijkstra(self, mode: str = "best_time", from_to: list = [],
                           depart_time: int = 10, vehicle: str = '') -> tuple:
        """
        根据模式返回两地最优线路
        :rtype: object
        :param self.adj_matrix； 邻接矩阵,存储i -> j的所有班次
        :param mode: 模式，best_time表最优时间，best_price表最优价格
        :param from_to: 起点和终点城市
        :param depart_time: 最早可出发时间
        :return: 包含TravelRoute对象的列表,以及最优开销
        """
        # 从城市i最早可出发时间
        d_time_list: list = [-1] * 31
        # 城市列表为空
        if not list:
            return None, None
        depart = depart_time
        # 起点，终点
        start: int = label[from_to[0]]
        destination: int = label[from_to[1]]
        # 一定确定距离的城市集合
        already_certain: list = [bool] * 31
        # 从起点的时间或价格开销
        distance: list = [int] * 31
        # 路径
        path: list = [dict] * 31
        # 求出个点到起点的开销
        for city in range(31):
            weight_dict: dict = {}
            weight: int = 0
            already_certain[city] = False
            train_route = self.adj_matrix[start][city]['train']
            air_route = self.adj_matrix[start][city]['air']
            bullet_route = self.adj_matrix[start][city]['bullet']
            if mode == "best_time":
                weight_dict, weight = self.cal_weight_by_time(d_time=depart,
                                                              train_route=train_route, 
                                                              air_route=air_route,
                                                              bullet_route=bullet_route, 
                                                              vehicle=vehicle)
            elif mode == "best_price":
                weight_dict, weight = self.cal_weight_by_price(train_route=train_route,
                                                               air_route=air_route, 
                                                               bullet_route=bullet_route,
                                                               vehicle=vehicle)
            if not weight_dict:
                distance[city] = sys.maxsize
            else:
                if mode == "best_time":
                    distance[city] = weight
                    d_time_list[city] = (weight_dict['depart_time'] + weight_dict['length_time']) % 24
                else:
                    distance[city] = weight_dict['price']
            if distance[city] < sys.maxsize:
                path[city] = weight_dict
            else:
                path[city] = {}
        # 确认起点距离，到自身距离为0
        already_certain[start] = True
        distance[start] = 0

        for city in range(30):
            weight: int = 0
            weight_dict: dict = {}
            new_city: int = 0
            min_cost: int = sys.maxsize
            # 选出目前离起点开销最短的城市
            for j in range(31):
                if not already_certain[j] and (distance[j] < min_cost):
                    new_city = j
                    min_cost = distance[j]
            # 确定该城市距离
            already_certain[new_city] = True
            for j in range(31):
                if not already_certain[j]:  # 该城市距离未确定
                    # 获取班次列表
                    train_route: list = self.adj_matrix[new_city][j]['train']
                    air_route: list = self.adj_matrix[new_city][j]['air']
                    bullet_route: list = self.adj_matrix[new_city][j]['bullet']
                    if mode == "best_time":
                        depart = d_time_list[new_city]
                        weight_dict, weight = self.cal_weight_by_time(d_time=depart, 
                                                                      train_route=train_route,
                                                                      air_route=air_route, 
                                                                      bullet_route=bullet_route,
                                                                      vehicle=vehicle)
                    elif mode == "best_price":
                        weight_dict, weight = self.cal_weight_by_price(train_route=train_route, 
                                                                       air_route=air_route,
                                                                       bullet_route=bullet_route, 
                                                                       vehicle=vehicle)

                    if weight_dict:
                        if distance[j] > (distance[new_city] + weight):
                            # 如果从new_city到j开销小于原开销,更新
                            distance[j] = distance[new_city] + weight
                            if mode == "best_time":
                                # 最优时间模式还需更新到j城市后的最早可出发时间
                                d_time_list[j] = (weight_dict['depart_time'] + weight_dict['length_time']) % 24
                            # 加入路径
                            path[j] = weight_dict
        # 将path的记录改为正序
        order: list = []
        rou = path[destination]
        while rou:
            order.insert(0, rou)
            c_from = rou['from']
            num: int = label[c_from]
            rou = path[num]
        # 返回结果
        result: list = []
        for r in order:
            code: str = r['number']
            price: int = r['price']
            des: str = r['to']
            depart_time: int = r['depart_time']
            duration: int = r['length_time']
            by: str = r['type']
            seg = TravelRoute(by=by, code=code, price=price, des=des, depart_time=depart_time, duration=duration)
            result.append(seg)

        return result, distance[destination]