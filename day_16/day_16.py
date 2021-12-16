from pathlib import Path
from typing import List, Tuple

import numpy as np

code = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def convert_to_binary(cipher: str) -> str:
    return "".join([code[c] for c in cipher])


data = Path(__file__).with_name("input_ex.txt").read_text()
binary = convert_to_binary(data)
print(binary)


def get_package_version(binary: str, pointer: int) -> int:
    return int(binary[pointer : pointer + 3], 2)


def get_packet_type(binary: str, pointer: int) -> int:
    return int(binary[pointer : pointer + 3], 2)


def read_literal_value(binary: str, pointer: int) -> Tuple[int, int]:
    binary_value = ""
    while binary[pointer] == "1":
        binary_value += binary[pointer + 1 : pointer + 5]
        pointer += 5
    # leading number was 0
    binary_value += binary[pointer + 1 : pointer + 5]
    pointer += 5

    decimal = int(binary_value, 2)
    return decimal, pointer


def apply_package_operation(decimals: List[int], package_type: int) -> int:
    if package_type == 0:
        decimal = sum(decimals)
    elif package_type == 1:
        decimal = np.prod(decimals)
    elif package_type == 2:
        decimal = np.min(decimals)
    elif package_type == 3:
        decimal = np.max(decimals)
    elif package_type == 5:
        decimal = decimals[0] > decimals[1]
    elif package_type == 6:
        decimal = decimals[0] < decimals[1]
    elif package_type == 7:
        decimal = decimals[0] == decimals[1]
    else:
        # Here package_type is 4
        decimal = decimals[0]
    return decimal


def decipher(binary: str) -> Tuple[int, int, int]:
    pointer = 0
    total_package_version = get_package_version(binary, pointer)
    pointer += 3
    package_type = get_packet_type(binary, pointer)
    pointer += 3

    decimals = []
    if package_type == 4:
        # is literal value -> read 5 bits until 0 is leading
        decimal, pointer = read_literal_value(binary, pointer)
        decimals += [decimal]
    else:
        # operator
        length_type_id = binary[pointer]
        pointer += 1
        if length_type_id == "0":
            total_length_sub_pakets = int(binary[pointer : pointer + 15], 2)
            pointer += 15
            pointer_old = pointer
            while pointer < pointer_old + total_length_sub_pakets:
                decimals_sub, package_version, pointer_sub = decipher(binary[pointer:])
                decimals += [decimals_sub]
                total_package_version += package_version
                pointer += pointer_sub
        else:
            # length_type_id = "1"
            number_sub_pakets = int(binary[pointer : pointer + 11], 2)
            pointer += 11
            for _ in range(number_sub_pakets):
                decimals_sub, package_version, pointer_sub = decipher(binary[pointer:])
                total_package_version += package_version
                decimals += [decimals_sub]
                pointer += pointer_sub

    # Calculate final decimal
    decimal = apply_package_operation(decimals, package_type)

    return decimal, total_package_version, pointer


decimal, _, _ = decipher(binary)
assert decimal == 2021

data = Path(__file__).with_name("input_ex2.txt").read_text()
binary = convert_to_binary(data)
decipher(binary)

data = Path(__file__).with_name("input_ex3.txt").read_text()
binary = convert_to_binary(data)
decipher(binary)

# add up all version numbers
binary = convert_to_binary("8A004A801A8002F478")
_, sum_package_version, _ = decipher(binary)
assert sum_package_version == 16

binary = convert_to_binary("620080001611562C8802118E34")
_, sum_package_version, _ = decipher(binary)
assert sum_package_version == 12

binary = convert_to_binary("C0015000016115A2E0802F182340")
_, sum_package_version, _ = decipher(binary)
assert sum_package_version == 23

binary = convert_to_binary("A0016C880162017C3686B18A3D4780")
_, sum_package_version, _ = decipher(binary)
assert sum_package_version == 31

data = Path(__file__).with_name("input.txt").read_text()
binary = convert_to_binary(data)
decimal, sum_package_version, _ = decipher(binary)
print(sum_package_version)

# Part two
print(decimal)
