import numpy as np
import networkx as nx
from collections import Counter

edgelist = np.loadtxt('./12/data.txt', delimiter='-', dtype=str)
print(len(edgelist))

G = nx.from_edgelist(edgelist)

print(G)


def get_filtered_neighbours(G, route):
    if route[-1] == 'end':
        return []

    neighbours = G.neighbors(route[-1])
    neighbours = [n for n in neighbours if n not in route or n.isupper() or (n != 'start' and double_small(route))]
    return neighbours


def double_small(route):
    c = Counter(route)
    return not any(v > 1 for k, v in c.items() if k.islower())


neighbours = G.neighbors('start')
routes = [['start']]

done_in_route = {}

print(routes)

routes_expanded = True
while routes_expanded:
    routes_expanded = False
    for i, route in enumerate(routes):
        if route[-1] == 'end':
            continue

        # For every route, get the neighbours of the last node
        neighbours = get_filtered_neighbours(G, route)
        # Spawn new routes for each neighbour
        for n in neighbours:
            routes_expanded = True
            new_route = route.copy()
            new_route.append(n)
            routes.append(new_route)

        # Remove the currrent route from the list
        routes.pop(i)

print(len(routes))
