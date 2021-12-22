import numpy as np
from pprint import pprint

with open('./21/data.txt', 'r') as f:
    data = f.readlines()
    data = [int(l.strip()[-1]) for l in data]

# We needs to calculate the number of rolls that would be required for all possbilities to get to 21


# 22 elements as score as the 22th element keeps all ones above 21
track = {}
# Throws # pos # score -> count

# Set the starting score and position of player 1
track[(0, 3, 0)] = 9

# Throws and counts
throws_counts = {}

scores = np.arange(1, 11)

# Calculate the number of throws for each position and score
terminated_dims = 0
while sum(track.values()) != 0:
    next = {}
    # Update every entry
    for (throws, pos, score), count in track.items():
        # 2, 5, 11, 17, 23
        # dims = 3**(throws * 6 + 2)
        if throws == 0:
            dims = 1
        else:
            dims = 729

        # We need to account for finished dims.

        # dims = 3**(throws * 6 + 2)
        # Dims grow with a factor of 729...

        # Calculate next states
        pos1 = (pos + 1) % 10
        pos2 = (pos + 2) % 10
        pos3 = (pos + 3) % 10

        score1 = score + scores[pos1]
        score2 = score + scores[pos2]
        score3 = score + scores[pos3]

        terminated_dims = 0
        added = [(throws + 1, pos1, score1), (throws + 1, pos2, score2), (throws + 1, pos3, score3)]
        for (a_throws, a_pos, a_score) in added:
            if a_score >= 21:
                if a_throws not in throws_counts:
                    throws_counts[a_throws] = 0
                throws_counts[a_throws] += count * dims
            else:
                if (a_throws, a_pos, a_score) not in next:
                    next[(a_throws, a_pos, a_score)] = 0
                next[(a_throws, a_pos, a_score)] += count * dims

    print(dims, terminated_dims)

    track = next

print(throws_counts)

s = sum(throws_counts.values())
print(s)
print(444356092776315 + 341960390180808)
