import numpy as np

data = np.loadtxt('./05/data.txt', dtype=str, delimiter=' -> ')

print(len(data))

data = np.array([[(int(w.split(',')[0]), int(w.split(',')[1])) for w in z] for z in data])

max = np.max(data)

# Create map with +1 size as data is zero indexed.
map = np.zeros((max + 1, max + 1), dtype=int)

for vector in data:
    [x1, y1], [x2, y2] = vector

    print(x1, y1, x2, y2)

    # Skip vector if x and y are not equal
    if x1 != x2 and y1 != y2:
        continue

    # Swap ranges if one is larger than the other
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1

    # Mark vector on map
    map[y1:y2 + 1, x1:x2 + 1] += 1

print(map)
print(np.count_nonzero(map > 1))
