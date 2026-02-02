import base64
import hashlib
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def _derive_3des_key(passphrase: str) -> bytes:
    """
    Derive a valid 24-byte 3DES key from passphrase using SHA-256
    """
    key = hashlib.sha256(passphrase.encode()).digest()[:24]
    return DES3.adjust_key_parity(key)


def encrypt_3des(plaintext: str, passphrase: str) -> str:
    key = _derive_3des_key(passphrase)
    iv = get_random_bytes(8)  # DES block size = 8 bytes

    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), DES3.block_size))

    encrypted = iv + ciphertext
    return base64.b64encode(encrypted).decode()


def decrypt_3des(ciphertext_b64: str, passphrase: str) -> str:
    key = _derive_3des_key(passphrase)
    encrypted = base64.b64decode(ciphertext_b64)

    iv = encrypted[:8]
    ciphertext = encrypted[8:]

    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), DES3.block_size)

    return plaintext.decode()