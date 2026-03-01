import cv2
import numpy as np

from .lsb_analysis import lsb_score
from .entropy_analysis import entropy_score
from .histogram_analysis import histogram_score
from .correlation_analysis import correlation_score
from .chi_square_analysis import chi_square_score
from .lsb_extraction import extract_lsb_payload
from .content_validator import validate_content
from .scoring_engine import aggregate_scores


# ==========================================
# Normalize Image to RGB
# ==========================================
def load_and_normalize_image(file_path):

    image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        raise ValueError("Invalid or unsupported image format")

    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    if len(image.shape) == 3 and image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image


# ==========================================
# Main Image Analysis
# ==========================================
def analyze_image(file_path):

    image = load_and_normalize_image(file_path)

    # Statistical Scores
    lsb = lsb_score(image)
    entropy = entropy_score(image)
    histogram = histogram_score(image)
    correlation = correlation_score(image)
    chi_square = chi_square_score(image)

    result = aggregate_scores(
        lsb,
        entropy,
        histogram,
        correlation,
        chi_square
    )

    # --------------------------------------
    # Conditional LSB Extraction Attempt
    # --------------------------------------

    hidden_found = False
    extracted_text = None

    if result["risk_level"] != "Clean":

        raw_payload = extract_lsb_payload(image)

        is_valid, decoded = validate_content(raw_payload)

        if is_valid:
            hidden_found = True
            extracted_text = decoded

    result["hidden_content_found"] = hidden_found

    if hidden_found:
        result["extracted_content"] = extracted_text
    else:
        result["message"] = "No valid hidden content found."

    return result