from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64

from .lsb import embed_lsb, extract_lsb


def encrypt_message(message, password):
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32)

    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())

    payload = base64.b64encode(
        salt + cipher.nonce + tag + ciphertext
    ).decode()

    return payload


def decrypt_message(payload, password):
    data = base64.b64decode(payload)

    salt = data[:16]
    nonce = data[16:32]
    tag = data[32:48]
    ciphertext = data[48:]

    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    return cipher.decrypt_and_verify(ciphertext, tag).decode()


def embed_lsb_keyed(image, secret, password):
    encrypted = encrypt_message(secret, password)
    return embed_lsb(image, encrypted)


def extract_lsb_keyed(image, password):
    encrypted = extract_lsb(image)
    return decrypt_message(encrypted, password)