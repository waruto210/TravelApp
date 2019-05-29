from map import Map
from dijkstra_algorithm import Dijkstra
from tabu_algorithm import TabuAlgorithm
from routes import TravelRoute
import sys


class Traveler(object):
    """
    旅行主对象,生成地图和算法对象,给出search_plan()方法.
    """
    def __init__(self):
        # 生成地图和算法对象
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
        # 最终结果
        ret = []
        # 策略1,2
        if mode != 'three':
            # 初始最早可出发时间
            d_time = depart_time
            for i in range(len(cities) - 1):
                # 获取起点终点
                if i == 0:
                    start = cities[0]
                else:
                    start = cities[i][0]
                des = cities[i + 1][0]
                # 第一次搜索
                tmp, cost = self.Dijkstra.search_by_dijkstra(
                    mode=mode, from_to=[start, des],
                    depart_time=d_time, vehicle=vehicle)
                # 如果未搜到路径
                if cost == sys.maxsize:
                    # 且交通工具有优先要求，则去除交通工具优先请求，重新搜索
                    if vehicle != '':
                        tmp, cost = self.Dijkstra.search_by_dijkstra(
                            mode=mode, from_to=[start, des],
                            depart_time=d_time, vehicle='')
                # 仍未搜索到路径，返回空
                if cost == sys.maxsize:
                    return []
                # 将本段路径加入最终线路
                ret.extend(tmp)
                # 生成一个段标志对象
                stay = cities[i + 1][1]
                t_1 = TravelRoute(by='', code='', price=0, des='', depart_time=-1,
                                  duration=-1, is_tag=True, stay=stay)
                ret.append(t_1)
                # 更新最早可出发时间
                d_time = (d_time + cost + stay) % 24
            return ret

        else:
            d_time = depart_time
            for i in range(len(cities) - 1):
                # 是否满足了时间限制
                timelimit_satisfy: bool = True
                # 获取起点终点
                if i == 0:
                    start = cities[0]
                else:
                    start = cities[i][0]
                des = cities[i + 1][0]
                time_limit = cities[i + 1][1]
                # 第一次搜索
                tmp, cost = self.TabuAlgorithm.search_by_tabu(from_to=[start, des],
                                                              depart_time=depart_time,
                                                              time_limit=time_limit,
                                                              vehicle=vehicle)
                # 没有搜索到路径
                if cost == sys.maxsize:
                    # 时间要求不满足
                    timelimit_satisfy = False
                    # 放宽时间要求，重新搜索
                    for times in range(2, 5):
                        tmp, cost = self.TabuAlgorithm.search_by_tabu(from_to=[start, des],
                                                                      depart_time=depart_time,
                                                                      time_limit=time_limit * times,
                                                                      vehicle=vehicle)
                        # 搜索到路径，退出循环
                        if cost != sys.maxsize:
                            break
                # 仍未搜索到路径，返回空
                if cost == sys.maxsize:
                    return []
                # 将本段路径加入最终线路
                ret.extend(tmp)
                # 生成一个段标志对象
                stay = cities[i + 1][1]
                t_2 = TravelRoute(by='', code='', price=0, des='', depart_time=-1,
                                  duration=-1, is_tag=True, stay=stay,
                                  timelimit_satisfy=timelimit_satisfy)
                ret.append(t_2)
                # 更新最早可出发时间
                d_time = (d_time + cost + stay) % 24
            return ret

# 以下测试代码


T = Traveler()
ret: [TravelRoute] = T.search_plan(
    cities=['北京', ['重庆', 48], ['乌鲁木齐', 44], ['长沙', 25], ['北京', 20]],
    depart_time=13, mode='best_time', vehicle='')
for r in ret:
    if not r.is_tag:
        print(r.by, r.code, r.price, r.des, r.depart_time, r.duration)
    else:
        if r.is_tag:
            print("Stay for ", r.stay)
            print('\n')
            if not r.timelimit_satisfy:
                print("Sorry, following travel time limitation not satisfied!")
