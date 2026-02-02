from .utils import text_to_bits, bits_to_text, set_lsb, get_lsb
from .capacity import image_capacity

END_MARKER = "1111111111111110"  # end delimiter


def embed_lsb(image, secret):
    secret_bits = text_to_bits(secret) + END_MARKER
    capacity = image_capacity(image)

    if len(secret_bits) // 8 > capacity:
        raise ValueError("Secret message too large for this image")

    pixels = image.load()
    bit_index = 0

    for y in range(image.height):
        for x in range(image.width):
            if bit_index >= len(secret_bits):
                return image

            r, g, b = pixels[x, y]
            r = set_lsb(r, secret_bits[bit_index]); bit_index += 1
            if bit_index < len(secret_bits):
                g = set_lsb(g, secret_bits[bit_index]); bit_index += 1
            if bit_index < len(secret_bits):
                b = set_lsb(b, secret_bits[bit_index]); bit_index += 1

            pixels[x, y] = (r, g, b)

    return image


def extract_lsb(image):
    pixels = image.load()
    bits = ""

    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            bits += str(get_lsb(r))
            bits += str(get_lsb(g))
            bits += str(get_lsb(b))

            if END_MARKER in bits:
                bits = bits.split(END_MARKER)[0]
                return bits_to_text(bits)

    return ""