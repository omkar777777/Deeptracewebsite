import numpy as np


def lsb_score(image):
    # Detects abnormal bit uniformity.
    # In a natural image, LSBs are pseudo-random but not perfectly uniform.
    # If a message is encrypted or compressed, it's very close to 50/50.
    
    flat = image.flatten()
    lsb_bits = flat & 1
    
    zeros = np.sum(lsb_bits == 0)
    ones = np.sum(lsb_bits == 1)
    
    total = zeros + ones
    if total == 0:
        return 0
        
    ratio = ones / total
    
    # perfectly random is 0.5. 
    # deviation from 0.5:
    deviation = abs(ratio - 0.5)
    
    # If deviation is very small (e.g. < 0.005), it's highly anomalous (too perfectly random).
    # If deviation is larger, it's more natural.
    
    if deviation < 0.001:
        score = 100
    elif deviation < 0.005:
        score = 80
    elif deviation < 0.01:
        score = 50
    else:
        score = 10
        
    return score