import numpy as np
from PIL import Image
from .utils import text_to_bits, bits_to_text
from .capacity import image_capacity

END_MARKER = "1111111111111110"  # 16-bit delimiter


def embed_lsb(image, secret):
    """
    Embed secret string inside image using 1-bit LSB via NumPy.
    Returns modified image.
    """

    if image.mode != "RGB":
        raise ValueError("Image must be RGB")

    secret_bits = text_to_bits(secret) + END_MARKER
    capacity = image_capacity(image)

    if len(secret_bits) > capacity * 8:
        raise ValueError("Secret message too large for this image")

    # Map the secret bits to an integer array
    bits_array = np.fromiter((int(b) for b in secret_bits), dtype=np.uint8)

    # Convert image to numpy array and flatten it
    img_array = np.array(image, dtype=np.uint8)
    flat_img = img_array.flatten()

    # Apply NumPy vectorized bitwise operation
    flat_img[:len(bits_array)] = (flat_img[:len(bits_array)] & ~np.uint8(1)) | bits_array

    # Reshape back to original shape and return Image
    img_array = flat_img.reshape(img_array.shape)

    return Image.fromarray(img_array, mode="RGB")


def extract_lsb(image):
    """
    Extract hidden message from image using NumPy arrays.
    """

    if image.mode != "RGB":
        raise ValueError("Image must be RGB")

    # Convert image to numpy flat array
    img_array = np.array(image, dtype=np.uint8)
    flat_img = img_array.flatten()

    # Extract all LSBs cleanly
    lsb_bits = flat_img & 1
    
    # Fast delimiter slicing
    bit_str = ''.join(lsb_bits.astype(str))
    
    if END_MARKER in bit_str:
        clean_bits = bit_str.split(END_MARKER)[0]
        return bits_to_text(clean_bits)

    return ""