def aggregate_scores(lsb_anomaly, entropy_deviation, extraction_success, content_validity):
    # Weights for Risk Assessment Engine
    w1 = 0.20  # LSB anomaly
    w2 = 0.20  # Entropy deviation
    w3 = 0.20  # Extraction success
    w4 = 0.40  # Content validity

    risk_percentage = (
        (lsb_anomaly * w1) +
        (entropy_deviation * w2) +
        ((100 if extraction_success else 0) * w3) +
        ((100 if content_validity else 0) * w4)
    )
    
    risk_percentage = min(max(int(risk_percentage), 0), 100)

    # Risk Classification
    if risk_percentage <= 30:
        classification = "Low"
    elif risk_percentage <= 70:
        classification = "Moderate"
    else:
        classification = "High"
        
    # Confidence Level
    if content_validity:
        confidence = "High (Content Decoded)"
    elif extraction_success:
        confidence = "Moderate (Delimiter/Pattern Detected)"
    elif lsb_anomaly > 75 or entropy_deviation > 75:
        confidence = "Moderate (Statistical Anomaly)"
    else:
        confidence = "Low (No Anomalies Detected)"

    return {
        "risk_percentage": risk_percentage,
        "risk_classification": classification,
        "confidence_level": confidence,
        "details": {
            "lsb_anomaly_score": lsb_anomaly,
            "entropy_deviation_score": entropy_deviation,
            "extraction_success": extraction_success,
            "content_validity": content_validity
        }
    }