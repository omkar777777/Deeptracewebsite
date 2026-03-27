import numpy as np

def rs_score(image):
    """
    RS (Regular-Singular) Analysis for LSB Steganography detection.
    Splits pixels into groups of 4, applies LSB flipping, and measures smoothness changes.
    Returns a normalized anomaly score 0-100.
    """
    try:
        pixels = image.flatten().astype(np.int32)
        
        n = len(pixels)
        n = n - (n % 4)
        if n < 4:
            return 0
            
        pixels = pixels[:n]
        groups = pixels.reshape(-1, 4)
        
        # Original smoothness
        diffs = np.abs(np.diff(groups, axis=1))
        f_orig = np.sum(diffs, axis=1)
        
        # Flipping function (LSB flip is mathematically equivalent to XOR 1)
        flipped_groups = groups ^ 1
        flipped_diffs = np.abs(np.diff(flipped_groups, axis=1))
        f_flip = np.sum(flipped_diffs, axis=1)
        
        R = np.sum(f_flip < f_orig)
        S = np.sum(f_flip > f_orig)
        
        total = R + S
        if total == 0:
            return 0
            
        embedding_rate = abs(R - S) / total
        
        score = min(int(embedding_rate * 100), 100)
        return score
    except Exception:
        return 0
