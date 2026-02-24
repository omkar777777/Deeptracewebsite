import cv2
import numpy as np
import os

from .lsb_analysis import lsb_score
from .entropy_analysis import entropy_score
from .histogram_analysis import histogram_score
from .correlation_analysis import correlation_score
from .chi_square_analysis import chi_square_score
from .lsb_extraction import extract_lsb_variants
from .content_validator import validate_content
from .scoring_engine import aggregate_scores


DEBUG = False


# ==========================================
# Load Image (Convert BGR → RGB)
# ==========================================
def load_and_normalize_image(file_path):

    if not os.path.exists(file_path):
        raise ValueError("File not found")

    image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        raise ValueError("Invalid or unsupported image format")

    # Grayscale → 3-channel
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Remove alpha channel
    if len(image.shape) == 3 and image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    # Convert BGR → RGB (embedder used PIL RGB)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image


# ==========================================
# Main Image Analysis
# ==========================================
def analyze_image(file_path):

    try:
        image = load_and_normalize_image(file_path)

        # -----------------------------
        # Statistical Scores
        # -----------------------------
        lsb = lsb_score(image)
        entropy = entropy_score(image)
        histogram = histogram_score(image)
        correlation = correlation_score(image)
        chi_square = chi_square_score(image)

        if DEBUG:
            print("\nAnalyzing:", file_path)
            print("LSB:", lsb)
            print("Entropy:", entropy)
            print("Histogram:", histogram)
            print("Correlation:", correlation)
            print("Chi-Square:", chi_square)
            print("----------------------------------")

        result = aggregate_scores(
            lsb,
            entropy,
            histogram,
            correlation,
            chi_square
        )

        # -----------------------------
        # Multi-Variant LSB Extraction
        # -----------------------------
        hidden_found = False
        extracted_text = None

        candidates = extract_lsb_variants(image)

        best_score = 0
        best_text = None

        for candidate in candidates:

            cleaned_payload = candidate.rstrip(b"\x00")

            if not cleaned_payload or len(cleaned_payload) < 4:
                continue

            classification, decoded = validate_content(cleaned_payload)

            if classification in ["plaintext", "ciphertext"]:

                confidence = len(decoded)

                if confidence > best_score:
                    best_score = confidence
                    best_text = decoded
                    hidden_found = True

        # -----------------------------
        # Risk Escalation Logic
        # -----------------------------
        base_score = result["total_score"]

        if hidden_found:
            # Force minimum suspicion level
            base_score = max(base_score, 60)

        result["total_score"] = base_score

        # -----------------------------
        # 4-Tier Risk Classification
        # -----------------------------
        if base_score <= 25:
            risk = "Clean"
        elif base_score <= 50:
            risk = "Low Risk"
        elif base_score <= 80:
            risk = "Suspicious"
        else:
            risk = "High Risk"

        result["risk_level"] = risk
        result["hidden_content_found"] = hidden_found

        if hidden_found:
            result["extracted_content"] = best_text
        else:
            result["message"] = "No recoverable hidden content detected."

        return result

    except Exception as e:
        return {
            "total_score": 0,
            "risk_level": "Error",
            "hidden_content_found": False,
            "message": str(e),
            "details": {}
        }