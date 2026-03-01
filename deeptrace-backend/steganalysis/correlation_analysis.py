import numpy as np


def correlation_score(image):
    gray = np.mean(image, axis=2)

    right_shift = np.roll(gray, -1, axis=1)

    correlation = np.corrcoef(
        gray.flatten(), right_shift.flatten()
    )[0, 1]

    correlation = 0 if np.isnan(correlation) else correlation

    score = int((1 - correlation) * 25)

    return max(min(score, 25), 0)