from trains.models import *
__all__ = [
    'get_routes',
]


def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph(qs):
    graph = {}
    for item in qs:
        graph.setdefault(item.from_city_id, set())
        graph[item.from_city_id].add(item.to_city_id)
    return graph


def get_routes(request, form) -> dict:
    context = {'form': form}
    # qs = Train.objects.all()
    qs = Train.objects.all().select_related('from_city', 'to_city')
    graph = get_graph(qs)
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    travel_time = data['travel_time']
    cities = data['cities']
    all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
    if not len(all_ways):
        raise ValueError('Маршрута, удовлетворяющего условиям не существует')
    if cities:
        cities_id = [city.id for city in cities]
        right_ways = []
        for route in all_ways:
            if all([city in route for city in cities_id]):
                right_ways.append(route)
        if not right_ways:
            raise ValueError('Маршрут, через эти города не возможен')
    else:
        right_ways = all_ways
    routes = []
    all_trains = {}
    for q in qs:
        all_trains.setdefault((q.from_city_id, q.to_city_id), [])
        all_trains[(q.from_city_id, q.to_city_id)].append(q)
    for route in right_ways:
        tmp = {'trains': []}
        total_time = 0
        for i in range(len(route) - 1):
            qs = all_trains[(route[i], route[i + 1])]
            q = qs[0]
            total_time += q.travel_time
            tmp['trains'].append(q)
        tmp['total_time'] = total_time
        if total_time <= travel_time:
            routes.append(tmp)
    if not routes:
        raise ValueError('Время в пути больше заданного')
    sorted_routes = []
    if len(routes) == 1:
        sorted_routes = routes
    else:
        times = sorted(list(set(r['total_time'] for r in routes)))
        for time in times:
            for route in routes:
                if time == route['total_time']:
                    sorted_routes.append(route)
    context['routes'] = sorted_routes
    context['cities'] = {'from_city': from_city.name, 'to_city': to_city.name}
    return context
