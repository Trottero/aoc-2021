import numpy as np

data = np.loadtxt('./02/data.txt', dtype='object')

print(len(data))


class Submarine():

    def __init__(self, horizontal, aim, depth):
        self.horizontal = horizontal
        self.aim = aim
        self.depth = depth

        self.actions = {
            'forward':  self.forward,
            'down': self.down,
            'up': self.up,
        }

    def instruction(self, instruction):
        action = instruction[0]
        args = instruction[1:]
        self.actions[action](*args)

    def forward(self, depth):
        self.horizontal += int(depth)
        self.depth += self.aim * int(depth)

    def down(self, aim):
        self.aim += int(aim)

    def up(self, aim):
        self.down(-int(aim))


sub = Submarine(0, 0, 0)
for i in data:
    sub.instruction(i)

print(sub.horizontal * sub.depth)
