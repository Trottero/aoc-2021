import numpy as np

with open('./17/data.txt', 'r') as f:
    data = f.readlines()[0].split(' ')[-2:]

data[0] = data[0][:-1]

data = [[int(co) for co in c.split('=')[1].split('..')] for c in data]

print(data)

x1, x2 = data[0]
y1, y2 = data[1]


def simulate_x(initial_velocity):
    probe_x = 0
    drag = 0
    velocity = initial_velocity
    steps = []
    while probe_x <= x2 and velocity > 0:
        # Check if probe x lands into area
        if probe_x >= x1 and probe_x <= x2:
            steps.append(drag)

        velocity = max(initial_velocity - drag, 0)
        probe_x += velocity
        drag += 1

    return steps


def simulate_y(initial_velocity):
    probe_y = 0
    drag = 0
    velocity = initial_velocity
    steps = []
    while True:
        # Check if probe y lands into area
        if probe_y >= min(y1, y2) and probe_y <= max(y1, y2):
            steps.append(drag)

        if velocity < 0 and probe_y < min(y1, y2):
            return steps

        velocity = initial_velocity - drag

        probe_y += velocity
        drag += 1


def compute_top_height(initial_y):
    return np.sum([initial_y - i for i in range(0, initial_y)])


feasible_steps = {}
x_solutions = []
potential_x = 1

while potential_x < x2 + 1:
    steps = simulate_x(potential_x)
    if len(steps) > 0:
        x_solutions.append(potential_x)
        for step in steps:
            feasible_steps[step] = True
    potential_x += 1

print(x_solutions)

max_steps = np.max(list(feasible_steps.keys()))

print(max_steps)
y_solutions = []
potential_y = -abs(min(y1, y2))

while potential_y < abs(min(y1, y2) * 10):
    steps = simulate_y(potential_y)
    if len(steps) > 0:
        y_solutions.append(potential_y)
    potential_y += 1

print(y_solutions)

print(compute_top_height(y_solutions[-1]))
