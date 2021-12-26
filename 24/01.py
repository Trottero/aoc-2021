import numpy as np
from pprint import pprint
import tqdm
import sys
import networkx as nx
from copy import deepcopy

data = []
with open('./24/data.txt', 'r') as f:
    for line in f:
        l = line.strip()
        l = l.split(' ')
        instruction = l[0]
        args = l[1:]
        data.append((instruction, args))

print(data)
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


def validate_number():
    for instruction, args in data:
        instructions[instruction](*args)
    return memory['z']


max_n = 999_999_999_999_99

for n in range(max_n, 0, -1):
    if '0' in str(n):
        continue
    reset_memory()
    input_seq = str(n)
    if validate_number() == 0:
        print(n)
        break
