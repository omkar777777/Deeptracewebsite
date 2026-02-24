import numpy as np


def correlation_score(image):
    """
    Measures horizontal pixel correlation.

    Natural images:
        correlation ≈ 0.85 – 0.98

    LSB embedding slightly reduces correlation.
    Lower correlation → higher suspicion.

    Returns score between 0–25.
    """

    # Convert to grayscale
    gray = np.mean(image, axis=2)

    # Horizontal shift
    shifted = np.roll(gray, 1, axis=1)

    # Compute correlation
    corr_matrix = np.corrcoef(gray.flatten(), shifted.flatten())
    corr = corr_matrix[0, 1]

    if np.isnan(corr):
        return 0

    # -------------------------------------
    # Suspicion Logic
    # -------------------------------------
    # Natural region
    high_threshold = 0.95   # very natural
    low_threshold = 0.75    # strong degradation

    if corr >= high_threshold:
        return 0  # clearly natural

    if corr <= low_threshold:
        return 25  # highly suspicious

    # Linear interpolation
    normalized = (high_threshold - corr) / (high_threshold - low_threshold)

    score = int(normalized * 25)

    return max(0, min(score, 25))