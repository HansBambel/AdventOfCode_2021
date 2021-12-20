from pathlib import Path
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np


def transform_input(input_str: str) -> Tuple:
    data = input_str.replace("#", "1")
    data = data.replace(".", "0")
    enhancement_algorithm_string = np.array(list(data.split("\n")[0]), dtype=int)
    image_raw = np.array([list(line) for line in data.split("\n")[2:]], dtype=int)
    return enhancement_algorithm_string, image_raw


def decode(enhancement_algorithm_string, cutout) -> int:
    """Old manual decoding of converting the binary number to decimal."""
    # convert to str and remove brackets
    bin_str = np.array2string(cutout.reshape(-1), separator="")[1:-1]
    decimal = int(bin_str, 2)
    return enhancement_algorithm_string[decimal]


def enhance_image(enhancement_algorithm_string, image_raw):
    # returns an enhanced image
    conv = np.array([[256, 128, 64], [32, 16, 8], [4, 2, 1]])
    # pad with the value that is in the infinite size of the image
    resulting_image = image_raw.copy()
    for y in range(1, image_raw.shape[0] - 1):
        for x in range(1, image_raw.shape[1] - 1):
            # convolve the image
            index_for_alg = np.sum(image_raw[y - 1 : y + 2, x - 1 : x + 2] * conv)
            resulting_image[y, x] = enhancement_algorithm_string[index_for_alg]

    return resulting_image[1:-1, 1:-1]


data = Path(__file__).with_name("input_ex.txt").read_text()
enhancement_algorithm_string, image_raw = transform_input(data)
# plt.imshow(image_raw)
# plt.show()
pad = 100
image_raw = np.pad(image_raw, pad)
for i in range(50):
    image_raw = enhance_image(enhancement_algorithm_string, image_raw)
    # plt.imshow(image_raw)
    # plt.show()
    if i == 1:
        assert np.sum(image_raw) == 35
assert np.sum(image_raw) == 3351

data = Path(__file__).with_name("input_ex2.txt").read_text()
enhancement_algorithm_string, image_raw = transform_input(data)
# plt.imshow(image_raw)
# plt.show()
image_raw = np.pad(image_raw, pad)

for _ in range(2):
    image_raw = enhance_image(enhancement_algorithm_string, image_raw)
    # plt.imshow(image_raw)
    # plt.show()
assert np.sum(image_raw) == 5326

data = Path(__file__).with_name("input.txt").read_text()
enhancement_algorithm_string, image_raw = transform_input(data)
plt.imshow(image_raw)
plt.show()
image_raw = np.pad(image_raw, pad)

for i in range(50):
    image_raw = enhance_image(enhancement_algorithm_string, image_raw)
    plt.imshow(image_raw)
    plt.show()
    if i == 1:
        print(np.sum(image_raw))
print(np.sum(image_raw))
