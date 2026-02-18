import string


def validate_content(byte_data):
    """
    Validates whether extracted byte data is meaningful.
    Returns (is_valid, decoded_text)
    """

    if not byte_data:
        return False, None

    try:
        decoded = byte_data.decode("utf-8", errors="ignore")
    except:
        return False, None

    if len(decoded) < 5:
        return False, None

    printable_ratio = sum(
        c in string.printable for c in decoded
    ) / max(len(decoded), 1)

    if printable_ratio < 0.7:
        return False, None

    return True, decoded.strip()