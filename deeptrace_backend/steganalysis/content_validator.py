import string
import re

def is_valid_base64_or_hex(text):
    """Check if the string strongly represents a base64 encoded payload or HEX string."""
    text = text.strip()
    
    # Must be reasonably long to be considered a deliberate stego ciphertext
    if len(text) < 16:
        return False
        
    # Check Hex
    if all(c in string.hexdigits for c in text):
        return True
        
    # Check Base64 (Length multiple of 4, standard chars, optional padding)
    b64_pattern = r'^[A-Za-z0-9+/]+={0,2}$'
    if len(text) % 4 == 0 and re.match(b64_pattern, text):
        return True
        
    return False

def validate_content(byte_data):
    """
    Validates whether extracted byte data is meaningful.
    Categorizes it into "plaintext", "cipher text", or "nothing found".
    Returns (result_type, decoded_text)
    """

    if not byte_data:
        return "nothing found", None

    try:
        decoded = byte_data.decode("utf-8", errors="ignore")
    except:
        return "nothing found", None

    # Strip nulls and whitespace
    clean_text = decoded.strip('\x00').strip()

    if len(clean_text) < 5:
        return "nothing found", None

    # Count standard printable characters
    valid_chars = set(string.ascii_letters + string.digits + string.punctuation + " \t\n\r")
    printable_count = sum(1 for c in clean_text if c in valid_chars)
    printable_ratio = printable_count / max(len(clean_text), 1)

    # ---------------------------------------------------------
    # 1. Plaintext Check (Very Strict)
    # ---------------------------------------------------------
    # Must be 95%+ standard printable characters and not repeating garbage
    if printable_ratio > 0.95:
        # Reject if it's just repeating punctuation like $$$$$ or %%%%%
        punctuation_ratio = sum(1 for c in clean_text if c in string.punctuation) / max(len(clean_text), 1)
        if punctuation_ratio < 0.3:
            return "plaintext", clean_text

    # ---------------------------------------------------------
    # 2. Ciphertext Check 
    # ---------------------------------------------------------
    # Must be >90% printable, but tightly match known cipher structures
    if printable_ratio > 0.90:
        # Try to find a continuous block of base64 or hex
        words = clean_text.split()
        for word in words:
            if is_valid_base64_or_hex(word):
                return "cipher text", clean_text

    return "nothing found", None