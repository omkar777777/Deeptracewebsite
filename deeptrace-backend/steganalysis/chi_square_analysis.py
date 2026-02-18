import numpy as np


def chi_square_score(image):
    """
    Performs Chi-Square analysis on image pixel pairs.
    Detects unnatural equalization caused by LSB embedding.
    """

    # Convert to grayscale for statistical consistency
    gray = np.mean(image, axis=2).astype(np.uint8)

    flat = gray.flatten()

    # Compute histogram
    hist, _ = np.histogram(flat, bins=256, range=(0, 256))

    chi_square = 0

    # Iterate over pixel pairs (0,1), (2,3), ..., (254,255)
    for i in range(0, 256, 2):
        observed_1 = hist[i]
        observed_2 = hist[i + 1]

        expected = (observed_1 + observed_2) / 2

        if expected > 0:
            chi_square += ((observed_1 - expected) ** 2) / expected
            chi_square += ((observed_2 - expected) ** 2) / expected

    # Normalize chi-square value
    normalized = min(chi_square / 10000, 1)

    score = int(normalized * 25)

    return score