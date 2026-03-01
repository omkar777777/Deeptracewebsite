import numpy as np


def extract_lsb_payload(image, max_bytes=5000):
    """
    Extract raw LSB bitstream from image.
    Returns raw byte payload.
    """

    flat = image.flatten()

    # Extract LSB bits
    bits = flat & 1

    byte_array = []

    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i + 8]
        if len(byte_bits) < 8:
            break

        byte = 0
        for bit in byte_bits:
            byte = (byte << 1) | bit

        byte_array.append(byte)

        if len(byte_array) >= max_bytes:
            break

    return bytes(byte_array)