import numpy as np


def bits_to_bytes(bits, max_bytes):
    """Helper to convert a 1D numpy array of bits into bytes."""
    
    # 🌟 NEW: Check for DeepTrace's native END_MARKER to prevent trailing noise from destroying accuracy
    END_MARKER = "1111111111111110"
    bit_str = ''.join(bits[:max_bytes * 8].astype(str))
    
    payloads = []
    
    # Payload 1: Truncated at END_MARKER (if present)
    if END_MARKER in bit_str:
        clean_bits = bit_str.split(END_MARKER)[0]
        byte_array = []
        for i in range(0, len(clean_bits), 8):
            chunk = clean_bits[i:i+8]
            if len(chunk) == 8:
                byte_array.append(int(chunk, 2))
        payloads.append({"data": bytes(byte_array), "delimiter": True})

    # Payload 2: Raw (Standard max_bytes extraction)
    # Reconstruct from bit_str to keep it efficient instead of looping over bits again
    raw_array = []
    for i in range(0, len(bit_str), 8):
        chunk = bit_str[i:i+8]
        if len(chunk) == 8:
            raw_array.append(int(chunk, 2))
    payloads.append({"data": bytes(raw_array), "delimiter": False})
    
    return payloads

def extract_lsb_payload(image, max_bytes=5000):
    """
    Extract raw LSB bitstream from image using multiple common strategies.
    Returns a list of raw byte payloads.
    """
    payloads = []

    # 1. Standard Flatten (Row-major, RGB/BGR interleaved)
    flat = image.flatten()
    bits_std = flat & 1
    payloads.extend(bits_to_bytes(bits_std, max_bytes))

    # 2. Column-Major Flatten
    img_t = np.transpose(image, (1, 0, 2))
    flat_t = img_t.flatten()
    bits_col = flat_t & 1
    payloads.extend(bits_to_bytes(bits_col, max_bytes))

    # 3. Channel-Specific (R, G, B individually)
    for c in range(image.shape[2]):
        channel_flat = image[:, :, c].flatten()
        bits_channel = channel_flat & 1
        payloads.extend(bits_to_bytes(bits_channel, max_bytes))

    # 4. Standard Flatten, Reversed Bits
    bits_rev = bits_std[::-1]
    payloads.extend(bits_to_bytes(bits_rev, max_bytes))

    return payloads