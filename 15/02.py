import numpy as np
from collections import Counter
import networkx as nx
from numpy.lib.utils import source


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


def get_node_id(pt, data, offset, size):
    # Get local pos first
    x, y = pt
    local_pos = y * data.shape[0] + x

    globaloffset = data.shape[0]**2

    gx, gy = offset

    return local_pos + gy * (globaloffset * size) + globaloffset * gx


def get_edges(pt, data, offset, size):
    n = get_neigbours(pt, data)
    x, y = pt
    nodeid = get_node_id(pt, data, offset, size)
    edges = []
    for xn, yn in n:
        edges.append((nodeid, get_node_id((x + xn, y + yn), data, offset, size), data[y + yn, x + xn]))

    return edges


def get_gradient(source_map, offset):
    x, y = offset
    o = x + y - 1

    return (source_map + o) % 9 + 1


G = nx.DiGraph()

for y in range(5):
    for x in range(5):
        gradient = get_gradient(data, (x, y))

        for gy in range(gradient.shape[0]):
            for gx in range(gradient.shape[1]):
                edges = get_edges((gx, gy), gradient, (x, y), 5)
                for e in edges:
                    u, v, w = e
                    G.add_edge(u, v, weight=w)

        if x > 0:
            # Create edges from from left gradient to this one.
            gs = gradient.shape[0]
            for ny in range(gs):
                u = get_node_id((gs - 1, ny), gradient, (x - 1, y), 5)
                v = get_node_id((0, ny), gradient, (x, y), 5)

                w = gradient[ny, 0]
                G.add_edge(u, v, weight=w)

                # Also add opposite edge
                prev_w = get_gradient(data, (x - 1, y))[ny, gs - 1]
                G.add_edge(v, u, weight=prev_w)

        if y > 0:
            # Create edges from from left gradient to this one.
            gs = gradient.shape[0]
            for n_x in range(gs):
                u = get_node_id((n_x, gs - 1), gradient, (x, y - 1), 5)
                v = get_node_id((n_x, 0), gradient, (x, y), 5)
                w = gradient[0, n_x]
                G.add_edge(u, v, weight=w)

                # Also add opposite edge
                prev_w = get_gradient(data, (x, y - 1))[gs - 1, n_x]
                G.add_edge(v, u, weight=prev_w)


print(G)

path = nx.dijkstra_path_length(G, 0, data.shape[0] * 5 * 5 * data.shape[1] - 1, weight='weight')
print(path)
pos = (0, 0)


print(get_gradient(data, (1, 1)))
