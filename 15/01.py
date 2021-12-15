import numpy as np
from collections import Counter
import networkx as nx


d = np.loadtxt('./15/data.txt', dtype=str)
data = []
for l in d:
    data.append(np.array([int(c) for c in l]))

data = np.array(data)
print(data.shape)
print(data[0])

# Create a weighted undirected graph


def get_neigbours(pt, data):
    x, y = pt
    n = []
    if x > 0:
        n.append((-1, 0))
    if x < data.shape[0] - 1:
        n.append((1, 0))
    if y > 0:
        n.append((0, - 1))
    if y < data.shape[1] - 1:
        n.append((0, 1))

    return n


def get_node_id(pt, data):
    x, y = pt
    return y * data.shape[0] + x


def get_edges(pt, data):
    n = get_neigbours(pt, data)
    x, y = pt
    nodeid = get_node_id(pt, data)
    edges = []
    for xn, yn in n:
        edges.append((nodeid, get_node_id((x + xn, y + yn), data), data[y + yn, x + xn]))

    return edges


# Turn the numpy matrix into nodes and edges between all the nodes
G = nx.DiGraph()

for y in range(data.shape[0]):
    for x in range(data.shape[1]):
        value = data[y, x]

        edges = get_edges((x, y), data)
        for e in edges:
            u, v, w = e
            G.add_edge(u, v, weight=w)

print(G)

path = nx.dijkstra_path_length(G, 0, data.shape[0] * data.shape[1] - 1, weight='weight')
print(path)
pos = (0, 0)
