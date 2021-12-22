import itertools
import re
from pathlib import Path

import numpy as np


def get_turned_on_cubes(data, part_two=False) -> int:
    active_cubes = set()
    for line in data:
        x = re.findall(r"x=(-?\d+)\.\.(-?\d+)", line)[0]
        y = re.findall(r"y=(-?\d+)\.\.(-?\d+)", line)[0]
        z = re.findall(r"z=(-?\d+)\.\.(-?\d+)", line)[0]

        if not part_two:
            min_val, max_val = -50, 50
            x = np.arange(max(int(x[0]), min_val), min(int(x[1]), max_val) + 1)
            y = np.arange(max(int(y[0]), min_val), min(int(y[1]), max_val) + 1)
            z = np.arange(max(int(z[0]), min_val), min(int(z[1]), max_val) + 1)
        else:
            x = np.arange(int(x[0]), int(x[1]) + 1)
            y = np.arange(int(y[0]), int(y[1]) + 1)
            z = np.arange(int(z[0]), int(z[1]) + 1)

        cubes = itertools.product(x, y, z)
        if line.startswith("on"):
            for cube in cubes:
                active_cubes.add(cube)
        else:
            for cube in cubes:
                active_cubes.discard(cube)
    return len(active_cubes)


print("ex1")
data = Path(__file__).with_name("input_ex.txt").read_text().split("\n")
on_cubes = get_turned_on_cubes(data)
assert on_cubes == 39

print("ex2")
data = Path(__file__).with_name("input_ex2.txt").read_text().split("\n")
on_cubes = get_turned_on_cubes(data)
assert on_cubes == 590784

print("ex3")
data = Path(__file__).with_name("input_ex3.txt").read_text().split("\n")
on_cubes = get_turned_on_cubes(data, part_two=False)
assert on_cubes == 474140
# print("part two")
# on_cubes = get_turned_on_cubes(data, part_two=True)
# assert on_cubes == 2758514936282235

print("real input")
data = Path(__file__).with_name("input.txt").read_text().split("\n")
on_cubes = get_turned_on_cubes(data)
print("part_one", on_cubes)
print("part two")
on_cubes = get_turned_on_cubes(data, part_two=True)
print(on_cubes)
