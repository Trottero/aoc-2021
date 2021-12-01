import numpy as np

data = np.loadtxt('./01/data.txt')

print(len(data))

zipped = zip(data[:-1], data[1:])

c = 0
for prev, curr in zipped:
    if curr > prev:
        c += 1

print(c)
