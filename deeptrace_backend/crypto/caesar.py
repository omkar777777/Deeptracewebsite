"""
Caesar Cipher Algorithm
-----------------------
Supports encryption and decryption with a fixed shift.
Preserves case and non-alphabet characters.
"""

def encrypt_caesar(plaintext: str, shift: int) -> str:
    result = []

    for char in plaintext:
        if char.isupper():
            result.append(
                chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            )
        elif char.islower():
            result.append(
                chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            )
        else:
            result.append(char)

    return "".join(result)


def decrypt_caesar(ciphertext: str, shift: int) -> str:
    return encrypt_caesar(ciphertext, -shift)