import string
import base64
import re


def validate_content(byte_data):
    """
    Classifies extracted LSB payload.

    Returns:
        ("plaintext", decoded_text)
        ("ciphertext", decoded_text)
        ("none", None)

    Logic:
    - Plaintext → highly printable readable text
    - Ciphertext → structured alphanumeric (base64/hex/encrypted)
    - None → random noise
    """

    if not byte_data or len(byte_data) < 8:
        return "none", None

    # ---------------------------------------
    # Attempt UTF-8 decoding
    # ---------------------------------------
    try:
        decoded = byte_data.decode("utf-8")
    except UnicodeDecodeError:
        return "none", None

    decoded = decoded.strip()

    if len(decoded) < 4:
        return "none", None

    # ---------------------------------------
    # Printable ratio check
    # ---------------------------------------
    printable_count = sum(c in string.printable for c in decoded)
    printable_ratio = printable_count / len(decoded)

    # ---------------------------------------
    # 1️⃣ Plaintext detection
    # ---------------------------------------
    if printable_ratio > 0.92:
        # Contains readable words/spaces
        if any(char.isalpha() for char in decoded):
            return "plaintext", decoded

    # ---------------------------------------
    # 2️⃣ Ciphertext detection
    # ---------------------------------------

    # Base64 pattern
    base64_pattern = re.fullmatch(r"[A-Za-z0-9+/=\n\r]+", decoded)

    # Hex pattern
    hex_pattern = re.fullmatch(r"[0-9a-fA-F]+", decoded)

    if printable_ratio > 0.60:
        if base64_pattern or hex_pattern:
            return "ciphertext", decoded

        # High printable but not readable words
        if printable_ratio > 0.75:
            return "ciphertext", decoded

    # ---------------------------------------
    # Otherwise: likely random noise
    # ---------------------------------------
    return "none", None