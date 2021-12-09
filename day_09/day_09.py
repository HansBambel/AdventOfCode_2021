from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np


def get_lowest_points(ocean_floor):
    lowest_points = np.zeros(ocean_floor.shape, dtype=int)
    for y in range(ocean_floor.shape[0]):
        for x in range(ocean_floor.shape[1]):
            # all four neighbors need to be bigger than Point(x,y)
            # additionally it is also okay when we are at an edge or corner
            if (
                ((y - 1 < 0) | (ocean_floor[max(y - 1, 0), x] > ocean_floor[y, x]))
                & (
                    (y + 1 >= ocean_floor.shape[0])
                    | (ocean_floor[min(y + 1, ocean_floor.shape[0] - 1), x] > ocean_floor[y, x])
                )
                & ((x - 1 < 0) | (ocean_floor[y, max(0, x - 1)] > ocean_floor[y, x]))
                & (
                    (x + 1 >= ocean_floor.shape[1])
                    | (ocean_floor[y, min(ocean_floor.shape[1] - 1, x + 1)] > ocean_floor[y, x])
                )
            ):
                lowest_points[y, x] = 1
    return lowest_points


def get_lowest_points_pure_np(ocean_floor):
    # Interesting solution taken from
    # https://www.reddit.com/r/adventofcode/comments/rcjgu6/despite_having_used_python_for_years_today_was
    m = np.pad(ocean_floor, pad_width=1, constant_values=9)
    # get the points where all neighbors are higher
    return ((m < np.roll(m, 1, 0)) &
            (m < np.roll(m, -1, 0)) &
            (m < np.roll(m, 1, 1)) &
            (m < np.roll(m, -1, 1)))[
        1:-1, 1:-1
    ]  # Because earlier it was padded we need to remove the padding again


def calc_risk_level(ocean_floor) -> int:
    lowest_points = get_lowest_points(ocean_floor)
    lowest_points = get_lowest_points_pure_np(ocean_floor)

    return np.sum(ocean_floor * lowest_points) + np.sum(lowest_points)


def basin_size(basin_edges, y: int, x: int) -> int:
    # If the current field is outside or is an edge don't add to basin size
    if (y < 0) | (y > basin_edges.shape[0] - 1) | (x < 0) | (x > basin_edges.shape[1] - 1):
        return 0
    elif basin_edges[y, x] == 1:
        return 0
    else:
        # set current field to an edge
        basin_edges[y, x] = 1
        # recursive calls
        return (
            1
            + basin_size(basin_edges, y - 1, x)
            + basin_size(basin_edges, y + 1, x)
            + basin_size(basin_edges, y, x - 1)
            + basin_size(basin_edges, y, x + 1)
        )


def get_biggest_basin_size(ocean_floor) -> List[int]:
    lowest_points = get_lowest_points(ocean_floor)
    # These are the start points
    basin_edges = np.where(ocean_floor == 9, 1, 0)
    y_indices, x_indices = np.where(lowest_points)
    basin_sizes = [basin_size(basin_edges, y_indices[i], x_indices[i]) for i in range(len(x_indices))]
    return sorted(basin_sizes, reverse=True)[:3]


ocean_floor_raw = ["2199943210", "3987894921", "9856789892", "8767896789", "9899965678"]
ocean_floor = np.array([list(line) for line in ocean_floor_raw], dtype=int)
assert calc_risk_level(ocean_floor) == 15
basins = get_biggest_basin_size(ocean_floor)
assert np.prod(basins) == 1134

with open(Path(__file__).parent / "input.txt", "r") as f:
    ocean_floor_raw = f.readlines()

ocean_floor = np.array([list(line.strip()) for line in ocean_floor_raw], dtype=int)
plt.imshow(ocean_floor)
plt.show()
print("Risk level:", calc_risk_level(ocean_floor))
basins = get_biggest_basin_size(ocean_floor)
print("Multiplied biggest basins:", np.prod(basins))
