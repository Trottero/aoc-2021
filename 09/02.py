import numpy as np

with open('./09/data.txt', 'r') as f:
    data = f.readlines()
    d = []
    for l in data:
        a = np.array([c for c in l if c != '\n'], dtype=int)
        d.append(a)

data = np.array(d)

print(len(data))
print(data[0])


def is_local_minima(pt, data):
    x, y = pt
    val = data[y, x]
    if x > 0 and data[y, x - 1] <= data[y, x]:
        return False

    if x < data.shape[1] - 1 and data[y, x + 1] <= data[y, x]:
        return False

    if y > 0 and data[y - 1, x] <= data[y, x]:
        return False

    if y < data.shape[0] - 1 and data[y + 1, x] <= data[y, x]:
        return False

    return True


def larger_neighbours(pt, data):
    x, y = pt
    n = []

    if x > 0 and data[y, x - 1] > data[y, x]:
        n.append((x - 1, y))

    if x < data.shape[1] - 1 and data[y, x + 1] > data[y, x]:
        n.append((x + 1, y))

    if y > 0 and data[y - 1, x] > data[y, x]:
        n.append((x, y - 1))

    if y < data.shape[0] - 1 and data[y + 1, x] > data[y, x]:
        n.append((x, y + 1))

    # Already filter out the empty list
    n = [nn for nn in n if data[nn[1], nn[0]] != 9]
    return n


def get_basin_size(pt, data):
    x, y = pt

    # Initialize list with neighbours
    n = larger_neighbours(pt, data)
    counted = [pt]
    while len(n) > 0:
        x, y = n.pop()
        counted.append((x, y))

        # Add neighbours which are not already counted
        n.extend([x for x in larger_neighbours((x, y), data) if x not in counted])

    return len(list(set(counted)))


basins = []

for y in range(data.shape[0]):
    for x in range(data.shape[1]):
        basin_size = 0
        if is_local_minima((x, y), data):
            basin_size = get_basin_size((x, y), data)
            basins.append(basin_size)

largest = sorted(basins, reverse=True)[:3]

s = 1
for n in largest:
    s *= n

print(s)
