import numpy as np
from pprint import pprint
import tqdm
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.patches as patches
from matplotlib.collections import LineCollection

with open('./22/data.txt', 'r') as f:
    data = f.readlines()
    data = [l.strip() for l in data]


procedures = []
for instruction, dims in [l.split(' ') for l in data]:
    dims = [d[2:] for d in dims.split(',')]
    (x1, x2), (y1, y2), (z1, z2) = [[d for d in a.split('..')] for a in dims]
    procedures.append((instruction, (int(x1), int(x2) + 1, int(y1), int(y2) + 1, int(z1), int(z2) + 1)))

x = []
y = []
z = []
for instruction, box in procedures:
    x1, x2, y1, y2, z1, z2 = box
    x.extend([x1, x2])
    y.extend([y1, y2])
    z.extend([z1, z2])

minx, maxx = min(x), max(x)
miny, maxy = min(y), max(y)
minz, maxz = min(z), max(z)

print(procedures)


def get_box_lines(box):
    x1, x2, y1, y2, z1, z2 = box

    x = [[x1, x2], [x1, x2], [x1, x1], [x2, x2], [x1, x2], [x1, x2], [x1, x1], [x2, x2], [x1, x1], [x2, x2], [x1, x1], [x2, x2]]
    y = [[y1, y1], [y2, y2], [y1, y2], [y1, y2], [y1, y1], [y2, y2], [y1, y2], [y1, y2], [y1, y1], [y1, y1], [y2, y2], [y2, y2]]
    z = [[z1, z1], [z1, z1], [z1, z1], [z1, z1], [z2, z2], [z2, z2], [z2, z2], [z2, z2], [z1, z2], [z1, z2], [z1, z2], [z1, z2]]

    return x, y, z


fig = plt.figure()
ax = plt.axes(projection='3d')


def plot_boxes(boxes, highlights=None, save=False, plt_name=None):
    for box in boxes:
        for x, y, z in zip(*get_box_lines(box)):
            ax.plot(x, y, z, 'grey')
    if highlights:
        for bs, color in highlights:
            for b in bs:
                for x, y, z in zip(*get_box_lines(b)):
                    ax.plot(x, y, z, color)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_zlim(minz, maxz)

    if save:
        plt.savefig('22/figs/{}.png'.format(plt_name))
        plt.gca().cla()
    else:
        plt.show()


def box_size(box):
    x1, x2, y1, y2, z1, z2 = box
    x = abs(x2 - x1)
    if x == 0:
        x = 1
    y = abs(y2 - y1)
    if y == 0:
        y = 1
    z = abs(z2 - z1)
    if z == 0:
        z = 1
    return x * y * z


def calculate_overlap_region(reg1, reg2):
    # If x is out of bounds
    if reg2[0] > reg1[1] or reg2[1] < reg1[0]:
        return None
    # If y is out of bounds
    if reg2[2] > reg1[3] or reg2[3] < reg1[2]:
        return None
    # If z is out of bounds
    if reg2[4] > reg1[5] or reg2[5] < reg1[4]:
        return None

    xoverlap = max(reg1[0], reg2[0]), min(reg1[1], reg2[1])
    yoverlap = max(reg1[2], reg2[2]), min(reg1[3], reg2[3])
    zoverlap = max(reg1[4], reg2[4]), min(reg1[5], reg2[5])

    if xoverlap[0] == xoverlap[1] or yoverlap[0] == yoverlap[1] or zoverlap[0] == zoverlap[1]:
        return None

    return (*xoverlap, *yoverlap, *zoverlap)


def is_sub_box(big, small):
    x1, x2, y1, y2, z1, z2 = big
    sx1, sx2, sy1, sy2, sz1, sz2 = small
    return (x1 <= sx1 <= x2) and (x1 <= sx2 <= x2) and (y1 <= sy1 <= y2) and (y1 <= sy2 <= y2) and (z1 <= sz1 <= z2) and (z1 <= sz2 <= z2)


def remove_overlap(reg1, overlap):
    x1, x2, y1, y2, z1, z2 = reg1
    ox1, ox2, oy1, oy2, oz1, oz2 = overlap
    if is_sub_box(reg1, overlap):
        xs = [(x1, ox1), (ox1, ox2), (ox2, x2)]
        ys = [(y1, oy1), (oy1, oy2), (oy2, y2)]
        zs = [(z1, oz1), (oz1, oz2), (oz2, z2)]
    else:
        if x1 == x2:
            xs = [(x1, x2)]
        else:
            if x1 == ox1:
                xs = [(x1, ox2), (ox2, x2)]
            else:
                xs = [(x1, ox1), (ox1, x2)]

        if y1 == y2:
            ys = [(y1, y2)]
        else:
            if y1 == oy1:
                ys = [(y1, oy2), (oy2, y2)]
            else:
                ys = [(y1, oy1), (oy1, y2)]

        if z1 == z2:
            zs = [(z1, z2)]
        else:
            if z1 == oz1:
                zs = [(z1, oz2), (oz2, z2)]
            else:
                zs = [(z1, oz1), (oz1, z2)]

    cubes = []
    for x in xs:
        for y in ys:
            for z in zs:
                cubes.append((*x, *y, *z))

    # plot_boxes(regions.keys(), [(cubes, 'red'), ([reg1], 'blue'), ([overlap], 'green')])

    cubes = list(set(cubes))
    to_rm = []
    for x1, x2, y1, y2, z1, z3 in cubes:
        if x1 == x2 or y1 == y2 or z1 == z3:
            to_rm.append((x1, x2, y1, y2, z1, z3))
    for cube in to_rm:
        cubes.remove(cube)

    assert sum(box_size(c) for c in cubes) == box_size(reg1)
    cubes.remove(overlap)
    return cubes


def count_on(regions):
    s = 0
    for box in regions.keys():
        if regions[box] == 1:
            s += box_size(box)

    return s


regions = {}

plt_name = 1
boxes = []
for instruction, box in procedures:
    # Check if the box collides with any other known box
    updates = {}
    to_remove = []
    print(instruction, box)
    # plot_boxes(boxes, [([box], 'blue')], save=True, plt_name=plt_name)
    # boxes.append(box)
    plt_name += 1
    for reg_box, reg_val in regions.items():
        overlap = calculate_overlap_region(reg_box, box)
        if overlap is None:
            continue

        if reg_box == overlap:
            to_remove.append(reg_box)
            continue

        # If the box is overlapping, split the existing box into 3 new ones
        boxes = remove_overlap(reg_box, overlap)
        for subbox in boxes:
            updates[subbox] = reg_val
        to_remove.append(reg_box)

    for reg_box in to_remove:
        regions.pop(reg_box)
    regions.update(updates)

    if instruction == 'on':
        regions[box] = 1
    else:
        regions[box] = 0

    print(count_on(regions))

print(box_size((11, 13, 11, 13, 11, 13)))
pprint(regions)
s = 0
for box in regions.keys():
    if regions[box] == 1:
        s += box_size(box)

print(s)
