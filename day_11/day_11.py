from pathlib import Path

import numpy as np
from tqdm import tqdm

neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def simulate_steps(octopuses, steps: int) -> int:
    total_flashes = 0
    for _ in tqdm(range(steps)):
        # increase energy level
        octopuses += 1
        flashed_oct = octopuses > 9
        flashed_oct_step = flashed_oct
        octopuses[flashed_oct] = 0
        while (flashes := np.sum(flashed_oct)) > 0:
            total_flashes += flashes
            # increase neighbors of flashed ones
            ind_y_flashed, ind_x_flashed = np.where(flashed_oct)
            for ind_y, ind_x in zip(ind_y_flashed, ind_x_flashed):
                for y, x in neighbors:
                    y_neighbor = y + ind_y
                    x_neighbor = x + ind_x
                    # neighbor is not outside of range
                    if (
                        (y_neighbor < 0)
                        or (x_neighbor < 0)
                        or (y_neighbor >= len(octopuses))
                        or (x_neighbor >= len(octopuses[0]))
                    ):
                        continue
                    else:
                        # note that an octopus can only flash once per step
                        if (octopuses[y_neighbor, x_neighbor] == 0) and flashed_oct_step[y_neighbor, x_neighbor]:
                            continue
                        else:
                            octopuses[y_neighbor, x_neighbor] += 1
            flashed_oct = octopuses > 9
            octopuses[flashed_oct] = 0
            flashed_oct_step[flashed_oct] = 1

    return total_flashes


def get_sync_step(octopuses) -> int:
    steps = 0
    all_flashed = False
    while not all_flashed:
        # increase energy level
        octopuses += 1
        flashed_oct = octopuses > 9
        flashed_oct_step = flashed_oct
        octopuses[flashed_oct] = 0
        while np.sum(flashed_oct) > 0:
            # increase neighbors of flashed ones
            ind_y_flashed, ind_x_flashed = np.where(flashed_oct)
            for ind_y, ind_x in zip(ind_y_flashed, ind_x_flashed):
                for y, x in neighbors:
                    y_neighbor = y + ind_y
                    x_neighbor = x + ind_x
                    # neighbor is not outside of range
                    if (
                        (y_neighbor < 0)
                        or (x_neighbor < 0)
                        or (y_neighbor >= len(octopuses))
                        or (x_neighbor >= len(octopuses[0]))
                    ):
                        continue
                    else:
                        # note that an octopus can only flash once per step
                        if (octopuses[y_neighbor, x_neighbor] == 0) and flashed_oct_step[y_neighbor, x_neighbor]:
                            continue
                        else:
                            octopuses[y_neighbor, x_neighbor] += 1
            flashed_oct = octopuses > 9
            octopuses[flashed_oct] = 0
            flashed_oct_step[flashed_oct] = 1
        all_flashed = flashed_oct_step.all()
        steps += 1
    return steps


octopuses_raw = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
octopuses_raw = [list(line) for line in octopuses_raw.split("\n")]
octopuses = np.array(octopuses_raw[1:-1], dtype=int)

assert simulate_steps(octopuses.copy(), 10) == 204
assert simulate_steps(octopuses.copy(), 100) == 1656
assert get_sync_step(octopuses) == 195

with open(Path(__file__).parent / "input.txt", "r") as f:
    octopuses_raw = f.readlines()

octopuses_raw = [list(line.strip()) for line in octopuses_raw]
octopuses = np.array(octopuses_raw, dtype=int)
print("total_flashes after 100 steps:", simulate_steps(octopuses.copy(), 100))
print("synchronysing after:", get_sync_step(octopuses))
