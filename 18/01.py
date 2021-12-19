import numpy as np

data = np.loadtxt('./18/data.txt', dtype=object)

print(data)


class Node():
    def __init__(self, left, right, value):
        self.left = left
        self.right = right
        self.value = value

    pass

    def preorder(self):
        if self.left is None and self.right is None:
            print(self.value)
            return
        self.left.preorder()
        self.right.preorder()


def parse_snail_number(part):
    i = 0
    while part[i] == ',' or part[i] == ']':
        i += 1

    c = part[i]
    if c.isdigit():
        return Node(None, None, int(c)), i

    if c == '[':
        i += 1
        # Find left subtree
        left, skip = parse_snail_number(part[i:])
        print('Left:', left.value, skip)
        i += skip + 1
        right, skip = parse_snail_number(part[i:])
        print('Right: ', left.value, skip)
        return Node(left, right, None), i

    return None


n = 1
print(data[n])
tree, i = parse_snail_number(data[n])
print(tree.left.value, tree.right.value)
tree.preorder()
