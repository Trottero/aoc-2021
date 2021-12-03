import numpy as np

data = np.loadtxt('./03/data.txt', dtype=str)


def to_array(x):
    return np.array(list(x), dtype=int)


processed = []
for l in data:
    processed.append(to_array(l))

processed = np.array(processed)
print(processed[0])

nn = np.count_nonzero(processed, axis=0)
print(nn)

gamma = (nn > len(processed) / 2)
print(gamma)
gamma_v = int("".join(gamma.astype(int).astype(str)), 2)

epsilon = ~gamma
print(epsilon)
epsilon_v = int("".join(epsilon.astype(int).astype(str)), 2)

print(gamma_v * epsilon_v)
