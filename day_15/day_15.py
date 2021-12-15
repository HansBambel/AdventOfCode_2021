from pathlib import Path
from typing import Tuple

import numpy as np

neighbors = [(-1, 0), (+1, 0), (0, -1), (0, +1)]


def expand_path(cave, node: Tuple[int, int], costs, visited):
    while not visited[-1, -1]:
        # get current node
        y, x = node
        # inside cave
        neighbor_coords = [
            (y + n_y, x + n_x)
            for n_y, n_x in neighbors
            if (0 <= y + n_y < cave.shape[0]) and (0 <= x + n_x < cave.shape[1]) and (not visited[(y + n_y, x + n_x)])
        ]

        visited[y, x] = True
        for n_coord in neighbor_coords:
            alt = costs[y, x] + cave[n_coord]
            if alt < costs[n_coord]:
                costs[n_coord] = alt

        # expand most promising node
        most_promising_node = np.unravel_index(np.argmin(np.where(~visited, costs, np.inf), axis=None), costs.shape)
        node = most_promising_node


def find_lowest_path(cave) -> int:
    # Start is the top left
    node = (0, 0)
    costs = np.ones(cave.shape) * np.inf
    costs[0, 0] = 0
    visited = np.zeros(cave.shape, dtype=bool)
    expand_path(cave, node, costs, visited)

    return costs[-1, -1]


data = Path(__file__).with_name("input_ex2.txt").read_text()
cave = np.array([list(line) for line in data.split("\n")], dtype=int)
assert find_lowest_path(cave) == 8
print("Small done")
data = Path(__file__).with_name("input_ex.txt").read_text()
cave = np.array([list(line) for line in data.split("\n")], dtype=int)
assert find_lowest_path(cave) == 40
print("Example done")

# ### Real input ###
data = Path(__file__).with_name("input.txt").read_text()
cave = np.array([list(line) for line in data.split("\n")], dtype=int)
print(find_lowest_path(cave))


# Part two
def increase_cave(cave):
    bigger_cave = np.zeros((cave.shape[0] * 5, cave.shape[1] * 5), dtype=int)
    for i in range(5):
        for j in range(5):
            bigger_cave[j * cave.shape[1] : (j + 1) * cave.shape[1], i * cave.shape[0] : (i + 1) * cave.shape[0]] = (
                cave + i + j
            )
            # Wrap around
            bigger_cave[bigger_cave > 9] %= 9
    return bigger_cave


data = Path(__file__).with_name("input_ex.txt").read_text()
cave = np.array([list(line) for line in data.split("\n")], dtype=int)
data2 = Path(__file__).with_name("part2_ex.txt").read_text()
cave2 = np.array([list(line) for line in data2.split("\n")], dtype=int)

assert np.equal(increase_cave(cave), cave2).all()

data = Path(__file__).with_name("input.txt").read_text()
cave = np.array([list(line) for line in data.split("\n")], dtype=int)
cave_big = increase_cave(cave)
print(find_lowest_path(cave_big))
