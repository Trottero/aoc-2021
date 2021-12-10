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
                return False, []
    if len(stack) == 0:
        return True, []
    # Corrupt string

    tokens = []
    for _ in range(len(stack)):
        tokens.append(characters[stack.pop()])
    return False, tokens


values = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}
scores = []
for l in data:
    valid, char = determine_first_invalid_char(l)
    if not valid and len(char) != 0:
        # print(char)
        s = 0
        for c in char:
            s *= 5
            s += values[c]
        scores.append(s)

print(np.median(scores))
