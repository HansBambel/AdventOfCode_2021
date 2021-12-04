import numpy as np
from pathlib import Path
from itertools import groupby
import re

def play_bingo(drawn_numbers, bingo_boards):
    # One after the other draw a number and "activate" it

    # for checking create a boolean mask that has the same shape as bingo boards
    bingo_mask = np.zeros(bingo_boards.shape, dtype=bool)
    print(bingo_mask)
    part_one_done = False
    do_part_two_now = False

    for i, number in enumerate(drawn_numbers):
        # 1. tick number in all bingo boxes
        bingo_mask[np.where(bingo_boards == number)] = True
        # 2. check if row or column sum of a board is 5
        if (bingo_mask.sum(1) == 5).any() or (bingo_mask.sum(2) == 5).any():

            # 3. if so: calc sum of all unactivated numbers of that board and multiply by drawn number
            if len(np.where((bingo_mask.sum(1) == 5))[0]) > 0:
                ind = np.where((bingo_mask.sum(1) == 5))[0][0]
                unactivated_sum = sum(bingo_boards[ind][~bingo_mask[ind]])
            else:
                ind = np.where((bingo_mask.sum(2) == 5))[0][0]
                unactivated_sum = sum(bingo_boards[ind][~bingo_mask[ind]])

            if not part_one_done:
                print(f"After drawing {i} numbers with number: {number}")
                print(f"unactivated_sum: {unactivated_sum}")
                print(f"Total: {unactivated_sum*number}")
                part_one_done = True
            if do_part_two_now:
                print(f"After drawing {i} numbers with number: {number}")
                print(f"unactivated_sum: {unactivated_sum}")
                print(f"Total: {unactivated_sum * number}")
                break

        completed_board_indices = list(set(list(np.where((bingo_mask.sum(1) == 5))[0])
                                           + list(np.where((bingo_mask.sum(2) == 5))[0])))
        if len(completed_board_indices) == 99:
            print("99 boards completed. Next one is the last one.")
            # copy the mask of the last one
            mask = [False if num in completed_board_indices else True for num in range(100)]
            # Set the final board to be the only one that is important
            bingo_mask = bingo_mask[mask]
            bingo_boards = bingo_boards[mask]
            do_part_two_now = True



def create_bingo_boards(input_list):
    # a new bingo board is recognized by a sole linebreak
    splitted_boards = (list(g) for _, g in groupby(input_list, key='\n'.__ne__))
    # remove "\n"
    splitted_boards = [board for board in splitted_boards if "\n" not in board]

    # convert boards to matrix
    bingo_boards_np = np.zeros((len(splitted_boards), 5, 5), dtype=int)
    for i, board in enumerate(splitted_boards):
        # convert every row to an array from the string
        bingo_boards_np[i] = np.stack([np.array(re.findall("\d+", row), dtype=int) for row in board])
    return bingo_boards_np


if __name__ == "__main__":
    with open(Path(__file__).parent / "input.txt", "r") as f:
        drawn_numbers_str = f.readline()
        drawn_numbers = np.array(drawn_numbers_str.split(","), dtype=int)
        print(drawn_numbers)
        # remove linebreak
        f.readline()
        # Read in matrices
        bingo_boards_raw = f.readlines()
        print(bingo_boards_raw)
        created_bingo_boards = create_bingo_boards(bingo_boards_raw)
        print(created_bingo_boards)

    play_bingo(drawn_numbers, created_bingo_boards)
