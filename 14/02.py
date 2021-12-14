import numpy as np
from collections import Counter


with open('./14/data.txt', 'r') as f:
    data = [x.strip() for x in f.readlines()]

template = data[0]
data = data[2:]
reaction_map = {}
for l in data:
    reactants, product = l.split(' -> ')
    reaction_map[reactants] = product

print(template)

print(len(reaction_map))

steps = 10
for step in range(steps):
    reactions = []
    for x, y in zip(range(0, len(template) - 1), range(1, len(template))):
        # print(template[x] + template[y])
        if template[x] + template[y] in reaction_map.keys():
            reactions.append([template[x] + template[y], x])
    adjustment = 0
    for reactant, index in reactions:
        template = template[:index + 1 + adjustment] + reaction_map[reactant] + template[index + 1 + adjustment:]
        adjustment += 1


print(template)
counts = dict(Counter(template))
counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

print(counts)

print(counts[0][1] - counts[-1][1])
