import numpy as np
from pprint import pprint

with open('./20/data.txt', 'r') as f:
    data = f.readlines()
    data = [l.strip() for l in data]

algorithm = data[0]
print(len(algorithm))
data = np.array([np.array([c for c in d]) for d in data[2:]])
print(data)

light_pixels = np.nonzero(data == '#')

pixel_map = {}
for x, y in zip(light_pixels[1], light_pixels[0]):
    pixel_map[(x, y)] = '#'

dark_pixels = np.nonzero(data == '.')

for x, y in zip(dark_pixels[1], dark_pixels[0]):
    pixel_map[(x, y)] = '.'


def get_neighbours(x, y):
    neighbours = []
    for j in range(-1, 2):
        for i in range(-1, 2):
            neighbours.append((x + i, y + j))
    return neighbours


def print_map(pixel_map):
    min_x = min(pixel_map.keys(), key=lambda x: x[0])[0]
    max_x = max(pixel_map.keys(), key=lambda x: x[0])[0]
    xsize = max_x - min_x + 1

    min_y = min(pixel_map.keys(), key=lambda x: x[1])[1]
    max_y = max(pixel_map.keys(), key=lambda x: x[1])[1]
    ysize = max_y - min_y + 1

    strmap = np.full((ysize, xsize), '_', dtype=str)
    for (x, y), v in pixel_map.items():
        strmap[y + abs(min_y), x + abs(min_x)] = v
    print(strmap)


def compute_min_max(pixel_map):
    min_x = min(pixel_map.keys(), key=lambda x: x[0])[0]
    max_x = max(pixel_map.keys(), key=lambda x: x[0])[0]

    min_y = min(pixel_map.keys(), key=lambda x: x[1])[1]
    max_y = max(pixel_map.keys(), key=lambda x: x[1])[1]

    return min_x, max_x, min_y, max_y


def pad_with_space(pixel_map):
    min_x, max_x, min_y, max_y = compute_min_max(pixel_map)

    # Add 2 layers of outer pixels
    for x in range(min_x - 2, max_x + 3):
        pixel_map[(x, min_y - 1)] = infinite_space
        pixel_map[(x, min_y - 2)] = infinite_space
        pixel_map[(x, max_y + 1)] = infinite_space
        pixel_map[(x, max_y + 2)] = infinite_space
    for y in range(min_y, max_y + 1):
        pixel_map[(min_x - 1, y)] = infinite_space
        pixel_map[(max_x + 1, y)] = infinite_space
        pixel_map[(min_x - 2, y)] = infinite_space
        pixel_map[(max_x + 2, y)] = infinite_space


# pprint(pixel_map)
# print_map(pixel_map)

steps = 50
infinite_space = '.'
for step in range(steps):
    # Do all calculations on the previous pixel map
    new_light_pixel_map = {}

    pad_with_space(pixel_map)
    # print_map(pixel_map)
    # Find min and max x and y values
    min_x, max_x, min_y, max_y = compute_min_max(pixel_map)

    # First handle all of the inner convolutions, as these do not have any impact on the expansion of the image object
    for y in range(min_y + 1, max_y):
        for x in range(min_x + 1, max_x):
            neighbours = get_neighbours(x, y)
            algorithm_loc = int("".join([pixel_map[n] for n in neighbours]).replace('#', '1').replace('.', '0'), 2)
            new_light_pixel_map[(x, y)] = algorithm[algorithm_loc]

    if infinite_space == '.' and algorithm[0] == '#':
        infinite_space = '#'
    elif infinite_space == '#' and algorithm[-1] == '.':
        infinite_space = '.'

    pixel_map = new_light_pixel_map

    # print(f'Step {step}')
    # print_map(pixel_map)

# pad_with_space(pixel_map)
# print_map(pixel_map)

print(np.count_nonzero(np.array(list(pixel_map.values())) == '#'))
