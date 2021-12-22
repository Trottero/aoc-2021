import numpy as np
from pprint import pprint
import tqdm

with open('./22/data.txt', 'r') as f:
    data = f.readlines()
    data = [l.strip() for l in data]


procedures = []
for instruction, dims in [l.split(' ') for l in data]:
    dims = [d[2:] for d in dims.split(',')]
    (x1, x2), (y1, y2), (z1, z2) = [[d for d in a.split('..')] for a in dims]
    procedures.append((instruction, (int(x1), int(x2), int(y1), int(y2), int(z1), int(z2))))

print(procedures)


def get_cube_from_selection(x1, x2, y1, y2, z1, z2):
    # Get all coordinates within the selection
    x = np.arange(x1, x2 + 1)
    y = np.arange(y1, y2 + 1)
    z = np.arange(z1, z2 + 1)

    # Get all coordinates within the selection
    x, y, z = np.meshgrid(x, y, z)
    x = x.flatten()
    y = y.flatten()
    z = z.flatten()
    return list(zip(x, y, z))


reactor_state = {}

for instruction, box in tqdm.tqdm(procedures):
    if any(c > 50 or c < -50 for c in box):
        continue
    cube = get_cube_from_selection(*box)
    if instruction == 'on':
        reactor_state.update({c: 1 for c in cube})
    if instruction == 'off':
        reactor_state.update({c: 0 for c in cube})

print(sum(reactor_state.values()))
