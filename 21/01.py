import numpy as np
from pprint import pprint

with open('./21/data.txt', 'r') as f:
    data = f.readlines()
    data = [l.strip() for l in data]

players_pos = np.zeros((len(data)))
players_score = np.zeros((len(data)))

for i in range(len(data)):
    players_pos[i] = int(data[i][-1])

die = 0
roll = 0

player_to_move = 0
while all(players_score < 1000):
    die = die % 100 + 1
    one = die
    die = die % 100 + 1
    two = die
    die = die % 100 + 1
    three = die

    roll += 1
    move = one + two + three
    players_pos[player_to_move] += move
    players_pos[player_to_move] = (players_pos[player_to_move] - 1) % 10 + 1
    players_score[player_to_move] += players_pos[player_to_move]
    player_to_move = (player_to_move + 1) % len(players_pos)

print(players_score)
roll *= 3

print(np.min(players_score) * roll)
