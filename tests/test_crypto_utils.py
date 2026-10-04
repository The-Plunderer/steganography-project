import pytest

from src.crypto_utils import encrypt_data, decrypt_data


def test_encrypt_and_decrypt():
    data = b"Hello Steganography"
    password = "TestPassword123"

    encrypted = encrypt_data(data, password)
    recovered = decrypt_data(encrypted, password)

    assert recovered == data


def test_encryption_produces_different_ciphertext():
    data = b"Secret message"
    password = "TestPassword123"

    encrypted_1 = encrypt_data(data, password)
    encrypted_2 = encrypt_data(data, password)

    assert encrypted_1 != encrypted_2


def test_wrong_password_fails():
    data = b"Secret message"
    password = "CorrectPassword"
    wrong_password = "WrongPassword"

    encrypted = encrypt_data(data, password)

    with pytest.raises(ValueError):
        decrypt_data(encrypted, wrong_password)


def test_modified_ciphertext_fails():
    data = b"Secret message"
    password = "TestPassword123"

    encrypted = bytearray(
        encrypt_data(data, password)
    )

    encrypted[-1] ^= 1

    with pytest.raises(ValueError):
        decrypt_data(bytes(encrypted), password)


def test_empty_password_fails():
    data = b"Secret message"

    with pytest.raises(ValueError):
        encrypt_data(data, "")


def test_large_data():
    data = bytes(range(256)) * 100
    password = "LargeDataPassword"

    encrypted = encrypt_data(data, password)
    recovered = decrypt_data(encrypted, password)

    assert recovered == data