from pathlib import Path

import pandas as pd


def part_one(df: pd.DataFrame):
    depth = 0
    horizontal = 0

    for _, row in df.iterrows():
        if row["instruction"] == "forward":
            horizontal += row["value"]
        elif row["instruction"] == "down":
            depth += row["value"]
        else:
            depth -= row["value"]

    print("Part one")
    print(f"horizontal: {horizontal}, depth: {depth}, horizontal*depth: {horizontal*depth}")


def part_two(df: pd.DataFrame):
    depth = 0
    horizontal = 0
    aim = 0

    for _, row in df.iterrows():
        if row["instruction"] == "forward":
            horizontal += row["value"]
            depth += aim * row["value"]
        elif row["instruction"] == "down":
            aim += row["value"]
        else:
            aim -= row["value"]

    print("part two")
    print(f"aim: {aim}, horizontal: {horizontal}, depth: {depth}, horizontal*depth: {horizontal*depth}")


if __name__ == "__main__":
    df = pd.read_csv(Path(__file__).parent / "input.csv", sep=" ", names=["instruction", "value"])

    part_one(df)
    part_two(df)
