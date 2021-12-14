from collections import Counter
from pathlib import Path
from typing import Dict

from tqdm import tqdm


def get_polymere_after_steps(polymere: str, instructions: Dict[str, str], steps: int) -> str:
    new_polymere = ""
    for _ in tqdm(range(steps)):
        for i in range(len(polymere) - 1):
            new_polymere += polymere[i]
            if new_elem := instructions.get(polymere[i : i + 2]):
                new_polymere += new_elem
        new_polymere += polymere[-1]
        polymere = new_polymere
        new_polymere = ""
    return polymere


data = Path(__file__).with_name("input_ex.txt").read_text()
polymere_start, instructions = data.split("\n\n")
instructions = {line.split(" -> ")[0]: line.split(" -> ")[1] for line in instructions.split("\n")}
polymere = get_polymere_after_steps(polymere_start, instructions, 5)
assert len(polymere) == 97
polymere = get_polymere_after_steps(polymere_start, instructions, 10)
assert len(polymere) == 3073
counter = Counter(polymere)
assert counter.get("B") == 1749
assert counter.get("C") == 298
assert counter.get("H") == 161
assert counter.get("N") == 865
assert sorted(counter.values())[-1] - sorted(counter.values())[0] == 1588
polymere = get_polymere_after_steps(polymere_start, instructions, 40)
counter = Counter(polymere)
assert sorted(counter.values())[-1] - sorted(counter.values())[0] == 2188189693529

# ### Now with real input
data = Path(__file__).with_name("input.txt").read_text()
polymere_start, instructions = data.split("\n\n")
instructions = {line.split(" -> ")[0]: line.split(" -> ")[1] for line in instructions.split("\n")}
polymere = get_polymere_after_steps(polymere_start, instructions, 10)
counter = Counter(polymere)
print(sorted(counter.values()))
print(
    "Diff between most common - least common after 10 steps:",
    sorted(counter.values())[-1] - sorted(counter.values())[0],
)
polymere = get_polymere_after_steps(polymere_start, instructions, 40)
counter = Counter(polymere)
print(sorted(counter.values()))
print(
    "Diff between most common - least common after 40 steps:",
    sorted(counter.values())[-1] - sorted(counter.values())[0],
)
