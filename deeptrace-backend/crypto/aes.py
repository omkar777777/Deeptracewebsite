import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def _derive_key(passphrase: str) -> bytes:
    """
    Derive a 256-bit AES key from a passphrase using SHA-256
    """
    return hashlib.sha256(passphrase.encode()).digest()


def encrypt_aes(plaintext: str, passphrase: str) -> str:
    key = _derive_key(passphrase)
    iv = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))

    # prepend IV and encode
    encrypted = iv + ciphertext
    return base64.b64encode(encrypted).decode()


def decrypt_aes(ciphertext_b64: str, passphrase: str) -> str:
    key = _derive_key(passphrase)
    encrypted = base64.b64decode(ciphertext_b64)

    iv = encrypted[:16]
    ciphertext = encrypted[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return plaintext.decode()