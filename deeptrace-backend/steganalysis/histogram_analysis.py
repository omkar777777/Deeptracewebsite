import numpy as np


def histogram_score(image):
    """
    Detects even–odd histogram pair equalization.

    LSB embedding reduces deviation between even–odd pairs.
    Lower relative deviation → higher suspicion.

    Returns score between 0–25.
    """

    # Convert to grayscale
    gray = np.mean(image, axis=2).astype(np.uint8)
    flat = gray.flatten()

    hist, _ = np.histogram(flat, bins=256, range=(0, 256))

    pair_differences = []
    pair_totals = []

    for i in range(0, 256, 2):
        even = hist[i]
        odd = hist[i + 1]

        total = even + odd
        if total > 0:
            pair_differences.append(abs(even - odd))
            pair_totals.append(total)

    if len(pair_totals) == 0:
        return 0

    pair_differences = np.array(pair_differences, dtype=np.float64)
    pair_totals = np.array(pair_totals, dtype=np.float64)

    # Relative deviation per pair
    relative_deviation = pair_differences / pair_totals

    anomaly = np.mean(relative_deviation)

    # -------------------------------------
    # Suspicion Logic (Inverted)
    # -------------------------------------
    # Natural images ≈ 0.15–0.30
    # Strong LSB embedding → < 0.08

    high_threshold = 0.30   # clearly natural
    low_threshold = 0.05    # strongly equalized

    if anomaly >= high_threshold:
        return 0  # natural

    if anomaly <= low_threshold:
        return 25  # highly suspicious

    # Linear interpolation between thresholds
    normalized = (high_threshold - anomaly) / (high_threshold - low_threshold)

    score = int(normalized * 25)

    return max(0, min(score, 25))