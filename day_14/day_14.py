from collections import Counter
from pathlib import Path
from typing import Dict

from tqdm import tqdm


def get_polymere_after_steps(polymere: str, instructions: Dict[str, str], steps: int) -> Counter:
    counter = Counter([polymere[i : i + 2] for i in range(len(polymere) - 1)])
    new_counter = {}
    for _ in tqdm(range(steps)):
        new_counter = Counter()
        for pair, val in counter.items():
            if elem := instructions.get(pair):
                new_counter[pair[0] + elem] += val
                new_counter[elem + pair[1]] += val
            else:
                new_counter[pair] += val
        counter = new_counter
    # Now count occurrences of single chars
    counter = Counter()
    for pair, val in new_counter.items():
        counter[pair[0]] += val / 2
        counter[pair[1]] += val / 2
    # Counter could have fractions
    for c, val in counter.items():
        counter[c] = int(val + 0.5)

    return counter


data = Path(__file__).with_name("input_ex.txt").read_text()
polymere_start, instructions = data.split("\n\n")
instructions = {line.split(" -> ")[0]: line.split(" -> ")[1] for line in instructions.split("\n")}
counter = get_polymere_after_steps(polymere_start, instructions, 10)
assert counter.get("B") == 1749
assert counter.get("C") == 298
assert counter.get("H") == 161
assert counter.get("N") == 865
assert sorted(counter.values())[-1] - sorted(counter.values())[0] == 1588
counter = get_polymere_after_steps(polymere_start, instructions, 40)
assert sorted(counter.values())[-1] - sorted(counter.values())[0] == 2188189693529

# ### Now with real input
data = Path(__file__).with_name("input.txt").read_text()
polymere_start, instructions = data.split("\n\n")
instructions = {line.split(" -> ")[0]: line.split(" -> ")[1] for line in instructions.split("\n")}
counter = get_polymere_after_steps(polymere_start, instructions, 10)
print(sorted(counter.values()))
print(
    "Diff between most common - least common after 10 steps:",
    sorted(counter.values())[-1] - sorted(counter.values())[0],
)
counter = get_polymere_after_steps(polymere_start, instructions, 40)
print(sorted(counter.values()))
print(
    "Diff between most common - least common after 40 steps:",
    sorted(counter.values())[-1] - sorted(counter.values())[0],
)
