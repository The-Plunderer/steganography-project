
import base64
import json

import pytest
import qrcode

from src.qr_secure import (
    create_secure_qr,
    decrypt_secure_qr,
    generate_key_pair,
    read_secure_qr_payload,
)


PASSPHRASE = "test-passphrase-2026"


@pytest.fixture
def recipient_keys(tmp_path):
    private_key = tmp_path / "recipient_private.pem"
    public_key = tmp_path / "recipient_public.pem"

    generate_key_pair(private_key, public_key, PASSPHRASE)

    return private_key, public_key


def test_secure_qr_round_trip(tmp_path, recipient_keys):
    private_key, public_key = recipient_keys
    secret = "Private contact: Alice, alice@example.com"

    qr_path = tmp_path / "secure_contact.png"

    create_secure_qr(secret, public_key, qr_path)

    recovered = decrypt_secure_qr(
        qr_path,
        private_key,
        PASSPHRASE,
    )

    assert recovered == secret


def test_plaintext_is_not_in_qr_payload(tmp_path, recipient_keys):
    _, public_key = recipient_keys
    secret = "alice@example.com and private phone 123456789"

    qr_path = tmp_path / "secure_contact.png"
    create_secure_qr(secret, public_key, qr_path)

    envelope = read_secure_qr_payload(qr_path)
    encoded_payload = json.dumps(envelope)

    assert secret not in encoded_payload
    assert "alice@example.com" not in encoded_payload
    assert "123456789" not in encoded_payload


def test_wrong_private_key_fails(tmp_path, recipient_keys):
    private_key, public_key = recipient_keys

    other_private = tmp_path / "other_private.pem"
    other_public = tmp_path / "other_public.pem"

    generate_key_pair(
        other_private,
        other_public,
        PASSPHRASE,
    )

    qr_path = tmp_path / "secure.png"
    create_secure_qr("Secret message", public_key, qr_path)

    with pytest.raises(ValueError, match="Decryption failed"):
        decrypt_secure_qr(
            qr_path,
            other_private,
            PASSPHRASE,
        )


def test_tampered_ciphertext_fails(tmp_path, recipient_keys):
    private_key, public_key = recipient_keys

    qr_path = tmp_path / "secure.png"
    create_secure_qr("Secret message", public_key, qr_path)

    envelope = read_secure_qr_payload(qr_path)
    ciphertext = bytearray(
        base64.b64decode(envelope["ciphertext"])
    )
    ciphertext[0] ^= 1
    envelope["ciphertext"] = base64.b64encode(
        ciphertext
    ).decode("ascii")

    tampered_path = tmp_path / "tampered.png"

    qr = qrcode.QRCode(
        version = None,
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size = 16,
        border = 6,
    )
    qr.add_data(json.dumps(envelope, separators = (",", ":")))
    qr.make(fit = True)
    qr.make_image(
        fill_color = "black",
        back_color = "white",
    ).save(tampered_path)

    with pytest.raises(ValueError, match="Decryption failed"):
        decrypt_secure_qr(
            tampered_path,
            private_key,
            PASSPHRASE,
        )


def test_private_key_requires_passphrase(tmp_path, recipient_keys):
    private_key, public_key = recipient_keys

    qr_path = tmp_path / "secure.png"
    create_secure_qr("Secret message", public_key, qr_path)

    with pytest.raises(ValueError):
        decrypt_secure_qr(
            qr_path,
            private_key,
            "wrong-passphrase",
        )


def test_existing_key_files_are_not_overwritten(
    tmp_path,
    recipient_keys,
):
    private_key, public_key = recipient_keys
    original_private = private_key.read_bytes()
    original_public = public_key.read_bytes()

    with pytest.raises(FileExistsError):
        generate_key_pair(
            private_key,
            public_key,
            PASSPHRASE,
        )

    assert private_key.read_bytes() == original_private
    assert public_key.read_bytes() == original_public


def test_missing_qr_file_fails(tmp_path, recipient_keys):
    private_key, _ = recipient_keys

    with pytest.raises(FileNotFoundError):
        decrypt_secure_qr(
            tmp_path / "missing.png",
            private_key,
            PASSPHRASE,
        )
