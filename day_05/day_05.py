from pathlib import Path
import re
import numpy as np
import matplotlib.pyplot as plt


def create_ground_floor_map(coordinates, part_two=False):
    # x1, y1, x2, y2
    ground_floor = np.zeros((np.max(coordinates) + 1, np.max(coordinates) + 1))
    for row in coordinates:
        x1, y1, x2, y2 = row
        if x1 == x2:
            ground_floor[min(y1, y2):max(y1, y2) + 1, x1] += 1
        elif y1 == y2:
            ground_floor[y1, min(x1, x2):max(x1, x2) + 1] += 1
        elif part_two:
            # When lines are diagonal
            diff = abs(x1-x2)
            for i in range(diff+1):
                # When the diagonals are increasing then i increases for the coordinate
                y_ind = i if y2 > y1 else -i
                x_ind = i if x2 > x1 else -i
                ground_floor[y1 + y_ind, x1 + x_ind] += 1

    return ground_floor


if __name__ == "__main__":
    with open(Path(__file__).parent / "input_test.txt", "r") as f:
        coordinates_raw = f.readlines()
        # print(coordinates_raw)
        coordinates = np.stack([np.array(re.findall("\d+", row), dtype=int) for row in coordinates_raw])
        print("Test coordinates:")
        print(coordinates)

    ground_floor = create_ground_floor_map(coordinates)
    result = np.sum(ground_floor >= 2)
    assert result == 5
    plt.imshow(ground_floor)
    plt.colorbar()
    plt.show()
    ground_floor = create_ground_floor_map(coordinates, part_two=True)
    result = np.sum(ground_floor >= 2)
    plt.imshow(ground_floor)
    plt.colorbar()
    plt.show()
    print(result)
    assert result == 12
    assert np.sum(ground_floor==1) == 27
    assert np.sum(ground_floor==3) == 2
    print()

    # When we are here the tests have not failed and we should get the correct result
    with open(Path(__file__).parent / "input.txt", "r") as f:
        coordinates_raw = f.readlines()
        # print(coordinates_raw)
        coordinates = np.stack([np.array(re.findall("\d+", row), dtype=int) for row in coordinates_raw])
        print("Real input:")
        print(coordinates)
    ground_floor = create_ground_floor_map(coordinates)
    plt.imshow(ground_floor)
    plt.colorbar()
    plt.show()
    result = np.sum(ground_floor >= 2)
    print("Horizontal and vertical: ", result)

    ground_floor = create_ground_floor_map(coordinates, part_two=True)
    plt.imshow(ground_floor)
    plt.colorbar()
    plt.show()
    result = np.sum(ground_floor >= 2)
    print("Horizontal, vertical and diagonal: ", result)

