from pathlib import Path

import numpy as np


def part_one():
    my_arr = np.loadtxt(str(Path(__file__).parent / "input.txt"))
    print("Increasing: ", sum(np.diff(my_arr) > 0))


def part_two():
    my_arr = np.loadtxt(str(Path(__file__).parent / "input.txt"))
    # my_arr_test = np.array([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])
    avg = [sum(my_arr[i : i + 3]) for i in np.arange(len(my_arr) - 2)]
    diff = np.diff(avg)
    print(diff, len(diff))
    print("Increasing rolling window: ", sum(diff > 0))


if __name__ == "__main__":
    part_one()
    # One-liner:
    print("Increasing: ", sum(np.diff(np.loadtxt(str(Path(__file__).parent / "input.txt"))) > 0))

    part_two()
