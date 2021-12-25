import numpy as np
from pprint import pprint
import tqdm
import sys
import networkx as nx
from copy import deepcopy

rooms = ['D', 'B', 'D', 'A', 'C', 'A', 'B', 'C']
# rooms = ['B', 'A', 'C', 'D', 'B', 'C', 'D', 'A']
# rooms = ['', '', 'C', 'D', 'B', 'C', 'D', '']

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

valid_end_positions = [1, 2, 4, 6, 8, 10, 11]
room_nodes = [12, 13, 14, 15, 16, 17, 18, 19]

right_pos = {
    'A': [12, 13],
    'B': [14, 15],
    'C': [16, 17],
    'D': [18, 19],
}

costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}

atts = {n: '' for n in range(1, 12)}
for i, v in enumerate(rooms):
    atts[i + 12] = v

nx.set_node_attributes(G, atts, name="amph")

print(G.nodes[12]['amph'])
# G.nodes[6]['amph'] = 'A'
min_score = 17_000


def get_possible_paths(Gv: nx.Graph):
    possible_paths = {}
    for amph, correct_nodes in right_pos.items():
        nodes = [x for x, y in Gv.nodes(data=True) if y['amph'] == amph]
        if all([c in correct_nodes for c in nodes]):
            continue  # All correct
        for node in nodes:
            # Check if node isnt already at the bottom of a room.
            if node == right_pos[amph][1]:
                continue
            paths = nx.single_source_dijkstra(Gv, node)[1]
            # Prune paths which contain nodes which are taken
            # print('Paths for node', node)
            # print(paths)

            cant_pass_through = [x for x, y in Gv.nodes(data=True) if y['amph'] != '']
            cant_pass_through.remove(node)
            # print('Cant pass through', cant_pass_through)
            if node in room_nodes:
                should_end_on = [*valid_end_positions]
            else:
                should_end_on = []
            # If amph is moving from room to hallway / room
            # Room is empty
            if Gv.nodes[right_pos[amph][0]]['amph'] == '' and Gv.nodes[right_pos[amph][1]]['amph'] == '':
                # Add just the last position
                should_end_on.append(right_pos[amph][1])
            # Room has the correct one in the deepest pos with other empty
            elif Gv.nodes[right_pos[amph][0]]['amph'] == '' and Gv.nodes[right_pos[amph][1]]['amph'] == amph:
                should_end_on.append(right_pos[amph][0])

            if len(should_end_on) == 0:
                continue
            # Filter out paths with invalid destination
            paths = {dest: path for dest, path in paths.items() if dest in should_end_on}
            # Filter out paths which go through a amph
            paths = {dest: path for dest, path in paths.items() if not any(n in cant_pass_through for n in path)}
            # Filter out paths which are of len 1
            paths = {dest: path for dest, path in paths.items() if len(path) != 1}

            # print('Filtered')
            # print(paths)
            # print()

            if len(paths) != 0:
                possible_paths[node] = paths
    return possible_paths


def is_solved(G):
    for amph, (pos1, pos2) in right_pos.items():
        if G.nodes[pos1]['amph'] != amph or G.nodes[pos2]['amph'] != amph:
            return False

    return True


transpositions = {}


def to_transposition(Gv):
    return ''.join([str(x) + Gv.nodes[x]['amph'] + '-' for x in range(1, Gv.number_of_nodes() + 1)])


def solve(Gv: nx.Graph, cost):
    # if to_transposition(Gv) in transpositions:
    #     return
    global min_score
    if cost > min_score:
        return
    # Calculate all possible paths
    paths = get_possible_paths(Gv)
    if len(paths) == 0 and is_solved(Gv) and cost < min_score:
        print('New min score', cost)
        min_score = cost
        return
    if len(paths) == 0:
        return
    for node, npaths in paths.items():
        for dest, path in npaths.items():
            # Apply move to graph and calculate cost
            D = Gv.copy()
            D.nodes[dest]['amph'] = D.nodes[node]['amph']
            D.nodes[node]['amph'] = ''
            solve(D, cost + (len(path) - 1) * costs[D.nodes[dest]['amph']])
            transpositions[to_transposition(D)] = True


solve(G, 0)

print(min_score)
