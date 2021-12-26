import numpy as np
from pprint import pprint
import tqdm
import sys
import networkx as nx
from copy import deepcopy

rooms = ['D', 'D', 'D', 'B',
         'D', 'C', 'B', 'A',
         'C', 'B', 'A', 'A',
         'B', 'A', 'C', 'C']
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

room_edges = [
    (3, 12),
    (12, 13),
    (13, 14),
    (14, 15),
    (5, 16),
    (16, 17),
    (17, 18),
    (18, 19),
    (7, 20),
    (20, 21),
    (21, 22),
    (22, 23),
    (9, 24),
    (24, 25),
    (25, 26),
    (26, 27)]
for u, v in room_edges:
    G.add_edge(u, v)

valid_end_positions = [1, 2, 4, 6, 8, 10, 11]
room_nodes = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

right_pos = {
    'A': [12, 13, 14, 15],
    'B': [16, 17, 18, 19],
    'C': [20, 21, 22, 23],
    'D': [24, 25, 26, 27]
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

print(atts)
print(len(atts))
print(G.number_of_nodes())
nx.set_node_attributes(G, atts, name="amph")

print(G.nodes[12]['amph'])
# G.nodes[6]['amph'] = 'A'
min_score = 200_000


def is_in_correct_position(Gv: nx.Graph, node):
    amph = Gv.nodes[node]['amph']
    if node not in right_pos[amph]:
        return False
    # We are atleast in the right room.
    # Check if there are amphs below the current amph which are right.
    i = right_pos[amph].index(node)
    for j in range(i + 1, len(right_pos[amph])):
        if Gv.nodes[right_pos[amph][j]]['amph'] != amph:
            return False
    return True


def col_is_valid(Gv: nx.Graph, amph):
    room = right_pos[amph]
    for node in room:
        if not (Gv.nodes[node]['amph'] == '' or Gv.nodes[node]['amph'] == amph):
            return False
    return True


def get_possible_end_loc(Gv: nx.Graph, node):
    amph = Gv.nodes[node]['amph']
    # We can only move into hallways if possible
    if node in right_pos[amph]:
        return False, -1
    # We are in hallways or in other room
    prev = -1
    if not col_is_valid(Gv, amph):
        return False, -1
    for nodes in right_pos[amph]:
        if Gv.nodes[nodes]['amph'] != '':
            break
        prev = nodes
    return True, prev


def get_possible_paths(Gv: nx.Graph):
    possible_paths = {}
    for amph, correct_nodes in right_pos.items():
        nodes = [x for x, y in Gv.nodes(data=True) if y['amph'] == amph]
        if all([c in correct_nodes for c in nodes]):
            continue  # All correct
        for node in nodes:
            # Check if node isnt already at the bottom of a room.
            if is_in_correct_position(Gv, node):
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
            can_go_in_room, ridx = get_possible_end_loc(Gv, node)
            if can_go_in_room:
                should_end_on.append(ridx)

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
    for amph, posses in right_pos.items():
        if not all([G.nodes[x]['amph'] == amph for x in posses]):
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
