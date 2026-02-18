import numpy as np
from PIL import Image

def dct_2d(block):
    """
    Apply 2D Discrete Cosine Transform to an 8x8 block.
    Using explicit formula or matrix multiplication for pure NumPy implementation sans SciPy/OpenCV.
    """
    # Create DCT matrix for N=8
    N = 8
    n, k = np.meshgrid(np.arange(N), np.arange(N))
    # DCT matrix: C[k, n] = cos( (pi/N) * (n + 0.5) * k )
    # With normalization factors
    C = np.cos((np.pi / N) * (n + 0.5) * k) * np.sqrt(2.0 / N)
    C[0, :] /= np.sqrt(2) # First row correction
    
    # DCT = C * block * C.T
    return np.dot(np.dot(C, block), C.T)

def idct_2d(block):
    """
    Apply 2D Inverse Discrete Cosine Transform to an 8x8 block.
    """
    N = 8
    n, k = np.meshgrid(np.arange(N), np.arange(N))
    C = np.cos((np.pi / N) * (n + 0.5) * k) * np.sqrt(2.0 / N)
    C[0, :] /= np.sqrt(2)
    
    # IDCT = C.T * block * C
    return np.dot(np.dot(C.T, block), C)

import hashlib

def get_deterministic_seed(key):
    return int(hashlib.sha256(key.encode('utf-8')).hexdigest(), 16) % (2**32)

def embed_dct(image, secret_key, watermark_text):
    """
    Embeds text into the image using DCT algorithm.
    image: PIL Image object
    secret_key: seed for random location selection
    watermark_text: text to embed
    """
    # 1. Preprocess: Resize/Convert to YCbCr
    # We embed mainly in the Y channel (Luminance) or Blue channel in RGB.
    # To keep it simple and robust, let's use the Blue channel of RGB or Y of YCbCr.
    # YCbCr is better for imperceptibility.
    
    img = image.convert("YCbCr")
    y, cb, cr = img.split()
    y_data = np.array(y, dtype=float)
    
    h, w = y_data.shape
    
    # 2. Pad image to be divisible by 8
    pad_h = (8 - h % 8) % 8
    pad_w = (8 - w % 8) % 8
    if pad_h > 0 or pad_w > 0:
        y_data = np.pad(y_data, ((0, pad_h), (0, pad_w)), mode='edge')
    
    padded_h, padded_w = y_data.shape
    
    # 3. Prepare message bits
    # Convert text to binary
    bits = ''.join(format(ord(c), '08b') for c in watermark_text)
    bits += '00000000' # Null terminator
    
    # 4. Determine capacity and select blocks
    # FIX: Use original h/w to avoid writing into padded regions that get cropped
    blocks_h_usable = h // 8
    blocks_w_usable = w // 8
    num_blocks = blocks_h_usable * blocks_w_usable
    
    if len(bits) > num_blocks:
        raise ValueError(f"Message too long. Max chars: {num_blocks // 8}")
        
    # Shuffle block indices based on key
    np.random.seed(get_deterministic_seed(secret_key))
    block_indices = np.arange(num_blocks)
    np.random.shuffle(block_indices)
    
    # 5. Embed Bits
    
    for i, bit in enumerate(bits):
        idx = block_indices[i]
        # Use valid blocks width for row/col calculation
        r = (idx // blocks_w_usable) * 8
        c = (idx % blocks_w_usable) * 8
        
        block = y_data[r:r+8, c:c+8]
        dct_block = dct_2d(block - 128) # Center pixel values
        
        # Embed in mid-band coefficients (e.g., (3,3), (4,2))
        # Strategy: Ensure a > b for '1', b > a for '0' at two coupled locations
        # Selecting (4,3) and (3,4) as they are mid-frequency
        u1, v1 = 4, 3
        u2, v2 = 3, 4
        
        val1 = dct_block[u1, v1]
        val2 = dct_block[u2, v2]
        
        delta = 20 # Strength (robustness)
        
        if bit == '1':
            if val1 <= val2 + delta:
                dct_block[u1, v1] = val2 + delta / 2
                dct_block[u2, v2] = val2 - delta / 2
        else: # bit == '0'
            if val2 <= val1 + delta:
                dct_block[u2, v2] = val1 + delta / 2
                dct_block[u1, v1] = val1 - delta / 2
                
        # Reconstruct block
        y_data[r:r+8, c:c+8] = idct_2d(dct_block) + 128

    # 6. Clip and reconstruct image
    y_data = np.clip(y_data, 0, 255)
    
    # Remove padding
    y_data = y_data[:h, :w]
    
    y_new = Image.fromarray(y_data.astype(np.uint8), mode='L')
    return Image.merge("YCbCr", (y_new, cb, cr)).convert("RGB")

def extract_dct(image, secret_key):
    img = image.convert("YCbCr")
    y, _, _ = img.split()
    y_data = np.array(y, dtype=float)
    
    h, w = y_data.shape
    
    # Pad if necessary (though extraction should work on original size ideally)
    pad_h = (8 - h % 8) % 8
    pad_w = (8 - w % 8) % 8
    if pad_h > 0 or pad_w > 0:
        y_data = np.pad(y_data, ((0, pad_h), (0, pad_w)), mode='edge')
        
    padded_h, padded_w = y_data.shape
    
    # Shuffle logic must match embedding
    # FIX: Use original dimensions h/w to determine blocks
    blocks_h_usable = h // 8
    blocks_w_usable = w // 8
    num_blocks = blocks_h_usable * blocks_w_usable
    
    np.random.seed(get_deterministic_seed(secret_key))
    block_indices = np.arange(num_blocks)
    np.random.shuffle(block_indices)
    
    bits = ""
    u1, v1 = 4, 3
    u2, v2 = 3, 4
    
    # We don't know the length, so we iterate until null terminator or reasonable limit
    for i in range(num_blocks):
        idx = block_indices[i]
        r = (idx // blocks_w_usable) * 8
        c = (idx % blocks_w_usable) * 8
        
        block = y_data[r:r+8, c:c+8]
        dct_block = dct_2d(block - 128)
        
        val1 = dct_block[u1, v1]
        val2 = dct_block[u2, v2]
        
        if val1 > val2:
            bits += '1'
        else:
            bits += '0'
            
        # Check for null terminator every 8 bits
        if len(bits) % 8 == 0:
            if bits[-8:] == '00000000':
                bits = bits[:-8]
                break
    
    # Convert bits to string
    try:
        chars = []
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            chars.append(chr(int(byte, 2)))
        return "".join(chars)
    except Exception:
        return ""
