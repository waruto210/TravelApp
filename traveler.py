from map import Map
from dijkstra_algorithm import Dijkstra
from tabu_algorithm import TabuAlgorithm
from routes import TravelRoute
import sys


class Traveler(object):
    def __init__(self):
        self.map = Map('train.json', 'air.json', 'bullet.json')
        self.Dijkstra = Dijkstra(adj_matrix=self.map.adj_matrix)
        self.TabuAlgorithm = TabuAlgorithm(adj_matrix=self.map.adj_matrix)

    def search_plan(self, cities: list, depart_time: int, vehicle: str='',
                    mode: str='best_time', time_limit: int=None):
        """

        :param cities:
        :param depart_time:
        :param mode:
        :param time_limit:
        :return:
        """
        if mode != 'three':
            ret = self.Dijkstra.search_by_dijkstra(mode=mode, from_to=cities,
                                                   depart_time=depart_time, vehicle=vehicle)
            if not ret[0] and vehicle != '':
                ret = self.Dijkstra.search_by_dijkstra(mode=mode, from_to=cities,
                                                       depart_time=depart_time)
            if not ret[0]:
                return None
            routes: [TravelRoute] = ret[0]
            cost: int = ret[1]

            print('Total cost is ', cost, '!')
            for r in routes:
                print(r.by, r.code, r.price, r.des, r.depart_time, r.duration)
        else:
            ret = self.TabuAlgorithm.search_by_tabu(from_to=cities, depart_time=depart_time,
                                                    time_limit=time_limit, vehicle=vehicle)
            if ret[1] == sys.maxsize:
                return None
            routes: [TravelRoute] = ret[0]
            cost: int = ret[1]
            print('Total cost is ', cost, '!')
            for r in routes:
                print(r.by, r.code, r.price, r.des, r.depart_time, r.duration)
        return routes, cost


t = Traveler()
t.search_plan(mode='best_price', cities=['重庆', '长沙'], depart_time=12,  vehicle='bullet')
