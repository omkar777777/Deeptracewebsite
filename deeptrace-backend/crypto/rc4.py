import base64
import hashlib
from Crypto.Cipher import ARC4

def _derive_key(passphrase: str) -> bytes:
    # RC4 keys can be variable length
    return hashlib.sha256(passphrase.encode()).digest()

def encrypt_rc4(plaintext: str, passphrase: str) -> str:
    key = _derive_key(passphrase)
    cipher = ARC4.new(key)
    ciphertext = cipher.encrypt(plaintext.encode())
    return base64.b64encode(ciphertext).decode()

def decrypt_rc4(ciphertext_b64: str, passphrase: str) -> str:
    key = _derive_key(passphrase)
    cipher = ARC4.new(key)
    ciphertext = base64.b64decode(ciphertext_b64)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode()