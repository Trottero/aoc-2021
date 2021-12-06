import numpy as np
import time

data = np.loadtxt('./06/data.txt', dtype=int, delimiter=',')

start = time.perf_counter()
fish = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0,
}

for f in data:
    fish[f] += 1


for day in range(256):
    children = fish[0]
    fish[7] += children
    fish[9] = children

    # Increment day
    for i in range(0, 9):
        fish[i] = fish[i + 1]


fish[9] = 0

print(np.sum(list(fish.values())))

print('Time taken: ', (time.perf_counter() - start) * 1000, 'ms')
