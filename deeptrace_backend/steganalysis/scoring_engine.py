def aggregate_scores(lsb, entropy, histogram, correlation, chi_square):

    # Total score (Max = 125)
    total = lsb + entropy + histogram + correlation + chi_square

    # Updated thresholds for 0–125 scale
    if total <= 40:
        risk = "Clean"
    elif total <= 75:
        risk = "Suspicious"
    else:
        risk = "High Risk"

    return {
        "total_score": total,
        "risk_level": risk,
        "details": {
            "lsb_score": lsb,
            "entropy_score": entropy,
            "histogram_score": histogram,
            "correlation_score": correlation,
            "chi_square_score": chi_square
        },
    }