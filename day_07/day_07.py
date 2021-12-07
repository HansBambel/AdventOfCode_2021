from pathlib import Path

import numpy as np


def get_fuel_count_for_position(crab_submarines, part_two=False):
    fuel_costs = np.zeros((np.max(crab_submarines)))
    fuel_per_change = np.cumsum(range(np.max(crab_submarines) + 1))
    for pos in range(np.max(crab_submarines)):
        if not part_two:
            fuel_costs[pos] = np.sum(abs(crab_submarines - pos))
        else:
            fuel_costs[pos] = np.sum([fuel_per_change[change] for change in abs(crab_submarines - pos)])
    return fuel_costs


crabs = np.array([16, 1, 2, 0, 4, 2, 7, 1, 2, 14], dtype=int)
fuel_costs = get_fuel_count_for_position(crabs)

assert fuel_costs[2] == 37
assert fuel_costs[1] == 41
assert fuel_costs[3] == 39
assert fuel_costs[10] == 71
print("Lowest position: ", np.argmin(fuel_costs))

fuel_costs_new = get_fuel_count_for_position(crabs, part_two=True)
assert fuel_costs_new[5] == 168
assert fuel_costs_new[2] == 206

with open(Path(__file__).parent / "input.txt", "r") as f:
    crabs = f.readline()
    crabs = crabs.split(",")
crabs = np.array(crabs, dtype=int)
fuel_costs = get_fuel_count_for_position(crabs)
print("Best position: ", np.argmin(fuel_costs), "fuel use:", np.min(fuel_costs))

fuel_costs = get_fuel_count_for_position(crabs, part_two=True)
print("Best position new: ", np.argmin(fuel_costs), "fuel use:", np.min(fuel_costs))
