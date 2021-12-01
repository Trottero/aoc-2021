import numpy as np

data = np.loadtxt('./01/data.txt')

print(len(data))

zipped = zip(data[:-2], data[1:-1], data[2:])

# print(len(list(zipped)))

c = 0
last = 0
for f, s, t in zipped:
    current = f + s + t
    if current > last:
        c += 1
    last = current

print(c - 1)
