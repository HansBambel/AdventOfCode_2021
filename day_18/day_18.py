from itertools import chain
from pathlib import Path
from typing import List, Optional, Union


class FishNum:
    left: Union[int, "FishNum"]
    right: Union[int, "FishNum"]
    parent: Optional["FishNum"]

    def __init__(self, in_list: List, parent=None):
        self.parent = parent
        self.left = in_list[0] if isinstance(in_list[0], int) else FishNum(in_list[0], parent=self)
        self.right = in_list[1] if isinstance(in_list[1], int) else FishNum(in_list[1], parent=self)

    def __len__(self) -> int:
        left_max = 0
        right_max = 0
        if type(self.left) == FishNum:
            left_max += len(self.left)
        if type(self.right) == FishNum:
            right_max += len(self.right)
        return max(left_max, right_max)

    def magnitude(self) -> int:
        left_num = self.left if (isinstance(self.left, int)) else self.left.magnitude()
        right_num = self.right if (isinstance(self.right, int)) else self.right.magnitude()
        return 3 * left_num + 2 * right_num

    def trickle_up(self, number: int, direction: str):
        if direction == "right":
            if self.parent is None and self.left:
                return
            if type(self.left) == FishNum:
                self.left.trickle_down(number, direction=direction)
            else:
                self.parent.trickle_up(number, direction)

    def trickle_down(self, number: int, direction: str):
        if direction == "left":
            leaf = self.left
            while not isinstance(leaf, int):
                leaf = leaf.left
            leaf.left += number
        else:
            leaf = self.right
            while not isinstance(leaf, int):
                leaf = leaf.right
            leaf.right += number

    def explode(self) -> bool:
        if len(self) == 1:
            if len(self.left) == 0:
                self.trickle_down(self.left.right, direction="left")
                self.trickle_up(self.left.left, direction="right")
                self.left = 0

            return True
        else:
            exploded = self.left.explode()
            if not exploded:
                self.right.explode()
            return exploded

    def add_left(self, to_add: int):
        pass

    def reduce(self):
        while True:
            # explode
            change = self.explode()
            if change:
                continue
            change = self.split()
            if not change:
                break

    def split(self) -> bool:
        if any(list(chain(*self.to_list())) >= 10):
            return self.split().reduce()
        pass

    def to_list(self) -> List:
        return [
            self.left if type(self.left) == int else self.left.to_list(),
            self.right if type(self.right) == int else self.right.to_list(),
        ]

    def add(self, other: "FishNum"):
        return FishNum([self.to_list(), other.to_list()]).reduce()


data = Path(__file__).with_name("input_ex.txt").read_text()
current_number = ""
for line in data.split("\n"):
    fish = FishNum(eval(line))
    if current_number == "":
        current_number = fish
    else:
        current_number.add(fish)

assert current_number.to_list() == [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]

assert FishNum([[[[[9, 8], 1], 2], 3], 4]).explode() == [[[[0, 9], 2], 3], 4]
assert FishNum([7, [6, [5, [4, [3, 2]]]]]).explode() == [7, [6, [5, [7, 0]]]]
assert FishNum([[6, [5, [4, [3, 2]]]], 1]).explode() == [[6, [5, [7, 0]]], 3]
assert FishNum([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]).explode() == [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]
assert FishNum([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]).explode() == [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]

assert FishNum([[1, 2], [[3, 4], 5]]).magnitude() == 143
assert FishNum([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]).magnitude() == 1384
assert FishNum([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]).magnitude() == 445
assert FishNum([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]).magnitude() == 791
assert FishNum([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]).magnitude() == 1137
assert FishNum([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]).magnitude() == 3488


data = Path(__file__).with_name("input_ex2.txt").read_text()
current_number = ""
for line in data.split("\n"):
    fish = FishNum(eval(line))
    if current_number == "":
        current_number = fish
    else:
        current_number.add(fish)
assert current_number.to_list() == [[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]]
assert current_number.magnitude() == 4140

data = Path(__file__).with_name("input.txt").read_text()
current_number = ""
for line in data.split("\n"):
    fish = FishNum(eval(line))
    if current_number == "":
        current_number = fish
    else:
        current_number.add(fish)

print(current_number.magnitude())
