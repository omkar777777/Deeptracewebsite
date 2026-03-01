import numpy as np
from scipy.stats import entropy


def entropy_score(image):
    flat = image.flatten()

    hist, _ = np.histogram(flat, bins=256, range=(0, 255))
    prob = hist / np.sum(hist)

    ent = entropy(prob, base=2)

    # Normalize entropy (typical image entropy ~7-8)
    normalized = min(ent / 8, 1)

    score = int(normalized * 25)

    return score