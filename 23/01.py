import numpy as np
from pprint import pprint
import tqdm
import sys
import networkx as nx

hallway = [''] * 7
hallway[4] = 'Z'
print(hallway)
rooms = ['B', 'A', 'C', 'D', 'B', 'C', 'D', 'A']

#   #############
#   #1234567890-#
#   ###.#.#.#.###
#     #.#.#.#.#
#     #########

G = nx.Graph()
for i in range(1, 11):
    G.add_edge(i, i+1)

room_edges = [(3, 12), (12, 13), (5, 14), (14, 15), (7, 16), (16, 17), (9, 18), (18, 19)]
for u, v in room_edges:
    G.add_edge(u, v)

invalid_end_positions = [3, 5, 7, 9]
room_nodes = [12, 13, 14, 15, 16, 17, 18, 19]

right_pos = {
    'A': [12, 13],
    'B': [14, 15],
    'C': [16, 17],
    'D': [18, 19],
}

cost = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

atts = {n: '' for n in range(1, 13)}
for i, v in enumerate(rooms):
    atts[i + 12] = v

nx.set_node_attributes(G, atts, name="amph")

print(G.nodes[12]['amph'])

min_score = 17_000


def get_possible_paths(G: nx.Graph):
    for amph, correct_nodes in right_pos.items():
        nodes = [x for x, y in G.nodes(data=True) if y['amph'] == amph]
        if all([c in correct_nodes for c in nodes]):
            continue  # All correct
        for node in nodes:
            # Check if node isnt already at the bottom of a room.
            if node == right_pos[amph][1]:
                continue
            paths = nx.single_source_dijkstra(G, node)[1]
            # Prune paths which contain nodes which are taken
            print(paths)

            cant_pass_through = [x for x, y in G.nodes(data=True) if y['amph'] != '']
            # If amph is moving from room to hallway / room
            if node in room_nodes:
                # Cant end on invalid positions and also not in the incorrect room
                cant_end_on = invalid_end_positions
            print()
    pass


get_possible_paths(G)


def solve(G, cost):
    if cost > min_score:
        return
    # Calculate all possible paths
