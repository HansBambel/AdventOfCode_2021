from collections import Counter
from itertools import chain
from pathlib import Path
from typing import Dict, List


def find_path(caves_dict: Dict[str, List[str]], path: List[str], part_two=False) -> int:
    if path[-1] == "end":
        return 1
    else:
        if not part_two:
            possible_next = [cave for cave in caves_dict[path[-1]] if cave.isupper() or (cave not in path)]
        else:
            counter = Counter(path)
            small_cave_visited_twice = any([value > 1 for key, value in counter.items() if (key.islower())])
            possible_next = [
                cave
                for cave in caves_dict[path[-1]]
                if cave.isupper()
                or (cave.islower() and ((not small_cave_visited_twice) or counter[cave] == 0) and (cave != "start"))
            ]
        if len(possible_next) == 0:
            return 0
        total_paths = 0
        for cave in possible_next:
            total_paths += find_path(caves_dict, path + [cave], part_two=part_two)
    return total_paths


def get_all_paths(caves_raw: List[List[str]], part_two=False) -> int:
    caves = {cave for cave in chain(*caves_raw) if cave != ""}
    caves_dict = {}
    for cave in caves:
        caves_dict[cave] = [conn[0] if conn[1] == cave else conn[1] for conn in caves_raw if cave in conn]
    # generate path and check if path lead to end
    count = 0
    for cave in caves_dict["start"]:
        count += find_path(caves_dict, ["start", cave], part_two)

    return count


caves_raw = """start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""
caves_raw = [line.strip().split("-") for line in caves_raw.split("\n")]
assert get_all_paths(caves_raw) == 10
assert get_all_paths(caves_raw, part_two=True) == 36
caves_raw = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""
caves_raw = [line.strip().split("-") for line in caves_raw.split("\n")]
assert get_all_paths(caves_raw) == 19
assert get_all_paths(caves_raw, part_two=True) == 103
caves_raw = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""
caves_raw = [line.strip().split("-") for line in caves_raw.split("\n")]
assert get_all_paths(caves_raw) == 226
assert get_all_paths(caves_raw, part_two=True) == 3509


with open(Path(__file__).parent / "input.txt", "r") as f:
    caves_raw = f.readlines()

caves_raw = [line.strip().split("-") for line in caves_raw]

print("Paths through system:", get_all_paths(caves_raw))
print("Paths through system, part two:", get_all_paths(caves_raw, part_two=True))
