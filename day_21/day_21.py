from functools import lru_cache
from itertools import product
from pathlib import Path
from typing import List, Tuple

import numpy as np


def get_score_part_one(start_pos: List[int]) -> int:
    die_rolls = 0
    scores = np.array([0, 0])
    board = np.arange(10) + 1
    dice = np.arange(100) + 1
    stands_on = np.array(start_pos)
    while all(scores < 1000):
        dice_points = np.sum(np.roll(dice, -(die_rolls % 100))[:3])
        # Board points are the starting position + number of points wrapped around
        board_points = board[(stands_on[die_rolls % 2] + dice_points) % 10]
        stands_on[die_rolls % 2] = board_points - 1
        scores[die_rolls % 2] += board_points
        die_rolls += 3

    losing_score = np.min(scores)
    return losing_score * die_rolls


@lru_cache(maxsize=None)
def play_dirac_dice(scores: Tuple[int, int], turn: int, stands_on: Tuple[int, int]) -> Tuple[int, int]:
    # returns amount of wins
    wins = (0, 0)
    # Play finish playing dirac dice with rolling a 1, 2 and 3
    all_combs = (p for p in product([1, 2, 3], repeat=3))
    for points in all_combs:
        # Board points are the starting position + number of points wrapped around
        board_points = ((stands_on[turn] + sum(points)) % 10) + 1
        if turn == 0:
            stands_on_update = (board_points - 1, stands_on[1])
            points_update = (scores[0] + board_points, scores[1])
        else:
            stands_on_update = (stands_on[0], board_points - 1)
            points_update = (scores[0], scores[1] + board_points)
        # if score over 21 -> increase win counter for that player
        if points_update[0] >= 21:
            wins = (wins[0] + 1, wins[1])
        elif points_update[1] >= 21:
            wins = (wins[0], wins[1] + 1)
        else:
            # Add the winning numbers
            p1_wins, p2_wins = play_dirac_dice(points_update, (turn + 1) % 2, stands_on_update)
            wins = (wins[0] + p1_wins, wins[1] + p2_wins)
    return wins


def get_number_wins_part_two(start_pos: List[int]) -> List[int]:
    die_rolls = 0
    scores = (0, 0)
    stands_on = (start_pos[0], start_pos[1])

    wins = np.zeros(2)
    wins += play_dirac_dice(scores, die_rolls, stands_on)

    return wins


data = Path(__file__).with_name("input_ex.txt").read_text().split("\n")
start_p1 = int(data[0].split(": ")[-1])
start_p2 = int(data[1].split(": ")[-1])
# We need to subtract one because we want the indices
score = get_score_part_one([start_p1 - 1, start_p2 - 1])
assert score == 739785
print("Start part two")
wins = get_number_wins_part_two([start_p1 - 1, start_p2 - 1])
assert wins[0] == 444356092776315
assert wins[1] == 341960390180808

print("Real input")
data = Path(__file__).with_name("input.txt").read_text().split("\n")
start_p1 = int(data[0].split(":")[-1])
start_p2 = int(data[1].split(":")[-1])
# We need to subtract one because we want the indices
score = get_score_part_one([start_p1 - 1, start_p2 - 1])
print(score)
print("Start part two")
wins = get_number_wins_part_two([start_p1 - 1, start_p2 - 1])

print(wins)
print("Max wins: ", np.max(wins))
