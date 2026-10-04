from pathlib import Path

import pytest
from PIL import Image

from src.encrypted_steg import (
    serialize_image,
    deserialize_image,
    encrypt_image,
    decrypt_image,
)


def create_test_image(path):
    image = Image.new("RGB", (20, 20), "red")
    image.save(path)


def test_image_serialization(tmp_path):
    image_path = tmp_path / "secret.png"
    output_path = tmp_path / "recovered.png"

    create_test_image(image_path)

    data = serialize_image(image_path)

    assert len(data) == 20 * 20 * 3 + 13

    deserialize_image(data, output_path)

    recovered = Image.open(output_path)

    assert recovered.size == (20, 20)
    assert recovered.mode == "RGB"


def test_image_encryption_and_decryption(tmp_path):
    image_path = tmp_path / "secret.png"
    output_path = tmp_path / "recovered.png"

    create_test_image(image_path)

    password = "ProjectPassword123"

    encrypted = encrypt_image(
        image_path,
        password
    )

    decrypt_image(
        encrypted,
        password,
        output_path
    )

    original = Image.open(image_path)
    recovered = Image.open(output_path)

    assert recovered.size == original.size
    assert recovered.mode == original.mode
    assert recovered.tobytes() == original.tobytes()


def test_wrong_password_fails(tmp_path):
    image_path = tmp_path / "secret.png"
    output_path = tmp_path / "recovered.png"

    create_test_image(image_path)

    encrypted = encrypt_image(
        image_path,
        "CorrectPassword"
    )

    with pytest.raises(ValueError):
        decrypt_image(
            encrypted,
            "WrongPassword",
            output_path
        )


def test_modified_encrypted_image_fails(tmp_path):
    image_path = tmp_path / "secret.png"
    output_path = tmp_path / "recovered.png"

    create_test_image(image_path)

    encrypted = bytearray(
        encrypt_image(
            image_path,
            "ProjectPassword123"
        )
    )

    encrypted[-1] ^= 1

    with pytest.raises(ValueError):
        decrypt_image(
            bytes(encrypted),
            "ProjectPassword123",
            output_path
        )


def test_invalid_serialized_data(tmp_path):
    output_path = tmp_path / "recovered.png"

    with pytest.raises(ValueError):
        deserialize_image(
            b"invalid data",
            output_path
        )

def test_payload_embedding_and_extraction(tmp_path):
    cover_path = tmp_path / "cover.png"
    stego_path = tmp_path / "stego.png"

    create_test_image(cover_path)

    payload = b"Hello encrypted steganography"

    from src.encrypted_steg import (
        embed_payload,
        extract_payload
    )

    embed_payload(
        cover_path,
        payload,
        stego_path
    )

    recovered = extract_payload(
        stego_path
    )

    assert recovered == payload


def test_full_encrypted_steganography_pipeline(tmp_path):
    cover_path = tmp_path / "cover.png"
    secret_path = tmp_path / "secret.png"
    stego_path = tmp_path / "stego.png"
    recovered_path = tmp_path / "recovered.png"

    Image.new("RGB", (50, 50), "blue").save(cover_path)
    create_test_image(secret_path)

    password = "ProjectPassword123"

    from src.encrypted_steg import (
        encrypt_and_embed,
        extract_and_decrypt
    )

    encrypt_and_embed(
        cover_path,
        secret_path,
        password,
        stego_path
    )

    extract_and_decrypt(
        stego_path,
        password,
        recovered_path
    )

    original = Image.open(secret_path).convert("RGB")
    recovered = Image.open(recovered_path).convert("RGB")

    assert recovered.size == original.size
    assert recovered.tobytes() == original.tobytes()