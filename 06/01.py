import numpy as np

data = np.loadtxt('./06/data.txt', dtype=int, delimiter=',')

print(data[0])

for day in range(256):
    mask = data == 0
    data[mask] = 7
    children = np.count_nonzero(mask)
    data = np.append(data, np.full(children, 9))

    data -= 1

    # print(data)

print(len(data))
