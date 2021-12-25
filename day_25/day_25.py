from pathlib import Path

import numpy as np


def do_step(cucumbers) -> bool:
    """Returns true if cucumbers moved."""
    before_step = cucumbers.copy()
    # First the ones facing east (1) move then facing south (2)
    # -> basically two-step process

    # First east
    east_y, east_x = np.where(cucumbers == 1)
    # check if (east_x+1)%(len-1) is free
    east_x_new = (east_x + 1) % (cucumbers.shape[1])
    free = cucumbers[east_y, east_x_new] == 0
    # set the old ones to 0 and the new ones to 1
    cucumbers[east_y[free], east_x[free]] = 0
    cucumbers[east_y[free], east_x_new[free]] = 1

    # now south
    south_y, south_x = np.where(cucumbers == 2)
    # check if (east_x+1)%(len-1) is free
    south_y_new = (south_y + 1) % (cucumbers.shape[0])
    free = cucumbers[south_y_new, south_x] == 0
    # set the old ones to 0 and the new ones to 1
    cucumbers[south_y[free], south_x[free]] = 0
    cucumbers[south_y_new[free], south_x[free]] = 2

    # if equal then no change
    return not np.array_equal(before_step, cucumbers)


def convert_cucumbers(data):
    cucumbers = [list(line.replace(".", "0").replace(">", "1").replace("v", "2")) for line in data.split("\n")]
    # convert empty spaces to 0, east facing to 1 and south to 2
    cucumbers = np.array(cucumbers, dtype=int)
    return cucumbers


sample = """...>...
.......
......>
v.....>
......>
.......
..vvv.."""

sample_1step = """..vv>..
.......
>......
v.....>
>......
.......
....v.."""

sample = convert_cucumbers(sample)
sample_1step = convert_cucumbers(sample_1step)
do_step(sample)
assert np.array_equal(sample, sample_1step)

data = Path(__file__).with_name("input_ex.txt").read_text()
cucumbers = convert_cucumbers(data)
step = 1
while do_step(cucumbers):
    step += 1
assert step == 58

print("Example done")

data = Path(__file__).with_name("input.txt").read_text()
cucumbers = convert_cucumbers(data)
step = 1
while do_step(cucumbers):
    step += 1
print("Part 1:", step)
