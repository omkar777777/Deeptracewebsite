def text_to_bits(text):
    """
    Convert UTF-8 text to binary string
    Each character is encoded as 8-bit UTF-8 bytes
    """
    if not isinstance(text, str):
        raise ValueError("Input text must be a string")

    return "".join(f"{byte:08b}" for byte in text.encode("utf-8"))


def bits_to_text(bits):
    """
    Convert binary string back to UTF-8 text
    Enforces byte alignment and strict UTF-8 decoding
    """
    if not bits:
        raise ValueError("No bits provided for decoding")

    if len(bits) % 8 != 0:
        raise ValueError("Bit stream length is not byte-aligned")

    chars = [bits[i:i + 8] for i in range(0, len(bits), 8)]
    byte_array = bytearray(int(c, 2) for c in chars)

    try:
        return byte_array.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError("Decoded data is not valid UTF-8") from e