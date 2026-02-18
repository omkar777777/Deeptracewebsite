import os
import numpy as np
from scipy.stats import entropy

from .scoring_engine import aggregate_scores


# ==========================================
# Helper: Read file as binary
# ==========================================
def read_binary(file_path):
    with open(file_path, "rb") as f:
        return f.read()


# ==========================================
# 1️⃣ Byte-Level Entropy Analysis
# ==========================================
def file_entropy_score(data):
    byte_array = np.frombuffer(data, dtype=np.uint8)

    hist, _ = np.histogram(byte_array, bins=256, range=(0, 256))
    total = np.sum(hist)

    if total == 0:
        return 0

    prob = hist / total
    ent = entropy(prob, base=2)

    # Normalize (max entropy for byte = 8)
    normalized = min(ent / 8, 1)

    return int(normalized * 25)


# ==========================================
# 2️⃣ Bit Distribution (LSB Bias)
# ==========================================
def bit_distribution_score(data):
    byte_array = np.frombuffer(data, dtype=np.uint8)

    if len(byte_array) == 0:
        return 0

    lsb_bits = byte_array & 1
    zeros = np.sum(lsb_bits == 0)
    ones = np.sum(lsb_bits == 1)

    total = zeros + ones
    if total == 0:
        return 0

    imbalance = abs(zeros - ones) / total

    score = min(int((1 - imbalance) * 25), 25)

    return score


# ==========================================
# 3️⃣ File Size Anomaly
# ==========================================
def file_size_score(file_path):
    size = os.path.getsize(file_path)

    # Normalize size suspicion (5MB threshold)
    normalized = min(size / (5 * 1024 * 1024), 1)

    return int(normalized * 25)


# ==========================================
# 4️⃣ Header Consistency Check
# ==========================================
def header_score(data):
    signatures = {
        b"%PDF": "pdf",
        b"\x89PNG": "png",
        b"\xFF\xD8\xFF": "jpg",
        b"PK\x03\x04": "zip",
    }

    header = data[:8]

    for sig in signatures:
        if header.startswith(sig):
            return 0  # Valid header → low suspicion

    return 15  # Unknown header → moderate suspicion


# ==========================================
# Main File Analysis Function
# ==========================================
def analyze_file(file_path):

    data = read_binary(file_path)

    entropy_score_val = file_entropy_score(data)
    bit_score_val = bit_distribution_score(data)
    size_score_val = file_size_score(file_path)
    header_score_val = header_score(data)

    # IMPORTANT: Pass 0 for chi_square (image-only metric)
    result = aggregate_scores(
        bit_score_val,
        entropy_score_val,
        size_score_val,
        header_score_val,
        0   # chi_square placeholder
    )

    return result