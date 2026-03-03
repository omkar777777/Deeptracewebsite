import numpy as np
from scipy.stats import entropy


def entropy_score(image):
    # Shannon entropy calculation: H(X) = −Σ p(x) log₂ p(x)
    
    # We calculate the entropy of the LSB plane specifically, as it's more sensitive
    flat = image.flatten()
    lsb_bits = flat & 1
    
    # Pack bits into bytes for entropy calculation
    # Just grab chunks of 8 bits and calculate entropy
    # To avoid shape errors, we truncate to a multiple of 8
    length = (len(lsb_bits) // 8) * 8
    if length == 0:
        return 0
        
    byte_array = np.packbits(lsb_bits[:length])
    
    hist, _ = np.histogram(byte_array, bins=256, range=(0, 255))
    prob = hist / np.sum(hist)
    
    ent = entropy(prob, base=2)
    
    # Max entropy for 8-bit is 8.0.
    # Natural images usually have LSB plane byte entropy around 7.5 - 7.9.
    # If it is >= 7.99, it's very likely encrypted data.
    
    if ent > 7.99:
        score = 100
    elif ent > 7.95:
        score = 75
    elif ent > 7.90:
        score = 50
    else:
        score = min(int((ent / 8.0) * 30), 30)
        
    return score