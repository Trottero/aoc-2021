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
    while probe_x <= x2:
        # Check if probe x lands into area
        if probe_x >= x1 and probe_x <= x2:
            steps.append(drag)
            if velocity == 0:
                return steps, True
        if velocity == 0:
            return steps, False

        velocity = max(initial_velocity - drag, 0)
        probe_x += velocity
        drag += 1

    return steps, False


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


feasible_steps = {'any_step_past': []}
x_solutions = []
potential_x = 1

while potential_x < x2 + 1:
    steps, special = simulate_x(potential_x)
    if len(steps) > 0:
        x_solutions.append(potential_x)
        for step in steps:
            if step not in feasible_steps.keys():
                feasible_steps[step] = {'x': [], 'y': []}
            feasible_steps[step]['x'].append(potential_x)

        if special:
            feasible_steps['any_step_past'].append((potential_x, np.max(steps)))

    potential_x += 1

print(x_solutions)

print(feasible_steps)

y_solutions = []
potential_y = -abs(min(y1, y2))

combinations = []

while potential_y < abs(min(y1, y2) * 10):
    steps = simulate_y(potential_y)
    if len(steps) > 0:
        y_solutions.append(potential_y)
        for step in steps:
            if step in feasible_steps.keys():
                for x in feasible_steps[step]['x']:
                    combinations.append((x, potential_y))

            # Also check if its on the any step past list
            for x, stepy in feasible_steps['any_step_past']:
                if step > stepy:
                    combinations.append((x, potential_y))
    potential_y += 1

print(y_solutions)
print(compute_top_height(y_solutions[-1]))

print()
print(list(sorted(combinations, key=lambda x: x[0])))
print(len(set(combinations)))
