import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32
PBKDF2_ITERATIONS = 600_000


def derive_key(password, salt):
    """
    Derive a 256-bit AES key from a password using PBKDF2-HMAC-SHA256.
    """

    if not password:
        raise ValueError("Password cannot be empty.")

    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if len(salt) != SALT_SIZE:
        raise ValueError("Invalid salt size.")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )

    return kdf.derive(password.encode("utf-8"))


def encrypt_data(data, password):
    """
    Encrypt bytes using AES-256-GCM.

    Returns:
        salt + nonce + ciphertext
    """

    if not isinstance(data, bytes):
        raise TypeError("Data must be bytes.")

    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)

    key = derive_key(password, salt)

    aes = AESGCM(key)
    ciphertext = aes.encrypt(nonce, data, None)

    return salt + nonce + ciphertext


def decrypt_data(encrypted_data, password):
    """
    Decrypt data produced by encrypt_data().
    """

    if not isinstance(encrypted_data, bytes):
        raise TypeError("Encrypted data must be bytes.")

    minimum_size = SALT_SIZE + NONCE_SIZE + 16

    if len(encrypted_data) < minimum_size:
        raise ValueError("Encrypted data is too short.")

    salt = encrypted_data[:SALT_SIZE]

    nonce_start = SALT_SIZE
    nonce_end = nonce_start + NONCE_SIZE

    nonce = encrypted_data[nonce_start:nonce_end]
    ciphertext = encrypted_data[nonce_end:]

    key = derive_key(password, salt)

    aes = AESGCM(key)

    try:
        return aes.decrypt(nonce, ciphertext, None)

    except Exception as error:
        raise ValueError(
            "Decryption failed. Incorrect password or corrupted data."
        ) from error