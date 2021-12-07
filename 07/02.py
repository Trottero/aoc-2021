import numpy as np
import math
from scipy.special import factorial

data = np.loadtxt('./07/data.txt', dtype=int, delimiter=',')

print(len(data))
print(data[0])

average = int(np.average(data))
print('optimal position: ', average)


def triangular_number(n):
    for i in range(int(n)):  # range(3) is a generator for [0, 1, 2]
        n += i
    return n


vf = np.vectorize(triangular_number)


print(triangular_number(abs(data[0] - average)))

cost = np.sum(vf(np.abs(data - average)))
print(cost)
