def aggregate_scores(lsb, entropy, histogram, correlation, chi_square):

    # Total score (Max = 125)
    total = lsb + entropy + histogram + correlation + chi_square
    
    # Normalize to 100% scale
    normalized_percent = int((total / 125.0) * 100)

    # Updated thresholds for 0–100 scale
    if normalized_percent <= 30:
        risk = "Clean"
    elif normalized_percent <= 60:
        risk = "Suspicious"
    else:
        risk = "High Risk"

    return {
        "total_score": normalized_percent,
        "risk_level": risk,
        "details": {
            "lsb_score": lsb,
            "entropy_score": entropy,
            "histogram_score": histogram,
            "correlation_score": correlation,
            "chi_square_score": chi_square
        },
    }