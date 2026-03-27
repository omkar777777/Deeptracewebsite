import numpy as np

# Optional OpenCV import
try:
    import cv2
except Exception:
    cv2 = None

from .lsb_analysis import lsb_score
from .entropy_analysis import entropy_score
from .lsb_extraction import extract_lsb_payload
from .content_validator import validate_content
from .scoring_engine import aggregate_image_scores
from .rs_analysis import rs_score
from .spa_analysis import spa_score
from .srm_analysis import srm_score
from .cnn_analysis import cnn_score


# ==========================================
# Normalize Image to RGB
# ==========================================
def load_and_normalize_image(file_path):
    if cv2 is None:
        raise RuntimeError("OpenCV (cv2) is not available in this environment. Steganalysis is disabled on Vercel Serverless.")

    image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        raise ValueError("Invalid or unsupported image format")

    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    if len(image.shape) == 3 and image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

# Convert BGR → RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image


# ==========================================
# Main Image Analysis
# ==========================================
def analyze_image(file_path):

    image = load_and_normalize_image(file_path)

    # Statistical Scores (0-100)
    lsb_anomaly = lsb_score(image)
    entropy_dev = entropy_score(image)
    rs_anomaly = rs_score(image)
    spa_anomaly = spa_score(image)

    # Advanced Detection Layers (0-100 placeholder/ML scores)
    srm_anomaly = srm_score(image)
    cnn_anomaly = cnn_score(image)

    # --------------------------------------
    # LSB Extraction Attempt (ALWAYS RUN)
    # --------------------------------------

    extraction_success = False
    valid_content = False
    extracted_text = None
    extraction_type = None

    payload_results = extract_lsb_payload(image)
    
    for p in payload_results:
        byte_data = p["data"]
        delimiter_detected = p["delimiter"]
        
        if delimiter_detected:
            extraction_success = True
            
        content_type, decoded = validate_content(byte_data)
        
        if content_type in ("plaintext", "cipher text"):
            extraction_success = True
            valid_content = True
            extracted_text = decoded
            extraction_type = content_type
            break

    result = aggregate_image_scores(
        lsb_anomaly=lsb_anomaly,
        entropy_deviation=entropy_dev,
        rs_anomaly=rs_anomaly,
        spa_anomaly=spa_anomaly,
        srm_anomaly=srm_anomaly,
        cnn_anomaly=cnn_anomaly,
        extraction_success=extraction_success,
        content_validity=valid_content
    )

    result["hidden_content_found"] = valid_content

    if valid_content:
        result["extracted_content"] = extracted_text
        result["extraction_type"] = extraction_type
        result["message"] = f"Hidden content ({extraction_type}) successfully extracted."
    else:
        result["message"] = "No valid hidden content found."

    return result
