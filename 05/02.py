import numpy as np

data = np.loadtxt('./05/data.txt', dtype=str, delimiter=' -> ')

print(len(data))

data = np.array([[(int(w.split(',')[0]), int(w.split(',')[1])) for w in z] for z in data])

max = np.max(data)

# Create map with +1 size as data is zero indexed.
map = np.zeros((max + 1, max + 1), dtype=int)

for vector in data:
    start, target = vector

    direction = target - start
    distance = abs(direction[np.argwhere(direction)[0]])
    direction = np.array(direction / distance, dtype=int)

    for i in range(int(distance + 1)):
        map[start[1] + i * direction[1], start[0] + i * direction[0]] += 1


print(np.count_nonzero(map > 1))
