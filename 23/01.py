import numpy as np
from pprint import pprint
import tqdm
import sys

hallway = [''] * 7
hallway[4] = 'Z'
print(hallway)
rooms = [['B', 'A'], ['C', 'D'], ['B', 'C'], ['D', 'A']]

#   #############
#   #01.2.3.4.56#
#   ###B#C#B#D###
#     #A#D#C#A#
#     #########


right_pos = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
}

cost = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}


def get_possible_moves(hallway, rooms):
    # Pod, newpos, cost
    available_moves = []
    for room_id, room in enumerate(rooms):
        # Do not consider completed rooms
        if room[0] != '' and room[1] != '' and room_id == right_pos[room[0]] and room_id == right_pos[room[1]]:
            continue

        if room[0] != '':
            to_move = room[0]
            add = 0
        else:
            to_move = room[1]
            add = 1

        # Get all available moves to the right
        for distance, v in list(enumerate(hallway[room_id + 2:])):
            # only count empty hallways
            if v != '':
                break
            destination_room = distance + room_id + 2
            if destination_room == 6:
                available_moves.append((to_move, destination_room, (distance * 2 + 1 + add) * cost[to_move]))
            else:
                available_moves.append((to_move, destination_room, (distance * 2 + 2 + add) * cost[to_move]))
        # Get all available moves to the left
        for distance, v in list(enumerate(hallway[:room_id + 2][::-1])):
            # only count empty hallways
            if v != '':
                break
            destination_room = room_id + 2 - distance - 1
            if destination_room == 0:
                available_moves.append((to_move, destination_room, (distance * 2 + 1 + add) * cost[to_move]))
            else:
                available_moves.append((to_move, destination_room, (distance * 2 + 2 + add) * cost[to_move]))

        for hallway_index, v in enumerate(hallway):
            if v == '':
                continue
            if hallway_index >= right_pos[v] + 2:
                # We have to move to the left
                if hallway_index == right_pos[v] + 2:
                    available_moves.append((v, hallway_index, (hallway_index - right_pos[v] - 1) * cost[v]))
            else:
                # Move to the right

                pass
    return available_moves


#01#2#3#4#56#
#...A.......#
###B#C#B#D###
  #A#D#C#A#
  #2#3#4#5#

min_score = sys.maxsize


def solve(hallway, rooms, score, moves):
    pass


print(get_possible_moves(hallway, rooms))
