from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
import base64

from .lsb import embed_lsb, extract_lsb


# ======================================================
# CONFIGURATION
# ======================================================

PBKDF2_ITERATIONS = 100000
SALT_SIZE = 16
NONCE_SIZE = 16
TAG_SIZE = 16


# ======================================================
# ENCRYPTION
# ======================================================

def encrypt_message(message: str, password: str) -> str:
    """
    Encrypt message using AES-256 (EAX mode).
    Returns base64-encoded payload.
    """

    if not message:
        raise ValueError("Message cannot be empty")

    if not password:
        raise ValueError("Password is required")

    salt = get_random_bytes(SALT_SIZE)

    key = PBKDF2(
        password,
        salt,
        dkLen=32,
        count=PBKDF2_ITERATIONS,
        hmac_hash_module=SHA256
    )

    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode("utf-8"))

    payload = salt + cipher.nonce + tag + ciphertext

    return base64.b64encode(payload).decode("utf-8")


# ======================================================
# DECRYPTION
# ======================================================

def decrypt_message(payload: str, password: str) -> str:
    """
    Decrypt AES payload (base64 string).
    """

    if not payload:
        raise ValueError("No encrypted payload found")

    if not password:
        raise ValueError("Password is required")

    try:
        data = base64.b64decode(payload)

        # Basic structural validation
        if len(data) < (SALT_SIZE + NONCE_SIZE + TAG_SIZE):
            raise ValueError("Corrupted encrypted payload")

        salt = data[:SALT_SIZE]
        nonce = data[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
        tag = data[SALT_SIZE + NONCE_SIZE:SALT_SIZE + NONCE_SIZE + TAG_SIZE]
        ciphertext = data[SALT_SIZE + NONCE_SIZE + TAG_SIZE:]

        key = PBKDF2(
            password,
            salt,
            dkLen=32,
            count=PBKDF2_ITERATIONS,
            hmac_hash_module=SHA256
        )

        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

        decrypted = cipher.decrypt_and_verify(ciphertext, tag)

        return decrypted.decode("utf-8")

    except Exception:
        raise ValueError("Invalid password or corrupted stego image")


# ======================================================
# LSB + AES WRAPPERS
# ======================================================

def embed_lsb_keyed(image, secret: str, password: str):
    """
    Encrypt secret first, then embed using LSB.
    """
    encrypted_payload = encrypt_message(secret, password)
    return embed_lsb(image, encrypted_payload)


def extract_lsb_keyed(image, password: str) -> str:
    """
    Extract encrypted payload from image,
    then decrypt using provided password.
    """

    encrypted_payload = extract_lsb(image)

    if not encrypted_payload:
        raise ValueError("No hidden message found")

    return decrypt_message(encrypted_payload, password)