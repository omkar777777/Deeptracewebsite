def image_capacity(image):
    """
    Returns max number of BYTES that can be hidden using 1-bit LSB
    Works for RGB images only.
    """

    if image.mode != "RGB":
        raise ValueError("Image must be in RGB mode")

    width, height = image.size

    # 3 channels (R, G, B) × 1 bit per channel
    total_bits = width * height * 3

    # Convert bits → bytes
    return total_bits // 8