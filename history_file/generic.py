from population import Population
from cal_routes_count import cal_routes_count
from chromosome import Chromosome


def search_by_ga(adj_matrix: list, cities: list, depart_time: int, time_limit, epoch: int, route_length: int,
                 pop_size: int, p_mutation: float):

    routes_count: list = cal_routes_count(adj_matrix=adj_matrix)
    pop = Population(adj_matrix=adj_matrix, cities=cities, depart_time=depart_time, time_limit=time_limit,
                     routes_count=routes_count, route_length=route_length, pop_size=pop_size, p_mutation=p_mutation)

    for i in range(epoch):
        pop.mutation(i)
        pop.selection()

        if i % 1 == 0:
            ret: Chromosome = pop.get_best()
            print("epoch: " + str(i) + ' fitness: ' + str(ret.fitness))

