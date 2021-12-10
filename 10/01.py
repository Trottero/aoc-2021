import numpy as np

data = np.loadtxt('./10/data.txt', dtype=str)


print(len(data))
print(data[0])

characters = {
    '(': ')',
    '<': '>',
    '{': '}',
    '[': ']'
}


def determine_first_invalid_char(line):
    stack = []
    for c in line:
        if c in characters.keys():
            # Add when opening
            stack.append(c)
        else:
            # Pop when closing
            expected = stack.pop()
            expected_closing = characters[expected]
            if c != expected_closing:
                return False, c
    if len(stack) == 0:
        return True, ''
    # Corrupt string
    return False, ''


values = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

chars = []
for l in data:
    valid, char = determine_first_invalid_char(l)
    if not valid and char != '':
        chars.append(char)

v = [values[c] for c in chars]

print(sum(v))
