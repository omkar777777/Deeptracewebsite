def aggregate_scores(lsb, entropy, histogram, correlation, chi_square):
    """
    Weighted aggregation normalized to 0–100 scale.
    All metric inputs expected in range 0–25.
    """

    # -----------------------------
    # Weight Configuration
    # -----------------------------
    weights = {
        "lsb": 1.1,
        "entropy": 1.0,
        "histogram": 1.0,
        "correlation": 0.9,
        "chi_square": 1.0
    }

    # -----------------------------
    # Weighted Sum
    # -----------------------------
    weighted_total = (
        lsb * weights["lsb"] +
        entropy * weights["entropy"] +
        histogram * weights["histogram"] +
        correlation * weights["correlation"] +
        chi_square * weights["chi_square"]
    )

    max_possible = 25 * sum(weights.values())

    # -----------------------------
    # Normalize to 0–100
    # -----------------------------
    normalized_total = (weighted_total / max_possible) * 100
    normalized_total = int(max(0, min(normalized_total, 100)))

    # -----------------------------
    # 4-Tier Risk Classification
    # -----------------------------
    if normalized_total <= 25:
        risk = "Clean"
    elif normalized_total <= 50:
        risk = "Low Risk"
    elif normalized_total <= 80:
        risk = "Suspicious"
    else:
        risk = "High Risk"

    return {
        "total_score": normalized_total,
        "risk_level": risk,
        "details": {
            "lsb_score": lsb,
            "entropy_score": entropy,
            "histogram_score": histogram,
            "correlation_score": correlation,
            "chi_square_score": chi_square
        }
    }