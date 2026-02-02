from .utils import text_to_bits, bits_to_text

SPACE = " "
TAB = "\t"
END_MARKER = "00000000"


def embed_whitespace(cover_text, secret):
    if not cover_text or not secret:
        raise ValueError("Cover text and secret must not be empty")

    bits = text_to_bits(secret) + END_MARKER

    # safer split
    words = cover_text.split()

    if len(words) < len(bits) + 1:
        raise ValueError("Cover text too short")

    stego = []
    for i, word in enumerate(words):
        stego.append(word)
        if i < len(bits):
            stego.append(TAB if bits[i] == "1" else SPACE)

    return "".join(stego)


def extract_whitespace(stego_text):
    bits = ""

    for ch in stego_text:
        if ch == SPACE:
            bits += "0"
        elif ch == TAB:
            bits += "1"

        if bits.endswith(END_MARKER):
            return bits_to_text(bits[:-8])

    raise ValueError("No hidden message found")