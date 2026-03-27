def aggregate_image_scores(lsb_anomaly, entropy_deviation, rs_anomaly, spa_anomaly, srm_anomaly, cnn_anomaly, extraction_success, content_validity):
    # Weights for Risk Assessment Engine
    # By stacking multi-layered deep detections, we form a comprehensive anomaly rating.
    w1 = 0.05  # LSB anomaly
    w2 = 0.05  # Entropy deviation
    w3 = 0.05  # RS anomaly
    w4 = 0.05  # SPA anomaly
    w_srm = 0.10 # SRM anomaly
    w_cnn = 0.10 # CNN anomaly
    w5 = 0.20  # Extraction success
    w6 = 0.40  # Content validity

    risk_percentage = (
        (lsb_anomaly * w1) +
        (entropy_deviation * w2) +
        (rs_anomaly * w3) +
        (spa_anomaly * w4) +
        (srm_anomaly * w_srm) +
        (cnn_anomaly * w_cnn) +
        ((100 if extraction_success else 0) * w5) +
        ((100 if content_validity else 0) * w6)
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
    elif any(score > 75 for score in [lsb_anomaly, entropy_deviation, rs_anomaly, spa_anomaly, srm_anomaly, cnn_anomaly]):
        confidence = "Moderate (Statistical/Feature Anomaly)"
    else:
        confidence = "Low (No Anomalies Detected)"

    return {
        "risk_percentage": risk_percentage,
        "risk_classification": classification,
        "confidence_level": confidence,
        "details": {
            "lsb_anomaly_score": lsb_anomaly,
            "entropy_deviation_score": entropy_deviation,
            "rs_anomaly_score": rs_anomaly,
            "spa_anomaly_score": spa_anomaly,
            "srm_anomaly_score": srm_anomaly,
            "cnn_anomaly_score": cnn_anomaly,
            "extraction_success": extraction_success,
            "content_validity": content_validity
        }
    }

def aggregate_file_scores(bit_score, entropy_score, size_score, header_score, chi_square=0):
    w1 = 0.25
    w2 = 0.25
    w3 = 0.25
    w4 = 0.25
    
    risk_percentage = (
        (bit_score * w1) +
        (entropy_score * w2) +
        (size_score * w3) +
        (header_score * w4)
    )
    
    risk_percentage = min(max(int(risk_percentage), 0), 100)

    if risk_percentage <= 30:
        classification = "Low"
    elif risk_percentage <= 70:
        classification = "Moderate"
    else:
        classification = "High"
        
    confidence = "Low (No Anomalies Detected)"
    if risk_percentage > 75:
        confidence = "Moderate (Statistical Anomaly)"
        
    return {
        "risk_percentage": risk_percentage,
        "risk_classification": classification,
        "confidence_level": confidence,
        "details": {
            "bit_distribution_score": bit_score,
            "entropy_deviation_score": entropy_score,
            "size_anomaly_score": size_score,
            "header_anomaly_score": header_score
        }
    }