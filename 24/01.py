import numpy as np
from pprint import pprint
import tqdm
import sys
import networkx as nx
from copy import deepcopy
from tqdm import trange

data = []
with open('./24/data.txt', 'r') as f:
    for line in f:
        l = line.strip()
        l = l.split(' ')
        instruction = l[0]
        args = l[1:]
        data.append((instruction, args))

memory = {'x': 0, 'y': 0, 'z': 0, 'w': 0}

input_seq = ""
input_ptr = 0


def input(var):
    global input_ptr
    memory[var] = int(input_seq[input_ptr])
    input_ptr += 1


def add(a, b):
    if b.lstrip('-').isnumeric():
        b = int(b)
    else:
        b = memory[b]
    memory[a] = memory[a] + b


def mod(a, b):
    if b.lstrip('-').isnumeric():
        b = int(b)
    else:
        b = memory[b]
    memory[a] = memory[a] % b


def mul(a, b):
    if b.lstrip('-').isnumeric():
        b = int(b)
    else:
        b = memory[b]
    memory[a] = memory[a] * b


def div(a, b):
    if b.lstrip('-').isnumeric():
        b = int(b)
    else:
        b = memory[b]
    memory[a] = memory[a] // b


def eql(a, b):
    if b.lstrip('-').isnumeric():
        b = int(b)
    else:
        b = memory[b]
    memory[a] = int(memory[a] == b)


instructions = {
    'inp': input,
    'add': add,
    'mod': mod,
    'mul': mul,
    'div': div,
    'eql': eql,
}


def reset_memory():
    global input_ptr
    global memory
    memory = {'x': 0, 'y': 0, 'z': 0, 'w': 0}
    input_ptr = 0


def get_program_block(block):
    inputs = 0
    program = []
    for instruction, args in data:
        if instruction == 'inp':
            inputs += 1
        if inputs == block:
            program.append((instruction, args))
        if inputs > block:
            break
    return program


def validate_number(block, seq):
    global input_seq
    input_seq = seq
    for instruction, args in get_program_block(block):
        instructions[instruction](*args)
    return memory['z']


# possibilities = {0: ['']}

# vocabulary = np.arange(1, 10)
# print(vocabulary)
# for block in trange(1, 15):
#     new_possibilities = []
#     # All of the previous passing numbers
#     for p in possibilities[block - 1]:
#         # Brute force the new numbers
#         for i in vocabulary:
#             if validate_number(block, p + str(i)) == 0:
#                 new_possibilities.append(p + str(i))
#     print(possibilities)
#     # Make options bigger
#     possibilities[block] = new_possibilities

search_space = {
    'z': range(-500, 500),
    'w': range(1, 10),
}

# Block, z
# Only possibility for block 15 is z = 0 as input
options = {15: [(0, '')]}


def bruteforce_z_for_block(block, z):
    zw_comps = []
    for zsearch in search_space['z']:
        for w in search_space['w']:
            reset_memory()
            memory['z'] = zsearch
            if validate_number(block, str(w)) == z:
                zw_comps.append((zsearch, w))
    return zw_comps


for block in trange(14, 0, -1):
    options[block] = []
    # Get all options for the previously computed block
    for targetz, w in options[block + 1]:
        comps = bruteforce_z_for_block(block, targetz)
        for inz, inw in comps:
            options[block].append((inz, str(inw) + w))

    unique = {}
    for targetz, w in options[block]:
        if targetz in unique:
            if int(w) > int(unique[targetz]):
                unique[targetz] = w
        else:
            unique[targetz] = w

    options[block] = [(z, w) for z, w in unique.items()]

max = 0
for k, v in options.items():
    print(k, len(v))

for o, w in options[3]:
    if int(w) > max:
        max = int(w)

print(max)
# 979989699879
