import numpy as np

data = np.loadtxt('./02/data.txt', dtype='object')

print(len(data))


class Submarine():

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.actions = {
            'forward':  self.forward,
            'down': self.down,
            'up': self.up,
        }

    def instruction(self, instruction):
        action = instruction[0]
        args = instruction[1:]
        self.actions[action](*args)

    def forward(self, x):
        self.x += int(x)

    def down(self, y):
        self.y += int(y)

    def up(self, y):
        self.down(-int(y))


sub = Submarine(0, 0, 0)
for i in data:
    sub.instruction(i)

print(sub.x * sub.y)
