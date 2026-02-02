from .utils import text_to_bits, bits_to_text

ZW_SPACE = "\u200B"
ZW_NONJOIN = "\u200C"
END_MARKER = "1111111111111110"


def embed_zerowidth(cover_text, secret):
    if not cover_text or not secret:
        raise ValueError("Cover text and secret must not be empty")

    bits = text_to_bits(secret) + END_MARKER
    zw_sequence = [ZW_SPACE if b == "0" else ZW_NONJOIN for b in bits]
    return cover_text + "".join(zw_sequence)


def extract_zerowidth(stego_text):
    bits = ""

    for ch in stego_text:
        if ch == ZW_SPACE:
            bits += "0"
        elif ch == ZW_NONJOIN:
            bits += "1"

        if bits.endswith(END_MARKER):
            return bits_to_text(bits[:-len(END_MARKER)])

    raise ValueError("No hidden message found")