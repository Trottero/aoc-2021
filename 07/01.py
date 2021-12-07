import numpy as np

data = np.loadtxt('./07/data.txt', dtype=int, delimiter=',')

print(len(data))
print(data[0])

median = np.median(data)
print(median)

cost = np.sum(np.abs(data - median))
print(cost)
