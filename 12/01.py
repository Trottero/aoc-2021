import numpy as np
import networkx as nx

edgelist = np.loadtxt('./12/data.txt', delimiter='-', dtype=str)
print(len(edgelist))

G = nx.from_edgelist(edgelist)

print(G)

neighbours = G.neighbors('start')
routes = [['start']]

print(routes)

routes_expanded = True
while routes_expanded:
    routes_expanded = False
    for i, route in enumerate(routes):
        if route[-1] == 'end':
            continue

        # For every route, get the neighbours of the last node
        neighbours = G.neighbors(route[-1])
        # filter out neighbours that are already in the route
        neighbours = [n for n in neighbours if n not in route or n.isupper()]
        # Spawn new routes for each neighbour
        for n in neighbours:
            routes_expanded = True
            new_route = route.copy()
            new_route.append(n)
            routes.append(new_route)

        # Remove the currrent route from the list
        routes.pop(i)

print(len(routes))
