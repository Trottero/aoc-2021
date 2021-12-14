import numpy as np
from collections import Counter
import tqdm

with open('./14/data.txt', 'r') as f:
    data = [x.strip() for x in f.readlines()]

template = data[0]
data = data[2:]
reaction_map = {}
for l in data:
    reactants, product = l.split(' -> ')
    reaction_map[reactants] = product

print(template)

groups = {}
for x, y in zip(range(0, len(template) - 1), range(1, len(template))):
    if template[x] + template[y] not in groups.keys():
        groups[template[x] + template[y]] = 0
    groups[template[x] + template[y]] += 1

print(groups)

print(len(reaction_map))
steps = 40
for step in range(steps):
    reactions = []
    # Precalculate all of the reactions
    for reactant, product in reaction_map.items():
        if reactant in groups.keys():
            # We need to add this later
            reactions.append((reactant, product, groups[reactant]))

    for reactant, product, amount in reactions:
        groups[reactant] -= amount
        # Create the child elements created by this reaction
        a, b = reactant
        a1 = a + product
        b1 = product + b
        if a1 not in groups.keys():
            groups[a1] = 0
        if b1 not in groups.keys():
            groups[b1] = 0
        groups[a1] += amount
        groups[b1] += amount


print(groups)

counts = {}
for k, v in groups.items():
    a, b = k
    if a not in counts.keys():
        counts[a] = 0
    if b not in counts.keys():
        counts[b] = 0
    counts[a] += v
    counts[b] += v

print(counts)

counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

print(counts)

print(counts[0][1] - counts[-1][1])
print(round((counts[0][1] - counts[-1][1]) / 2))
