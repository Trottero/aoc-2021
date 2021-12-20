from os import link
import numpy as np
import pprint
import networkx as nx
import tqdm
from multiprocessing import Pool, TimeoutError
import time
import os
from tqdm.contrib.concurrent import process_map

# Use vectors,
# Every beacon has a relation to other beacons
# Use this relation to compute patterns in beacons for which we can look in other scanners

# Patterns are defined as follows:
# For every beacon found in a scanner
#   - Calculate offset to every other beacon

# We can then rotate these offsets to potentially get patterns for other beacons
# Use this to determine the location of unique beacons relative to the first scanner


def get_patterns(beacons):
    # Gets all beacon patterns for a specific scanner
    patterns = {}
    # For every beacon in this set
    for source in beacons:
        patterns[tuple(source)] = []
        # Compute offset to every other beacon
        for target in beacons:
            if all(a == b for a, b in zip(source, target)):
                continue
            offset = target - source
            patterns[tuple(source)].append(offset)

        patterns[tuple(source)] = np.array(patterns[tuple(source)])

    return patterns


def get_x_matrix(angle):
    rad = np.radians(angle)
    return np.array([[1, 0, 0], [0, np.cos(rad), -np.sin(rad)], [0, np.sin(rad), np.cos(rad)]])


def get_y_matrix(angle):
    rad = np.radians(angle)
    return np.array([[np.cos(rad), 0, np.sin(rad)], [0, 1, 0], [-np.sin(rad), 0, np.cos(rad)]])


def get_z_matrix(angle):
    rad = np.radians(angle)
    return np.array([[np.cos(rad), -np.sin(rad), 0], [np.sin(rad), np.cos(rad), 0], [0, 0, 1]])


def rotate(coords, xrot, yrot, zrot):
    return np.round(coords @ get_x_matrix(xrot) @ get_y_matrix(yrot) @ get_z_matrix(zrot))


def rotate_patterns(patterns, xrot, yrot, zrot):
    # Allows use to rotate a pattern into one of 4 * 4 * 4 offsets
    rotations = {}
    for key in patterns.keys():
        # Rotate key
        xyz = rotate(key, xrot, yrot, zrot)
        # Rotate offsets
        rotations[tuple(xyz)] = rotate(patterns[key], xrot, yrot, zrot)
    return rotations


def search_overlap(pattern1, pattern2):
    # Find overlaps between two sets of patterns by rotating the second set around.
    rots = [0, 90, 180, 270]
    for xrot in rots:
        for yrot in rots:
            for zrot in rots:
                rotated_pattern2 = rotate_patterns(pattern2, xrot, yrot, zrot)
                count, similar_beacons = overlap_count(pattern1, rotated_pattern2)
                if count >= 12:
                    # Found enough similar beacons
                    # Calculate the second scanners position based on the first
                    (x1, y1, z1), (x2, y2, z2) = similar_beacons[0]
                    return count, (x1 - x2, y1 - y2, z1 - z2), (xrot, yrot, zrot)
    return None, [], ()


def unique2D_subarray(a):
    dtype1 = np.dtype((np.void, a.dtype.itemsize * np.prod(a.shape[1:])))
    b = np.ascontiguousarray(a.reshape(a.shape[0], -1)).view(dtype1)
    return a[np.unique(b, return_index=1)[1]]


def overlap_count(scanner1_patterns, scanner2_patterns):
    # Find how many of scanner1_patterns exist in scanner2_patterns:
    similar_beacons = []
    for k1, offsets1 in scanner1_patterns.items():
        for k2, offsets2 in scanner2_patterns.items():
            expected_amount = len(offsets1) + len(offsets2)
            combined = np.concatenate((offsets1, offsets2))
            nodupes = unique2D_subarray(combined).shape[0]
            if expected_amount - nodupes >= 11:
                similar_beacons.append((k1, k2))
    return len(similar_beacons), similar_beacons


def overlap_wrapper(arg):
    p1, p2, i, j = arg
    overlapping, offset, rot = search_overlap(p1, p2)
    return overlapping, offset, rot, i, j


if __name__ == '__main__':
    # Parse data
    with open('./19/data.txt', 'r') as f:
        lines = f.readlines()

        scanners = []
        scanner_beacons = []
        for line in lines:
            line = line.strip()
            if line.startswith('---'):
                continue
            if line == '':
                scanners.append(scanner_beacons)
                scanner_beacons = []
                continue
            beacon = np.fromstring(line, dtype=int, sep=',')
            scanner_beacons.append(beacon)
        scanners.append(scanner_beacons)
        scanners = [np.array(beacons) for beacons in scanners]

    print('No. scanners: ', len(scanners))

    # Generate multiprocessing args
    args = []
    for i, scanner1 in enumerate(scanners):
        for j, scanner2 in enumerate(scanners):
            if i == j:
                continue
            args.append((get_patterns(scanner1), get_patterns(scanner2), i, j))

    results = process_map(overlap_wrapper, args, max_workers=16, chunksize=10)

    # Key dependency a -> b
    # Value relative rotation and position
    links = {}
    G = nx.DiGraph()
    for overlapping, offset, rot, i, j in results:
        if overlapping is not None:
            links[(i, j)] = (np.array(offset), rot)
            G.add_edge(i, j)

    relative_to_zero = {}
    rotated_scanners = []
    for scanner in range(len(scanners)):
        if scanner == 0:
            relative_to_zero[scanner] = np.array([0, 0, 0])
            rotated_scanners.append(scanners[scanner])
            continue

        path = nx.algorithms.shortest_path(G, source=scanner, target=0)

        # Calculate relative position to zero
        current_coord, rot = links[(path[1], path[0])]
        rotated_beacons = rotate(scanners[scanner], *rot)
        for i, node in enumerate(path[1:-1]):
            offset, (x, y, z) = links[(path[i + 2], node)]
            current_coord = rotate(current_coord, x, y, z) + offset
            rotated_beacons = rotate(rotated_beacons, x, y, z)
        relative_to_zero[scanner] = current_coord
        rotated_scanners.append(rotated_beacons)

    pprint.pprint(relative_to_zero)

    # print(np.round(
    #     # Take value between 4 to 2, multiply by value 1 to 4 and add 1 to 4 to transpose to 1
    #     (np.array([168.0, -1125.0, 72.0]) @ get_y_matrix(270) @ get_z_matrix(90) + [88.0, 113.0, -1104.0])
    #     # Bring from 1 to 0
    #     @ get_y_matrix(180) + [68, -1246, -43]))

    # Say 4 -> 2 and 1 -> 4 exist
    # We can transpose 4 -> 1 by doing the following steps:
    # 1. Bring 4 to 1 by taking rots from 1 -> 4 and applying them to 4
    # 2. Add the position from 1 -> 4
    # 3. Bring 1 to 0 by taking rots from 0 -> 1 and applying them to 1
    # 4. Add the position from 0 -> 1

    # Get all beacons relative to scanner 0
    relative_beacons = []
    for i, beacons in enumerate(rotated_scanners):
        for beacon in beacons:
            relative_beacons.append(tuple(beacon + relative_to_zero[i]))

    relative_beacons = list(set(relative_beacons))
    print(len(relative_beacons))
