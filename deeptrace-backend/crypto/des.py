import base64
import hashlib
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def _derive_des_key(passphrase: str) -> bytes:
    """
    Derive an 8-byte DES key from passphrase using MD5 (DES requires 8 bytes)
    """
    return hashlib.md5(passphrase.encode()).digest()[:8]


def encrypt_des(plaintext: str, passphrase: str) -> str:
    key = _derive_des_key(passphrase)
    iv = get_random_bytes(8)

    cipher = DES.new(key, DES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), DES.block_size))

    encrypted = iv + ciphertext
    return base64.b64encode(encrypted).decode()


def decrypt_des(ciphertext_b64: str, passphrase: str) -> str:
    key = _derive_des_key(passphrase)
    encrypted = base64.b64decode(ciphertext_b64)

    iv = encrypted[:8]
    ciphertext = encrypted[8:]

    cipher = DES.new(key, DES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), DES.block_size)

    return plaintext.decode()