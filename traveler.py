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

    def search_plan(self, cities: list, depart_time: int, vehicle: str = '',
                    mode: str = 'best_time'):
        """

        :param cities: 形式[出发地, [城市1 时间限制(策略3才有) 停留时间] [出发地2, 时间限制 停留时间], ...]
        :param depart_time: 出发时间
        :param vehicle: 分别为air bullet train
        :param mode: best_time best_price three
        :return: 返回[TravelRoute],当TravelRoute对象的is_tag为True时,表示这为一个标志,指示其前的
                一段旅程到达后停留多久(stay),帮助前端计算用,是否满足了用户的时间限制(timelimit_satisfy, 策略3时显示给用户)
                若返回了[]，则表示即使算法自动放宽了搜索要求仍旧无法搜索到路径，告知用户。

        """
        ret = []
        if mode != 'three':
            d_time = depart_time
            for i in range(len(cities) - 1):
                if i == 0:
                    start = cities[0]
                else:
                    start = cities[i][0]
                des = cities[i + 1][0]
                tmp, cost = self.Dijkstra.search_by_dijkstra(
                    mode=mode, from_to=[start, des],
                    depart_time=d_time, vehicle=vehicle)
                if cost == sys.maxsize:
                    if vehicle != '':
                        tmp, cost = self.Dijkstra.search_by_dijkstra(
                            mode=mode, from_to=[start, des],
                            depart_time=d_time, vehicle='')
                    else:
                        return []
                ret.extend(tmp)
                stay = cities[i + 1][1]
                t_1 = TravelRoute(by='', code='', price=0, des='', depart_time=-1,
                                  duration=-1, is_tag=True, stay=stay)
                ret.append(t_1)

                d_time = (d_time + cost + stay) % 24
            return ret

        else:
            d_time = depart_time
            for i in range(len(cities) - 1):
                timelimit_satisfy: bool = True
                if i == 0:
                    start = cities[0]
                else:
                    start = cities[i][0]
                des = cities[i + 1][0]
                time_limit = cities[i + 1][1]
                tmp, cost = self.TabuAlgorithm.search_by_tabu(from_to=[start, des],
                                                              depart_time=depart_time,
                                                              time_limit=time_limit,
                                                              vehicle=vehicle)
                if cost == sys.maxsize:
                    timelimit_satisfy = False
                    for times in range(2, 5):
                        tmp, cost = self.TabuAlgorithm.search_by_tabu(from_to=[start, des],
                                                                      depart_time=depart_time,
                                                                      time_limit=time_limit * times,
                                                                      vehicle=vehicle)
                        if cost != sys.maxsize:
                            break
                if cost == sys.maxsize:
                    return []
                ret.extend(tmp)
                stay = cities[i + 1][1]
                t_2 = TravelRoute(by='', code='', price=0, des='', depart_time=-1,
                                  duration=-1, is_tag=True, stay=stay,
                                  timelimit_satisfy=timelimit_satisfy)
                ret.append(t_2)
                d_time = (d_time + cost + stay) % 24
            return ret

# 以下测试代码


# T = Traveler()
# ret: [TravelRoute] = T.search_plan(
#     cities=['北京', ['重庆', 4, 48], ['乌鲁木齐', 16, 44], ['长沙', 22, 25], ['北京', 15, 20]],
#     depart_time=13, mode='best_time', vehicle='air')
# for r in ret:
#     if not r.is_tag:
#         print(r.by, r.code, r.price, r.des, r.depart_time, r.duration)
#     else:
#         if r.is_tag:
#             print("Stay for ", r.stay)
#             print('\n')
#             if not r.timelimit_satisfy:
#                 print("Sorry, following travel time limitation not satisfied!")
