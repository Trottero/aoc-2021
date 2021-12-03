import numpy as np

data = np.loadtxt('./03/data.txt', dtype=str)


def to_array(x):
    return np.array(list(x), dtype=int)


processed = []
for l in data:
    processed.append(to_array(l))

processed = np.array(processed)
print(processed[0])

oxygen = np.copy(processed)

for bitpos in range(len(oxygen[0])):
    nn = np.count_nonzero(oxygen, axis=0)

    mostcommon = (nn >= len(oxygen) / 2).astype(int)[bitpos]
    filter = oxygen[:, bitpos] == mostcommon
    oxygen = oxygen[filter]
    if len(oxygen) == 1:
        break

print(oxygen)

co2 = np.copy(processed)
for bitpos in range(len(co2[0])):
    nn = np.count_nonzero(co2, axis=0)

    leastcommon = (~(nn >= len(co2) / 2)).astype(int)[bitpos]
    filter = co2[:, bitpos] == leastcommon
    co2 = co2[filter]
    if len(co2) == 1:
        break

print(co2)


def bits_to_int(r):
    return int("".join(r.astype(str)), 2)


print(bits_to_int(co2[0]) * bits_to_int(oxygen[0]))
