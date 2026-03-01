import numpy as np


def lsb_score(image):
    flat = image.flatten()

    lsb_bits = flat & 1
    zeros = np.sum(lsb_bits == 0)
    ones = np.sum(lsb_bits == 1)

    total = zeros + ones
    ratio = abs(zeros - ones) / total

    score = min(int((1 - ratio) * 25), 25)

    return score