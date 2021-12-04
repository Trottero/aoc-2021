import numpy as np
import os
import pandas as pd


def get_score_for_board(board, marked):
    inverted = np.invert(marked)
    return np.sum(board[inverted])


with open('./04/data.txt', 'r') as f:
    lines = f.readlines()
    numbers = [int(n) for n in lines[0].split(',')]

    boards = []
    current_board = []
    for line in lines[2:]:
        if line == '\n':
            boards.append(np.array(current_board))
            current_board = []
            continue

        line = line.replace('  ', ' ').strip()
        # Append row to board
        current_board.append(np.array([int(n) for n in line.split(' ')]))

    boards.append(np.array(current_board))

    boards = np.array(boards)
    print(boards.shape)

    board_size = boards.shape[1]
    marked_numbers = np.full(boards.shape, False)

    winning_order = []

    for number in numbers:
        # Update the numbers drawn with equality checjks to current number
        marked_numbers = np.logical_or(marked_numbers, boards == number)
        # Check for wins
        counts_y = np.count_nonzero(marked_numbers, axis=1)
        winning_boards_y = np.argwhere(counts_y == board_size)

        counts_x = np.count_nonzero(marked_numbers, axis=2)
        winning_boards_x = np.argwhere(counts_x == board_size)

        winning_boards = np.concatenate((winning_boards_y, winning_boards_x), axis=0)

        if winning_boards.size > 0:
            winning_order = np.concatenate((winning_order, winning_boards[:, 0]))
            winning_order = pd.unique(winning_order)

        # All boards finished
        if len(winning_order) == boards.shape[0]:
            print(winning_order)
            break


last_board = int(winning_order[-1])
score = get_score_for_board(boards[last_board], marked_numbers[last_board])

print(score * number)
