import numpy as np
import tqdm

data = np.loadtxt('./11/data.txt', dtype=str)

data = np.array([np.array([int(c) for c in row]) for row in data])

print(len(data))
print(data[0])

print(data.shape)

for step in tqdm.tqdm(range(10000)):
    data += 1
    flashers = np.argwhere(data > 9)
    flashed = []

    while len(flashers) != 0:
        # Increase adjecent cells with one
        for y, x in flashers:
            if x > 0:
                data[y][x - 1] += 1
                if y > 0:
                    data[y - 1][x - 1] += 1
                if y < len(data) - 1:
                    data[y + 1][x - 1] += 1

            if x < len(data[y]) - 1:
                data[y][x + 1] += 1
                if y > 0:
                    data[y - 1][x + 1] += 1
                if y < len(data) - 1:
                    data[y + 1][x + 1] += 1
            if y > 0:
                data[y - 1][x] += 1
            if y < len(data) - 1:
                data[y + 1][x] += 1
            data[y, x] = -100

        # Mark these as flashed
        flashed.extend(flashers)

        # Find new flashers
        flashers = [x for x in np.argwhere(data > 9)]

    for y, x in flashed:
        data[y, x] = 0

    if len(flashed) == data.shape[0] * data.shape[1]:
        break
