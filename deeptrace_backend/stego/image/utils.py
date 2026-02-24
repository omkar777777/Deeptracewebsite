def text_to_bits(text):
    """
    Convert string to bit string (UTF-8 safe)
    """
    return ''.join(format(byte, '08b') for byte in text.encode("utf-8"))


def bits_to_text(bits):
    """
    Convert bit string back to text
    """
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    byte_array = bytearray(int(c, 2) for c in chars if len(c) == 8)

    return byte_array.decode("utf-8", errors="ignore")


def set_lsb(value, bit):
    """
    Set least significant bit of a channel
    """
    return (value & ~1) | int(bit)


def get_lsb(value):
    """
    Get least significant bit
    """
    return value & 1