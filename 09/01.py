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


minima = []

for y in range(data.shape[0]):
    for x in range(data.shape[1]):
        if is_local_minima((x, y), data):
            minima.append(data[y, x])

print(sum(minima) + len(minima))
