from pathlib import Path

import numpy as np

lanternfish_test = np.array([3, 4, 3, 1, 2], dtype=int)


def new_hatches(fish_days_to_hatch):
    new_fish = fish_days_to_hatch[0]
    # move all fishes to the left
    fish_days_to_hatch = fish_days_to_hatch[1:]
    fish_days_to_hatch = np.concatenate([fish_days_to_hatch, [new_fish]])
    fish_days_to_hatch[6] += new_fish
    return fish_days_to_hatch


def population_after_days(lanternfishes, days: int = 80):
    # Count the fishes and put them in bins: 0-8 days till hatch
    fish_days_to_hatch = np.bincount(lanternfishes, minlength=9)

    num_fishes = sum(fish_days_to_hatch)
    for _ in range(1, days + 1):
        fish_days_to_hatch = new_hatches(fish_days_to_hatch)
        num_fishes = sum(fish_days_to_hatch)

    return num_fishes


assert population_after_days(lanternfish_test, 18) == 26
assert population_after_days(lanternfish_test, 80) == 5934
assert population_after_days(lanternfish_test, 256) == 26984457539


with open(Path(__file__).parent / "input.txt", "r") as f:
    lanternfish = f.readline()
    lanternfish = lanternfish.split(",")
lanternfish = np.array(lanternfish, dtype=int)

print("Population after 80 days", population_after_days(lanternfish, 80))
print("Population after 256 days", population_after_days(lanternfish, 256))
