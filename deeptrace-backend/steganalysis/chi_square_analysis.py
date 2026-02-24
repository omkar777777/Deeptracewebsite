import numpy as np
import math


def chi_square_score(image):
    """
    Chi-square test for even–odd pair equalization.

    LSB embedding reduces chi-square value.
    Lower avg_chi → more suspicious.
    Returns score between 0–25.
    """

    gray = np.mean(image, axis=2).astype(np.uint8)
    flat = gray.flatten()

    hist, _ = np.histogram(flat, bins=256, range=(0, 256))

    chi_square = 0.0
    pair_count = 0

    for i in range(0, 256, 2):
        observed_1 = hist[i]
        observed_2 = hist[i + 1]

        total_pair = observed_1 + observed_2
        if total_pair == 0:
            continue

        expected = total_pair / 2

        chi_square += ((observed_1 - expected) ** 2) / expected
        chi_square += ((observed_2 - expected) ** 2) / expected

        pair_count += 1

    if pair_count == 0:
        return 0

    avg_chi = chi_square / pair_count

    # -------------------------------------
    # Suspicion Logic (Inverted)
    # -------------------------------------
    # Natural images → avg_chi typically high
    # Embedded images → avg_chi drops

    high_threshold = 500    # natural region
    low_threshold = 50      # strong embedding region

    if avg_chi >= high_threshold:
        return 0  # natural

    if avg_chi <= low_threshold:
        return 25  # highly suspicious

    # Linear interpolation between thresholds
    normalized = (high_threshold - avg_chi) / (high_threshold - low_threshold)

    score = int(normalized * 25)

    return max(0, min(score, 25))