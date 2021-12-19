from itertools import permutations
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
        if isinstance(self.left, int) and isinstance(self.right, int):
            return 0
        left_max = 1
        right_max = 1
        if type(self.left) == FishNum:
            left_max += len(self.left)
        if type(self.right) == FishNum:
            right_max += len(self.right)
        return max(left_max, right_max)

    def __str__(self):
        return str(self.to_list())

    def magnitude(self) -> int:
        # Recursively get the magnitude
        left_num = self.left if (isinstance(self.left, int)) else self.left.magnitude()
        right_num = self.right if (isinstance(self.right, int)) else self.right.magnitude()
        return 3 * left_num + 2 * right_num

    def _trickle_up(self, number: int, direction: str, from_leaf: "FishNum"):
        if self.parent is not None:
            # When we can still go further up
            if direction == "left":
                # When we come already from the left -> go further up
                if self.left == from_leaf:
                    self.parent._trickle_up(number, direction, self)
                else:
                    # When there is something to the left
                    if isinstance(self.left, int):
                        # when it is a number -> easy, add number
                        self.left += number
                    else:
                        # when the left is a tree -> trickle down to the right
                        self.left._trickle_down(number, direction="right")
            else:
                # When we come already from the right -> go further up
                if self.right == from_leaf:
                    self.parent._trickle_up(number, direction, self)
                else:
                    # When there is something to the right
                    if isinstance(self.right, int):
                        self.right += number
                    else:
                        # The right part is a tree -> trickle down to the left
                        self.right._trickle_down(number, direction="left")
        else:
            # We are at the top node -> reverse the direction when trickling down now
            if direction == "left":
                # When we come from the right node then we need to trickle down the left path
                if self.right == from_leaf:
                    # if left node is an int -> easy, increase number, else trickle further down the left tree
                    if isinstance(self.left, int):
                        self.left += number
                    else:
                        self.left._trickle_down(number, "right")
            else:
                # when we come from the left node then we need to trickle down the right path
                if self.left == from_leaf:
                    # if right node is an int -> easy, increase number, else trickle down the right tree
                    if isinstance(self.right, int):
                        self.right += number
                    else:
                        self.right._trickle_down(number, "left")

    def _trickle_down(self, number: int, direction: str):
        # Go to the left-most node
        if direction == "left":
            if isinstance(self.left, int):
                self.left += number
            else:
                self.left._trickle_down(number, direction)
        # Go to the right-most node
        else:
            if isinstance(self.right, int):
                self.right += number
            else:
                self.right._trickle_down(number, direction)

    def explode(self) -> bool:
        # If next one is about to explode
        if len(self) == 1:
            # left one will explode
            if isinstance(self.left, FishNum) and (len(self.left) == 0):
                if isinstance(self.right, int):
                    self.right += self.left.right
                else:
                    # trickle down the right node to the left side
                    self.right._trickle_down(self.left.right, direction="left")
                self.parent._trickle_up(self.left.left, direction="left", from_leaf=self)
                self.left = 0
            # right one will explode
            else:
                if isinstance(self.left, int):
                    self.left += self.right.left
                else:
                    self.left._trickle_down(self.right.left, direction="left")
                self.parent._trickle_up(self.right.right, direction="right", from_leaf=self)
                self.right = 0
            return True
        else:
            # Not yet found the correct exploding pair
            # Expand left first
            if isinstance(self.left, FishNum) and (len(self.left) == len(self) - 1):
                exploded = self.left.explode()
                if exploded == False:
                    if isinstance(self.right, FishNum):
                        exploded = self.right.explode()
                    else:
                        return False
                return exploded
            # Right one gets expanded
            elif isinstance(self.right, FishNum):
                exploded = self.right.explode()
                if exploded == False:
                    if isinstance(self.left, FishNum):
                        exploded = self.left.explode()
                    else:
                        return False
                return exploded
            else:
                return False

    def reduce(self):
        while True:
            # explode
            if len(self) >= 4:
                change = self.explode()
                if change:
                    continue
            change = self.split()
            if not change:
                break
        return self

    def split(self) -> bool:
        split_done = False
        if isinstance(self.left, int):
            if self.left >= 10:
                self.left = FishNum([self.left // 2, (self.left + 1) // 2], self)
                split_done = True
        else:
            if self.left.split():
                split_done = True

        if split_done:
            return True
        # When we are here we have not split in the left part of the tree yet
        if isinstance(self.right, int):
            if self.right >= 10:
                self.right = FishNum([self.right // 2, (self.right + 1) // 2], self)
                split_done = True
        else:
            if self.right.split():
                split_done = True
        return split_done

    def to_list(self) -> List:
        return [
            self.left if type(self.left) == int else self.left.to_list(),
            self.right if type(self.right) == int else self.right.to_list(),
        ]

    def add(self, other: "FishNum") -> "FishNum":
        return FishNum([self.to_list(), other.to_list()]).reduce()


test_explode = [
    ([[[[[9, 8], 1], 2], 3], 4], [[[[0, 9], 2], 3], 4]),
    ([7, [6, [5, [4, [3, 2]]]]], [7, [6, [5, [7, 0]]]]),
    ([[6, [5, [4, [3, 2]]]], 1], [[6, [5, [7, 0]]], 3]),
    ([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]], [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]),
    ([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]], [[3, [2, [8, 0]]], [9, [5, [7, 0]]]]),
]
for case in test_explode:
    key, value = case[0], case[1]
    fish = FishNum(key)
    fish.explode()
    assert fish.to_list() == value

# Test reduce
fish = FishNum([[[[4, 3], 4], 4], [7, [[8, 4], 9]]])
assert fish.add(FishNum([1, 1])).to_list() == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]

print("Start with whole example")
data = Path(__file__).with_name("input_ex.txt").read_text()
current_number = ""
for line in data.split("\n"):
    fish = FishNum(eval(line))
    if current_number == "":
        current_number = fish
    else:
        current_number = current_number.add(fish)

assert current_number.to_list() == [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]

print("Check magnitude")
assert FishNum([[1, 2], [[3, 4], 5]]).magnitude() == 143
assert FishNum([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]).magnitude() == 1384
assert FishNum([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]).magnitude() == 445
assert FishNum([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]).magnitude() == 791
assert FishNum([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]).magnitude() == 1137
assert FishNum([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]).magnitude() == 3488

print("Start with example 2")
data = Path(__file__).with_name("input_ex2.txt").read_text()
current_number = ""
for line in data.split("\n"):
    fish = FishNum(eval(line))
    if current_number == "":
        current_number = fish
    else:
        current_number = current_number.add(fish)
assert current_number.to_list() == [[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]]
assert current_number.magnitude() == 4140

highest_magnitude = 0
for pair in permutations(data.split("\n"), 2):
    num1 = eval(pair[0])
    num2 = eval(pair[1])
    new_fish_num = FishNum(num1).add(FishNum(num2))
    if new_fish_num.magnitude() > highest_magnitude:
        highest_magnitude = new_fish_num.magnitude()
assert highest_magnitude == 3993

data = Path(__file__).with_name("input.txt").read_text()
current_number = ""
for line in data.split("\n"):
    fish = FishNum(eval(line))
    if current_number == "":
        current_number = fish
    else:
        current_number = current_number.add(fish)

print(current_number.magnitude())

# part two
highest_magnitude = 0
for pair in permutations(data.split("\n"), 2):
    num1 = eval(pair[0])
    num2 = eval(pair[1])
    new_fish_num = FishNum(num1).add(FishNum(num2))
    if new_fish_num.magnitude() > highest_magnitude:
        highest_magnitude = new_fish_num.magnitude()

print("highest_magnitude", highest_magnitude)
