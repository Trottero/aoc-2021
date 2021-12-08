import numpy as np

with open('./08/data.txt', 'r') as f:
    data = f.readlines()

parsed = []
for line in data:
    line = np.array(line.split(' '), dtype=str)
    mask = line != '|'
    line = line[mask]
    if(line[-1][-1] == '\n'):
        line[-1] = line[-1][:-1]

    parsed.append((line[:10], line[10:]))

# print(len(parsed))
# print(parsed[0])

no_segments = {
    0: 6,  # Conflicts with 6 and 9
    1: 2,  # Unqiue -> 9, 3, 0
    2: 5,  # Conflicts with 3 and 5
    3: 5,  # Conflicts with 2 and 5
    4: 4,  # Unqiue -> 9
    5: 5,  # Conflicts with 2 and 3
    6: 6,  # Conflicts with 0 and 9
    7: 3,  # Unqiue -> 9, 3, 0
    8: 7,  # Unique, Useless
    9: 6,  # Conflicts with 0 and 6
}
# if 1 or 7 is found, we can identify all the 3s

segments = {
    0: [1, 2, 3, 5, 6, 7],
    1: [3, 6],
    2: [1, 3, 4, 5, 7],
    3: [1, 3, 4, 6, 7],
    4: [2, 3, 4, 6],
    5: [1, 2, 4, 6, 7],
    6: [1, 2, 4, 5, 6, 7],
    7: [1, 3, 6],
    8: [1, 2, 3, 4, 5, 6, 7],
    9: [1, 2, 3, 4, 6, 7],
}

# Key: number, Value: list of possible parents based on positions
relations = {
    0: [8],
    1: [0, 3, 4, 7, 8, 9],
    2: [8],
    3: [8, 9],
    4: [8, 9],
    5: [6, 8, 9],
    6: [8],
    7: [0, 3, 8, 9],
    8: [],
    9: [8]
}

# Sanity check
for k, l in no_segments.items():
    if l != len(segments[k]):
        print(f'INVALID SEGMENTS OR SMTH: {k}')


def is_parent(parent, child):
    # Check if all elements in child are atleast in parent
    return all(c in parent for c in child)


def is_equal(first, second):
    return is_parent(first, second) and is_parent(second, first)


def filter_by_len(key, options):
    return [p for p in options if len(key) == no_segments[p]]


s = 0
for input, output in parsed:
    # print(input, output)
    all_values = [*input, *output]
    all_values = {value: np.arange(10) for value in all_values}

    all_values = {key: filter_by_len(key, values) for key, values in all_values.items()}

    x = 0
    all_values = dict(sorted(all_values.items(), key=lambda x: len(x[1])))

    number = 0
    while not all(len(values) == 1 for values in all_values.values()) and x < 10:
        for key, val in all_values.items():
            # If solved and not eight.
            if len(val) == 1 and not val[0] == 8:
                for ki, vi in all_values.items():
                    if is_equal(ki, key):
                        if len(vi) > 1:
                            all_values[ki] = val.copy()
                        continue

                    if is_parent(ki, key):
                        all_values[ki] = [op for op in vi if op in relations[val[0]]]

                    all_values[ki] = [op for op in all_values[ki] if op != val[0]]

                    if all_values[ki] == [2, 5] or all_values[ki] == [5, 2]:
                        if val[0] == 9 and is_parent(key, ki):
                            all_values[ki] = [5]
        x += 1
    print(all_values)
    if x > 10:
        print('ERROR')
        break

    for i, x in enumerate(output[::-1]):
        # print(output, x)
        number += 10**i * all_values[x][0]
    s += number
print(s)
