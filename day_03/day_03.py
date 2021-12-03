import numpy as np


def binary2decimal(binary) -> int:
    """Convert binary code to decimal"""
    number = 0
    exponent = 1
    for bit in binary[::-1]:
        number += exponent * int(bit)
        exponent *= 2
    return number


def part_one(arr_np):
    occurrences = arr_np.sum(0)
    most_common = [1 if amount >= len(arr_np) / 2 else 0 for amount in occurrences]
    least_common = [0 if amount >= len(arr_np) / 2 else 1 for amount in occurrences]

    assert binary2decimal("10110") == 22

    print("gamma_rate:", most_common, "in decimal:", binary2decimal(most_common))
    print("epsilon_rate:", least_common, "in decimal:", binary2decimal(least_common))
    print("power consumption: ", binary2decimal(most_common) * binary2decimal(least_common))


def get_oxygen_rating(arr_np):
    my_copy = arr_np.copy()
    column = 0
    while len(my_copy) > 1:
        amount_ones = my_copy[:, column].sum()
        # keep only those that have the most occurrences
        if amount_ones >= len(my_copy) / 2:
            my_copy = my_copy[my_copy[:, column] == 1]
        else:
            my_copy = my_copy[my_copy[:, column] == 0]
        column += 1
    return my_copy.ravel()


def get_co2_scrubber_rating(arr_np):
    my_copy = arr_np.copy()
    column = 0
    while len(my_copy) > 1:
        amount_ones = my_copy[:, column].sum()
        # keep only those that have the least occurrences
        if amount_ones >= len(my_copy) / 2:
            my_copy = my_copy[my_copy[:, column] == 0]
        else:
            my_copy = my_copy[my_copy[:, column] == 1]
        column += 1
    return my_copy.ravel()


def part_two(arr_np):
    oxygen = get_oxygen_rating(arr_np)
    co2 = get_co2_scrubber_rating(arr_np)
    print("Oxygen rating", oxygen, binary2decimal(oxygen))
    print("co2_scrubber rating", co2, binary2decimal(co2))
    print("life support rating:", binary2decimal(oxygen) * binary2decimal(co2))


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        arr = f.readlines()
    arr_str = [binary.strip() for binary in arr]
    arr_np = np.zeros((len(arr_str), len(arr_str[0])), int)
    for i, binary in enumerate(arr_str):
        arr_np[i] = list(binary)

    part_one(arr_np)
    print()
    part_two(arr_np)
