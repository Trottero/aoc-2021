import numpy as np
import copy
import tqdm

data = np.loadtxt('./18/data.txt', dtype=object)

print(data)


class Node():
    def __init__(self, left=None, right=None, value=None, parent=None):
        self.set_left(left)
        self.set_right(right)
        self.value = value
        self.parent = parent

    pass

    def preorder(self):
        if self.left is None and self.right is None:
            return str(self.value)
        return f'[{self.left.preorder()},{self.right.preorder()}]'

    def explode(self, depth=0, root_left=True, root_right=True):
        if self.left is None and self.right is None:
            return depth > 4, False

        # Non terminal, continue traversing
        left_explode, already_exploded = self.left.explode(depth + 1, root_left, False)
        if already_exploded:
            return False, True
        right_explode, already_exploded = self.right.explode(depth + 1, False, root_right)
        if already_exploded:
            return False, True

        if left_explode and right_explode:
            # Both left and right al child nodes
            if not root_left:
                sibling = self.get_left_sibling()
                sibling.value += self.left.value
            if not root_right:
                sibling = self.get_right_sibling()
                sibling.value += self.right.value

            self.value = 0
            self.left = None
            self.right = None

        return False, left_explode or right_explode

    def split(self):
        if self.left is None and self.right is None:
            # Terminal node, check if we should split
            if self.value < 10:
                return False
            # Split the node
            self.set_left(Node(value=self.value // 2))
            self.set_right(Node(value=(self.value + 1) // 2))
            self.value = None
            return True

        # Non terminal, continue traversing
        if self.left.split():
            return True
        return self.right.split()

    def set_left(self, left):
        self.left = left
        if self.left is not None:
            self.left.parent = self

    def set_right(self, right):
        self.right = right
        if self.right is not None:
            self.right.parent = self

    def get_left_sibling(self):
        node = self
        prev = self
        while True:
            if node.parent is None:
                return None
            node = node.parent
            if node.right is prev:
                return node.left.get_right_most()
            prev = node

    def get_right_sibling(self):
        node = self
        prev = self
        while True:
            if node.parent is None:
                return None
            node = node.parent
            if node.left == prev:
                return node.right.get_left_most()
            prev = node

    def get_left_most(self):
        if self.left is None:
            return self
        return self.left.get_left_most()

    def get_right_most(self):
        if self.right is None:
            return self
        return self.right.get_right_most()

    def reduce(self):
        reduced = True
        while reduced:
            reduced = False
            _, reduced = self.explode()
            if reduced:
                continue
            reduced = self.split()

    def magnitude(self):
        if self.left is None and self.right is None:
            return self.value
        return 3*self.left.magnitude() + 2 * self.right.magnitude()

    def __add__(self, node):
        return Node(left=self, right=node)

    def __eq__(self, obj):
        return isinstance(obj, Node) and self.preorder() == obj.preorder()

    def __ne__(self, obj):
        return not self == obj


def parse_snail_number(part, parent=None):
    i = 0
    while part[i] == ',' or part[i] == ']':
        i += 1

    c = part[i]
    if c.isdigit():
        return Node(value=int(c), parent=parent), i + 1

    if c == '[':
        node = Node(parent=parent)
        i += 1
        # Find left subtree
        left, skip = parse_snail_number(part[i:], node)
        i += skip + 1
        right, skip = parse_snail_number(part[i:], node)

        node.set_left(left)
        node.set_right(right)

        return node, i + skip

    return None


max = 0
for number1 in tqdm.tqdm(data):
    for number2 in data:
        sn1, _ = parse_snail_number(number1)
        sn2, _ = parse_snail_number(number2)
        if sn1 == sn2:
            continue
        sn3 = sn1 + sn2
        sn3.reduce()
        sn3mag = sn3.magnitude()
        if sn3mag > max:
            max = sn3mag

        sn1, _ = parse_snail_number(number1)
        sn2, _ = parse_snail_number(number2)
        sn3 = sn2 + sn1
        sn3.reduce()
        sn3mag = sn3.magnitude()
        if sn3mag > max:
            max = sn3mag

print(max)
