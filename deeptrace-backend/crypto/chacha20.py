import base64
import hashlib
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes


def _derive_key(passphrase: str) -> bytes:
    # 256-bit key
    return hashlib.sha256(passphrase.encode()).digest()


def encrypt_chacha20(plaintext: str, passphrase: str) -> str:
    key = _derive_key(passphrase)
    nonce = get_random_bytes(12)  # 96-bit nonce

    cipher = ChaCha20.new(key=key, nonce=nonce)
    ciphertext = cipher.encrypt(plaintext.encode())

    return base64.b64encode(nonce + ciphertext).decode()


def decrypt_chacha20(ciphertext_b64: str, passphrase: str) -> str:
    key = _derive_key(passphrase)
    raw = base64.b64decode(ciphertext_b64)

    nonce = raw[:12]
    ciphertext = raw[12:]

    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)

    return plaintext.decode()