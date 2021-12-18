from functools import partial
from pathlib import Path
from typing import List, Tuple

from tqdm import tqdm


def check_if_hit(coords: Tuple[int, int], y_from: int, y_to: int, x_from: int, x_to: int) -> bool:
    # Y and X
    return (coords[0] in range(y_to, y_from + 1)) and coords[1] in range(x_from, x_to + 1)


def project_path(velocity: Tuple[int, int], y_to: int) -> List[Tuple[int, int]]:
    y, x = velocity
    path = []
    coords = (0, 0)
    while coords[0] >= y_to:
        coords = (coords[0] + y, coords[1] + x)
        path.append(coords)
        y -= 1
        x = 0 if x == 0 else x - 1
    return path


def get_highest_y_value(y_from: int, y_to: int, x_from: int, x_to: int) -> Tuple[int, int]:
    # x velocity decreases until 0 and y velocity increases constantly
    check_if_hit_ranges = partial(check_if_hit, y_from=y_from, y_to=y_to, x_from=x_from, x_to=x_to)
    project_path_y_to = partial(project_path, y_to=y_to)

    highest_y_value = 0
    found_velocities = 0

    min_x_velocity = 250
    max_y_velocity = 800
    for y in tqdm(range(max_y_velocity, -max_y_velocity, -1)):
        # if not, decrease x until 0
        for x in range(min_x_velocity, 0, -1):
            # project the path and then check if the target is hit at any step
            path_hits = any([check_if_hit_ranges(coords) for coords in project_path_y_to((y, x))])
            # if a path hits with this velocity then increase the counter
            found_velocities += path_hits
            if path_hits and highest_y_value == 0:
                path = project_path_y_to((y, x))
                highest_y_value = max([c[0] for c in path])

    return highest_y_value, found_velocities


data = Path(__file__).with_name("input_ex.txt").read_text()
target_x = data.split("x=")[1].split(",")[0]
x_from, x_to = int(target_x.split("..")[0]), int(target_x.split("..")[1])
target_y = data.split("y=")[1]
y_to, y_from = int(target_y.split("..")[0]), int(target_y.split("..")[1])

part_one, part_two = get_highest_y_value(y_from, y_to, x_from, x_to)
assert part_one == 45
assert part_two == 112

data = Path(__file__).with_name("input.txt").read_text()
target_x = data.split("x=")[1].split(",")[0]
x_from, x_to = int(target_x.split("..")[0]), int(target_x.split("..")[1])
target_y = data.split("y=")[1]
y_to, y_from = int(target_y.split("..")[0]), int(target_y.split("..")[1])


part_one, part_two = get_highest_y_value(y_from, y_to, x_from, x_to)
assert part_one == 4851
print(part_one)
print(part_two)
