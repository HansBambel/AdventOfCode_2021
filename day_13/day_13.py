from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def convert_input(input_raw):
    data_dots, folds = input_raw.split("\n\n")
    data_dots = np.array([line.split(",") for line in data_dots.split("\n")], dtype=int)
    folds = folds.split("\n")
    paper = np.zeros((np.max(data_dots, 0)[1] + 1, np.max(data_dots, 0)[0] + 1), dtype=bool)
    paper = add_dots(paper, data_dots)
    return paper, folds


def add_dots(paper, data_dots):
    for point in data_dots:
        paper[point[1], point[0]] = 1
    return paper


def fold_paper(paper, fold_instructions, part_one=True):
    for instr in fold_instructions:
        ind = int(instr.split("=")[1])
        if "x" in instr:
            to_fold = paper[:, ind + 1 :]
            # to_fold needs to be reversed
            to_fold = np.flip(to_fold, 1)
            # cut off the fold
            paper = paper[:, :ind]
            # add fold
            paper[:, -to_fold.shape[1] :] = paper[:, -to_fold.shape[1] :] + to_fold
        else:
            to_fold = paper[ind + 1 :, :]
            # to_fold needs to be reversed
            to_fold = np.flip(to_fold, 0)
            # cut off the fold
            paper = paper[:ind, :]
            # add fold
            paper[-to_fold.shape[1] :, :] = paper[-to_fold.shape[1] :, :] + to_fold
        if part_one:
            break
    return paper


data = Path(__file__).with_name("input_ex.txt").read_text()
paper, folds = convert_input(data)
paper = fold_paper(paper, folds, part_one=True)

assert np.sum(paper) == 17

data = Path(__file__).with_name("input.txt").read_text()
paper, folds = convert_input(data)

paper_one = fold_paper(paper.copy(), folds, part_one=True)
paper_two = fold_paper(paper.copy(), folds, part_one=False)
print("part one", np.sum(paper_one))
plt.imshow(paper_two)
plt.show()
