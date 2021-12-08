import numpy as np

data = np.loadtxt('./08/data.txt', dtype=str)

no_segments = {
    1: 2,
    4: 4,
    7: 3,
    8: 7
}

parsed = []
for line in data:
    mask = line != '|'
    line = line[mask]

    parsed.append((line[:10], line[10:]))

print(len(parsed))
print(parsed[0])
s = 0
for input, output in parsed:
    # print(input)
    # print(output)

    for o in output:
        if len(o) in no_segments.values():
            s += 1

print(s)
