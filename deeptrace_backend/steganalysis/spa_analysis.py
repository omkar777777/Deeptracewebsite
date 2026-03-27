import numpy as np

def spa_score(image):
    """
    Sample Pair Analysis (SPA) for LSB Steganography detection.
    Analyzes transitions between pixel pairs to detect LSB embedding.
    Returns a normalized anomaly score 0-100.
    """
    try:
        pixels = image.flatten().astype(np.int32)
        
        n = len(pixels)
        n = n - (n % 2)
        if n < 2:
            return 0
            
        pixels = pixels[:n]
        pairs = pixels.reshape(-1, 2)
        
        # Detect odd-even and even-odd transitions
        even_x = (pairs[:, 0] % 2 == 0)
        odd_y = (pairs[:, 1] % 2 == 1)
        even_odd = np.sum(even_x & odd_y)
        
        odd_x = (pairs[:, 0] % 2 == 1)
        even_y = (pairs[:, 1] % 2 == 0)
        odd_even = np.sum(odd_x & even_y)
        
        total = even_odd + odd_even
        if total == 0:
            return 0
            
        embedding_rate = abs(even_odd - odd_even) / total
        
        score = min(int(embedding_rate * 100), 100)
        return score
    except Exception:
        return 0
