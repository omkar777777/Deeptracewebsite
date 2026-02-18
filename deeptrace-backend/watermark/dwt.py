import numpy as np
from PIL import Image

def dwt_2d(layer):
    """
    1-level 2D Haar DWT using NumPy.
    Input: 2D numpy array (even dims)
    Output: LL, LH, HL, HH subbands
    """
    h, w = layer.shape
    
    # Rows
    L_row = (layer[:, 0::2] + layer[:, 1::2]) / 2
    H_row = (layer[:, 0::2] - layer[:, 1::2]) / 2
    
    # Cols (applied to row results)
    LL = (L_row[0::2, :] + L_row[1::2, :]) / 2
    LH = (L_row[0::2, :] - L_row[1::2, :]) / 2
    HL = (H_row[0::2, :] + H_row[1::2, :]) / 2
    HH = (H_row[0::2, :] - H_row[1::2, :]) / 2
    
    return LL, LH, HL, HH

def idwt_2d(LL, LH, HL, HH):
    """
    1-level 2D Inverse Haar DWT.
    """
    h, w = LL.shape
    
    # Inverse Cols
    L_row = np.zeros((h*2, w), dtype=float)
    H_row = np.zeros((h*2, w), dtype=float)
    
    L_row[0::2, :] = LL + LH
    L_row[1::2, :] = LL - LH
    
    H_row[0::2, :] = HL + HH
    H_row[1::2, :] = HL - HH
    
    # Inverse Rows
    layer = np.zeros((h*2, w*2), dtype=float)
    layer[:, 0::2] = L_row + H_row
    layer[:, 1::2] = L_row - H_row
    
    return layer

import hashlib

def get_deterministic_seed(key):
    return int(hashlib.sha256(key.encode('utf-8')).hexdigest(), 16) % (2**32)

def embed_dwt(image, secret_key, watermark_text):
    """
    Embeds text into the image using DWT (Haar) algorithm.
    Embeds in the HL subband (vertical details).
    """
    # 1. Convert to YCbCr, use Y channel
    img = image.convert("YCbCr")
    y, cb, cr = img.split()
    y_data = np.array(y, dtype=float)
    
    h, w = y_data.shape
    
    # 2. Pad to even dimensions
    pad_h = h % 2
    pad_w = w % 2
    if pad_h or pad_w:
        y_data = np.pad(y_data, ((0, pad_h), (0, pad_w)), mode='edge')
    
    # 3. Apply DWT
    LL, LH, HL, HH = dwt_2d(y_data)
    
    # 4. Prepare watermark bits
    bits = ''.join(format(ord(c), '08b') for c in watermark_text)
    bits += '00000000'
    
    # FIX: Only use coefficients that correspond to original image pixels
    # DWT reduces size by 2. Padding adds coefficients to the right/bottom.
    usable_h = h // 2
    usable_w = w // 2
    capacity = usable_h * usable_w
    
    if len(bits) > capacity:
        raise ValueError("Message too long for DWT embedding.")
    
    # 5. Shuffle indices
    np.random.seed(get_deterministic_seed(secret_key))
    indices = np.arange(capacity)
    np.random.shuffle(indices)
    
    # 6. Embed using QIM-like or simple modulation
    # Here using simple additive modulation for 0/1 differentiation
    alpha = 5 # Strength
    
    for i, bit in enumerate(bits):
        idx = indices[i]
        
        # Map linear index to 2D coordinates in usable region
        r = idx // usable_w
        c = idx % usable_w
        
        val = HL[r, c] 
        delta = 10 
        
        q = round(val / delta)
        rem = q % 2
        
        if bit == '0':
            if rem != 0: q += 1 # Make even
        else: # bit '1'
            if rem == 0: q += 1 # Make odd
            
        HL[r, c] = q * delta
        
    # Reshape back (Not needed if we modified HL in place)
    # HL = flat_HL.reshape(HL.shape) -> REMOVED since we modify 2D HL directly
    
    # 7. Inverse DWT
    y_rec = idwt_2d(LL, LH, HL, HH)
    
    # Remove padding
    y_rec = y_rec[:h, :w]
    y_rec = np.clip(y_rec, 0, 255)
    
    y_new = Image.fromarray(y_rec.astype(np.uint8), mode='L')
    return Image.merge("YCbCr", (y_new, cb, cr)).convert("RGB")

def extract_dwt(image, secret_key):
    """
    Extracts text from DWT (HL subband)
    """
    img = image.convert("YCbCr")
    y, _, _ = img.split()
    y_data = np.array(y, dtype=float)
    
    h, w = y_data.shape
    
    pad_h = h % 2
    pad_w = w % 2
    if pad_h or pad_w:
        y_data = np.pad(y_data, ((0, pad_h), (0, pad_w)), mode='edge')
        
    LL, LH, HL, HH = dwt_2d(y_data)
    
    # FIX: Use usable capacity
    usable_h = h // 2
    usable_w = w // 2
    capacity = usable_h * usable_w

    np.random.seed(get_deterministic_seed(secret_key))
    indices = np.arange(capacity)
    np.random.shuffle(indices)
    
    bits = ""
    delta = 10
    
    # Extract until null terminator or reasonable limit
    # We iterate a safe amount or until terminator
    max_bits = min(capacity, 10000) # 10k bits limit
    
    for i in range(max_bits):
        idx = indices[i]
        
        r = idx // usable_w
        c = idx % usable_w
        
        val = HL[r, c]
        
        q = round(val / delta)
        rem = q % 2
        
        if rem == 0:
            bits += '0'
        else:
            bits += '1'
            
        if len(bits) % 8 == 0:
            if bits[-8:] == '00000000':
                bits = bits[:-8]
                break
                
    try:
        chars = []
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            chars.append(chr(int(byte, 2)))
        return "".join(chars)
    except Exception:
        return ""
