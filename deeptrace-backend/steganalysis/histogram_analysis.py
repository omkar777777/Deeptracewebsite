import numpy as np


def histogram_score(image):
    flat = image.flatten()

    hist, _ = np.histogram(flat, bins=256, range=(0, 255))

    diff = np.abs(np.diff(hist))
    anomaly = np.mean(diff)

    normalized = min(anomaly / 1000, 1)

    score = int(normalized * 25)

    return score