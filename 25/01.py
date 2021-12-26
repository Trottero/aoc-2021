import numpy as np
from pprint import pprint
import tqdm
import sys
import networkx as nx
from copy import deepcopy

data = np.loadtxt('./25/data.txt', dtype=str, delimiter=',')
data = np.array([np.array([c for c in x]) for x in data])
print(data[0])

print(data.shape)
moved = -1
steps = 0
while moved != 0:
    moved = 0
    potential = np.array(np.nonzero(data == '>'))
    y, x = potential
    xnew = x + 1
    xnew %= data.shape[1]

    cdata = data.copy()
    for y, xnew, xold in zip(y, xnew, x):
        if data[y, xnew] == '.':
            cdata[y, xnew] = '>'
            cdata[y, xold] = '.'
            moved += 1

    data = cdata

    potential = np.array(np.nonzero(data == 'v'))
    y, x = potential
    ynew = y + 1
    ynew %= data.shape[0]

    cdata = data.copy()
    for ynew, yold, x in zip(ynew, y, x):
        if data[ynew, x] == '.':
            cdata[ynew, x] = 'v'
            cdata[yold, x] = '.'
            moved += 1

    data = cdata
    steps += 1
print(steps)
