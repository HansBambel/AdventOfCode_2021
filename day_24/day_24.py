from pathlib import Path
from typing import List

from tqdm import tqdm


def is_valid_model_number(model_number: str, instructions: List[str]) -> bool:
    assert len(model_number) == 14

    variables = {"w": 0, "x": 0, "y": 0, "z": 0}
    for i, ins_block in enumerate(instructions):
        # set w (other variables keep their old value)
        variables["w"] = int(model_number[i])
        # execute instructions
        for ins in ins_block.strip().split("\n"):
            op: str = ins.split()[0]
            var: str = ins.split()[1]
            val = ins.split()[2]
            if val.isdigit():
                # easy case
                val = int(val)
            else:
                # Negative values are not recognized with isdigit() -> handle that case
                if val[0] == "-":
                    val = int(val[1:]) * -1
                else:
                    # it is another variable
                    val = variables[val]
            # do the operation
            if op == "add":
                variables[var] += val
            elif op == "mul":
                variables[var] *= val
            elif op == "div":
                variables[var] //= val
            elif op == "mod":
                variables[var] %= val
            elif op == "eql":
                variables[var] = int(variables[var] == val)

    return variables["z"] == 0


instructions = Path(__file__).with_name("input.txt").read_text().split("inp w")
# Brute force is not the way to go (4mio h is not really feasible) <(°_°)>
num = 99_999_999_999_999
for num in tqdm(range(99_999_999_999_999, 11_111_111_111_111, -1)):
    if is_valid_model_number(str(num), instructions[1:]):
        break

print(num)
