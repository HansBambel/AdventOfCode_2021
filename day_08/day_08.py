from pathlib import Path
from typing import List


def count_1478(letter_lines) -> int:
    output = [line.split("|")[1].strip().split(" ") for line in letter_lines]
    # 1 needs 2 segments
    # 4 needs 4 segments
    # 7 needs 3 segments
    # 8 needs 7 segments
    counter = 0
    for line in output:
        for segment in line:
            if len(segment) == 2:
                counter += 1
            elif len(segment) == 4:
                counter += 1
            elif len(segment) == 3:
                counter += 1
            elif len(segment) == 7:
                counter += 1
    return counter


def decode_output(letter_lines) -> List[int]:
    letter_lines = [line.strip() for line in letter_lines]
    number_list = []
    for line in letter_lines:
        # the entries after | are the output
        segments, output = line.split(" | ")
        segments = segments.split(" ")
        output = output.split(" ")

        one = next(filter(lambda x: len(x) == 2, segments))
        seven = next(filter(lambda x: len(x) == 3, segments))
        eight = next(filter(lambda x: len(x) == 7, segments))
        four = next(filter(lambda x: len(x) == 4, segments))
        # seven = next(filter(lambda x: x not in list(one), list(seven)))
        # the three has the segment on the right in it
        candidates_three = list(filter(lambda x: len(x) == 5, segments))
        three = next(filter(lambda x: all([letter in x for letter in list(one)]), candidates_three))
        candidates_six = list(filter(lambda x: len(x) == 6, segments))
        six = next(filter(lambda x: not all([letter in x for letter in list(one)]), candidates_six))
        # contain only 2,5,9,0
        candidates_remaining = list(filter(lambda x: x not in [one, three, six, seven, eight, four], segments))
        five = next(filter(lambda x: len(x) == 5 and sum([letter in x for letter in six]) == 5, candidates_remaining))
        two = next(filter(lambda x: (len(x) == 5) and (x != five), candidates_remaining))
        candidates_remaining = [c for c in candidates_remaining if c not in [two, five]]
        nine = next(
            filter(
                lambda x: all([letter in x for letter in three]) and all([letter in x for letter in four]),
                candidates_remaining,
            )
        )
        zero = [c for c in candidates_remaining if c not in [nine]][0]

        decode_dict = {one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, zero: 0}

        def decode_letters(letters) -> str:
            for key, value in decode_dict.items():
                if all([(len(letters) == len(key)) and (code_letter in letters) for code_letter in key]):
                    return f"{value}"
            raise ValueError("unknown code")

        number_str = [decode_letters(letters) for letters in output]
        number_list.append(int("".join(number_str)))
    return number_list


letter_input = [
    "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
    "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
    "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
    "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
    "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
    "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",
    "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",
    "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",
    "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",
    "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce",
]

assert count_1478(letter_input) == 26
print("Count easy letters on test", count_1478(letter_input))
decoded_output = decode_output(letter_input)
assert decoded_output[0] == 8394
assert decoded_output[1] == 9781
assert decoded_output[2] == 1197
assert decoded_output[3] == 9361
assert decoded_output[4] == 4873
assert decoded_output[5] == 8418
assert decoded_output[6] == 4548
assert decoded_output[7] == 1625
assert decoded_output[8] == 8717
assert decoded_output[9] == 4315
assert sum(decoded_output) == 61229


with open(Path(__file__).parent / "input.txt", "r") as f:
    letter_input = f.readlines()

print("Count easy letters on real input", count_1478(letter_input))
print("Sum of decoded output", sum(decode_output(letter_input)))
