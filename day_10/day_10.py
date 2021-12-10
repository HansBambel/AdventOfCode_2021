from pathlib import Path
from typing import List

input_raw = """
        [({(<(())[]>[[{[]{<()<>>
        [(()[<>])]({[<{<<[]>>(
        {([(<{}[<>[]}>{[]{[(<()>
        (((({<>}<{<{<>}{[]{[]{}
        [[<[([]))<([[{}[[()]]]
        [{[{({}]{}}([{[{{{}}([]
        {<[[]]>}<{[{[{[]{()[[[]
        [<(<(<(<{}))><([]([]()
        <{([([[(<>()){}]>(<<{{
        <{([{{}}[<[[[<>{}]]]>[]]
        """


points_part_one = {")": 3, "]": 57, "}": 1197, ">": 25137}
points_part_two = {"(": 1, "[": 2, "{": 3, "<": 4}
bracket_partners = {"(": ")", "[": "]", "{": "}", "<": ">"}


def push_to_stack(stack: List[str], syn: str) -> int:
    if (syn == "(") or (syn == "[") or (syn == "{") or (syn == "<"):
        stack.append(syn)
    else:
        # if popping gives a mistake we add the points of the responsible bracket
        if len(stack) == 0:
            return points_part_one[syn]
        else:
            if syn != bracket_partners[stack.pop()]:
                return points_part_one[syn]
    return 0


def get_error_points(input, part_two=False):
    total_points = 0
    corrupt_lines = []
    for i, line in enumerate(input):
        stack = []
        for syn in line.strip():
            points = push_to_stack(stack, syn)
            if points > 0:
                total_points += points
                corrupt_lines.append(i)
                break
    # Only do those that are not corrupt
    if part_two:
        total_points = []
        incomplete_lines = [line for i, line in enumerate(input) if i not in corrupt_lines]
        # Iterate through and collect new points
        for line in incomplete_lines:
            points_per_line = 0
            stack = []
            # create stack
            for syn in line.strip():
                push_to_stack(stack, syn)
            # empty stack and compute points for line
            while len(stack) > 0:
                points_per_line = 5 * points_per_line + points_part_two[stack.pop()]
            total_points.append(points_per_line)
    return total_points


assert get_error_points(input_raw.split()) == 26397

points_part_two_true = [288957, 5566, 1480781, 995444, 294]
assert get_error_points(input_raw.split(), part_two=True) == points_part_two_true
assert sorted(points_part_two_true)[len(points_part_two_true) // 2] == 288957
with open(Path(__file__).parent / "input.txt", "r") as f:
    input_raw = f.readlines()

print(get_error_points(input_raw))
result_points = get_error_points(input_raw, part_two=True)
mid_points = sorted(result_points)[len(result_points) // 2]
print(mid_points)
