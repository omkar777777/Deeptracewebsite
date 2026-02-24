import numpy as np


def lsb_score(image):
    """
    Measures LSB bit balance.

    Natural images already tend toward ~50/50 balance.
    Only extremely tight equalization (typical in LSB embedding)
    should raise suspicion.

    Returns score between 0 and 25.
    """

    flat = image.flatten()
    lsb_bits = flat & 1

    total = len(lsb_bits)
    if total == 0:
        return 0

    ones = np.sum(lsb_bits)
    zeros = total - ones

    ratio = ones / total
    deviation = abs(ratio - 0.5)

    # -------------------------------------
    # Calibrated Sensitivity
    # -------------------------------------
    # Natural images typically deviate 0.01–0.03
    # Embedded images often < 0.005 deviation

    tight_threshold = 0.005   # very tight balance
    loose_threshold = 0.05    # clearly natural imbalance

    if deviation >= loose_threshold:
        return 0  # clearly natural

    if deviation <= tight_threshold:
        return 25  # highly suspicious equalization

    # Linear interpolation between thresholds
    normalized = (loose_threshold - deviation) / (loose_threshold - tight_threshold)

    score = int(normalized * 25)

    return max(0, min(score, 25))