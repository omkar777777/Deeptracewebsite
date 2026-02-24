import numpy as np
from scipy.stats import entropy


def entropy_score(image):
    """
    Measures global entropy deviation from natural range.

    Natural images: ~7.2 – 7.8
    Extremely close to 8.0 can indicate heavy embedding.
    Returns score between 0–25.
    """

    flat = image.flatten()

    hist, _ = np.histogram(flat, bins=256, range=(0, 256))
    total = np.sum(hist)

    if total == 0:
        return 0

    prob = hist / total
    ent = entropy(prob, base=2)

    # -------------------------------------
    # Calibrated Suspicion Logic
    # -------------------------------------

    natural_center = 7.5
    max_entropy = 8.0

    # Distance from maximum entropy
    distance_from_max = max_entropy - ent

    # If far from max entropy → natural
    if distance_from_max > 0.4:
        return 0

    # If extremely close to max → suspicious
    tight_threshold = 0.05

    if distance_from_max <= tight_threshold:
        return 25

    # Linear interpolation between 0.4 and 0.05
    normalized = (0.4 - distance_from_max) / (0.4 - tight_threshold)

    score = int(normalized * 25)

    return max(0, min(score, 25))