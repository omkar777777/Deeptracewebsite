def image_capacity(image):
    """
    Returns max number of bytes that can be hidden using LSB
    """
    width, height = image.size
    total_bits = width * height * 3
    return total_bits // 8