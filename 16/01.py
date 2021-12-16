import numpy as np
from collections import Counter
import networkx as nx

hex_to_bin = {
    '0': [0, 0, 0, 0],
    '1': [0, 0, 0, 1],
    '2': [0, 0, 1, 0],
    '3': [0, 0, 1, 1],
    '4': [0, 1, 0, 0],
    '5': [0, 1, 0, 1],
    '6': [0, 1, 1, 0],
    '7': [0, 1, 1, 1],
    '8': [1, 0, 0, 0],
    '9': [1, 0, 0, 1],
    'A': [1, 0, 1, 0],
    'B': [1, 0, 1, 1],
    'C': [1, 1, 0, 0],
    'D': [1, 1, 0, 1],
    'E': [1, 1, 1, 0],
    'F': [1, 1, 1, 1],
}

with open('./16/data.txt', 'r') as f:
    data = f.readlines()[0]

bit_program = []
for i in data:
    bit_program.extend(hex_to_bin[i])
bit_program = np.array(bit_program)

print(bit_program)

version_length = 3
packet_type_length = 3


def bin_to_dec(seq):
    return int("".join(seq.astype(str)), 2)


def parse_packet(packet):
    version = bin_to_dec(packet[:version_length])
    packet_type = bin_to_dec(packet[version_length:version_length + packet_type_length])

    payload = packet[version_length + packet_type_length:]
    number, ptr = parse_payload(version, packet_type, payload)
    return number, ptr + version_length + packet_type_length


def parse_payload(version, type, payload):
    # Track the movement from this packet
    number = version
    ptr = 0
    if type == 4:
        splits, ptr = split_payload(payload, 5)
        # Remove leading bit
        splits = splits[:, 1:]
        number = bin_to_dec(splits.flatten())
        return version, ptr

    # Not a literal number and thus we need to recursively parse subpackets
    length_type = payload[ptr]
    ptr += 1
    if length_type == 0:  # Length in bits
        length = bin_to_dec(payload[ptr:ptr + 15])
        ptr += 15
    else:  # Length in packets
        length = bin_to_dec(payload[ptr:ptr + 11])
        ptr += 11

    if length_type == 0:
        start = ptr
        while ptr - start != length:
            returnval, skip = parse_packet(payload[ptr:])
            ptr += skip
            number += returnval

    if length_type == 1:
        for _ in range(length):
            returnval, skip = parse_packet(payload[ptr:])
            ptr += skip
            number += returnval

    return number, ptr


def split_payload(payload, length):
    # Split the payload by length n and return
    splits = []
    for i in range(0, len(payload) + length, length):
        splits.append(payload[i:i + length])
        if payload[i] == 0:
            ptr = np.sum([len(x) for x in splits])
            if len(splits[-1]) != length:
                splits.remove(splits[-1])
            break

    return np.array(splits), ptr


print(parse_packet(bit_program))
