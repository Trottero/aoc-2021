import numpy as np


coords = []
folds = []

with open('./13/data.txt', 'r') as f:
    folding = False
    for line in f:
        if line == '\n':
            folding = True
            continue
        if not folding:
            coords.append([int(n) for n in line.split(',')])
        else:
            ax, loc = line.split(' ')[-1].split('=')
            folds.append([ax, int(loc)])

print(len(coords))
print(coords[0])

print(len(folds))
print(folds[0])

# Copy over to np array
size_x = np.max([x for x, y in coords]) + 1
size_y = np.max([y for x, y in coords]) + 1

paper = np.zeros((size_y, size_x), dtype=int)

for x, y in coords:
    paper[y, x] = 1

for ax, loc in folds:
    print(ax, loc)
    if ax == 'x':
        paper = paper[:, :loc] + np.flip(paper[:, loc + 1:], axis=1)
    else:
        paper = paper[:loc, :] + np.flip(paper[loc + 1:, :], axis=0)


print(np.count_nonzero(paper))

args = np.nonzero(paper > 1)
paper[args] = 1

print(paper)

np.savetxt('./13/paper.txt', paper, fmt='%d')
