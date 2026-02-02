import base64
import hashlib
from Crypto.Cipher import Blowfish
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def _derive_key(passphrase: str) -> bytes:
    # Blowfish supports variable key size (32–448 bits)
    # We take first 16 bytes (128-bit) from SHA-256
    return hashlib.sha256(passphrase.encode()).digest()[:16]


def encrypt_blowfish(plaintext: str, passphrase: str) -> str:
    key = _derive_key(passphrase)
    iv = get_random_bytes(8)  # Blowfish block size = 8 bytes

    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), Blowfish.block_size))

    return base64.b64encode(iv + ciphertext).decode()


def decrypt_blowfish(ciphertext_b64: str, passphrase: str) -> str:
    key = _derive_key(passphrase)
    data = base64.b64decode(ciphertext_b64)

    iv = data[:8]
    ciphertext = data[8:]

    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), Blowfish.block_size)

    return plaintext.decode()