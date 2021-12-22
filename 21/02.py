import numpy as np
from pprint import pprint
from tqdm import tqdm

with open('./21/data.txt', 'r') as f:
    data = f.readlines()
    data = [int(l.strip()[-1]) for l in data]

board = np.arange(1, 11)

transpositions = {}

# All the different possbilities for 3 rolls in a row
# And their counts
roll_result = {}
for one in range(1, 4):
    for two in range(1, 4):
        for three in range(1, 4):
            s = one + two + three
            if s not in roll_result:
                roll_result[s] = 0

            roll_result[s] += 1

pprint(roll_result)
print(sum(roll_result.values()))


def playout(p1pos, p1score, p2pos, p2score, move):
    # Check if the current state is not a transposition of another state
    if (p1pos, p1score, p2pos, p2score, move) in transpositions.keys():
        return transpositions[(p1pos, p1score, p2pos, p2score, move)]

    # We are required to evaluate sub tree

    # Terminal node
    if p1score >= 21:
        # P1 has won
        return (1, 0)
    if p2score >= 21:
        # P2 has won
        return (0, 1)

    # Track the amount of wins for each player
    p1wins = 0
    p2wins = 0

    for pos_increase, count in roll_result.items():
        if move % 2 == 0:
            # Calculate the new score for player 1
            player1pos = (p1pos + pos_increase) % 10
            newp1wins, newp2wins = playout(player1pos, p1score + board[player1pos], p2pos, p2score, move + 1)
            p1wins += (newp1wins * count)
            p2wins += (newp2wins * count)
        else:
            # Calculate the new score for player 2
            player2pos = (p2pos + pos_increase) % 10
            newp1wins, newp2wins = playout(p1pos, p1score, player2pos, p2score + board[player2pos], move + 1)
            p1wins += (newp1wins * count)
            p2wins += (newp2wins * count)

    # We have evaluated subtree store it for future use.
    transpositions[(p1pos, p1score, p2pos, p2score, move)] = (p1wins, p2wins)

    return (p1wins, p2wins)


# Pos is 0-indexed and thus we need to remove one.
p1, p2 = playout(7, 0, 4, 0, 0)

print(p1, p2)
print(max(p1, p2))
assert p1 + p2 == 444356092776315 + 341960390180808
