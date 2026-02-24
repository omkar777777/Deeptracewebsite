import numpy as np


END_MARKER = "1111111111111110"


def _extract_bits(flat):
    """
    Extract full LSB bitstream from flattened image array.
    """
    bits = (flat & 1).astype(str)
    return "".join(bits)


def _bits_to_bytes(bit_string):
    """
    Convert bit string to bytes.
    """
    byte_array = []

    for i in range(0, len(bit_string), 8):
        byte_bits = bit_string[i:i + 8]
        if len(byte_bits) < 8:
            break
        byte_array.append(int(byte_bits, 2))

    return bytes(byte_array)


def extract_lsb_variants(image):
    """
    Extract LSB using delimiter-aware logic.
    Tries multiple channel variants.
    """

    if image is None or image.size == 0:
        return []

    variants = []

    # Variant 1: All channels sequential
    flat_all = image.flatten().astype(np.uint8)
    variants.append(flat_all)

    # Variant 2: Blue only
    variants.append(image[:, :, 0].flatten().astype(np.uint8))

    # Variant 3: Green only
    variants.append(image[:, :, 1].flatten().astype(np.uint8))

    # Variant 4: Red only
    variants.append(image[:, :, 2].flatten().astype(np.uint8))

    extracted_candidates = []

    for flat in variants:

        bit_string = _extract_bits(flat)

        if END_MARKER in bit_string:
            bit_string = bit_string.split(END_MARKER)[0]

        extracted_candidates.append(_bits_to_bytes(bit_string))

    return extracted_candidates