import numpy as np
import os

# Optional OpenCV import
try:
    import cv2
except Exception:
    cv2 = None

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
# Utility: Convert NumPy types → Python types
# ==========================================
def make_json_safe(obj):
    """
    Recursively convert NumPy data types to native Python types
    so Flask can jsonify safely.
    """
    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_safe(v) for v in obj]
    elif isinstance(obj, np.generic):
        return obj.item()
    else:
        return obj


# ==========================================
# Load Image (Convert BGR → RGB)
# ==========================================
def load_and_normalize_image(file_path):

    if not os.path.exists(file_path):
        raise ValueError("File not found")

    if cv2 is None:
        raise RuntimeError("OpenCV (cv2) is not available in this runtime")

    image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        raise ValueError("Invalid or unsupported image format")

    # Grayscale → 3-channel
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Remove alpha channel
    if len(image.shape) == 3 and image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    # Convert BGR → RGB
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
        lsb = float(lsb_score(image))
        entropy_val = float(entropy_score(image))
        histogram = float(histogram_score(image))
        correlation = float(correlation_score(image))
        chi_square = float(chi_square_score(image))

        if DEBUG:
            print("\nAnalyzing:", file_path)
            print("LSB:", lsb)
            print("Entropy:", entropy_val)
            print("Histogram:", histogram)
            print("Correlation:", correlation)
            print("Chi-Square:", chi_square)
            print("----------------------------------")

        # Aggregate scores
        result = aggregate_scores(
            lsb,
            entropy_val,
            histogram,
            correlation,
            chi_square
        )

        # Ensure total_score exists & is float
        base_score = float(result.get("total_score", 0))

        # -----------------------------
        # Multi-Variant LSB Extraction
        # -----------------------------
        hidden_found = False
        best_score = 0
        best_text = None

        candidates = extract_lsb_variants(image)

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
        if hidden_found:
            base_score = max(base_score, 60)

        # -----------------------------
        # Risk Classification
        # -----------------------------
        if base_score <= 25:
            risk = "Clean"
        elif base_score <= 50:
            risk = "Low Risk"
        elif base_score <= 80:
            risk = "Suspicious"
        else:
            risk = "High Risk"

        # -----------------------------
        # Final Result
        # -----------------------------
        final_result = {
            "total_score": float(base_score),
            "risk_level": str(risk),
            "hidden_content_found": bool(hidden_found),
        }

        if hidden_found:
            final_result["extracted_content"] = str(best_text)
        else:
            final_result["message"] = "No recoverable hidden content detected."

        # Make everything JSON safe
        return make_json_safe(final_result)

    except Exception as e:
        return {
            "total_score": 0.0,
            "risk_level": "Error",
            "hidden_content_found": False,
            "message": str(e),
            "details": {}
        }