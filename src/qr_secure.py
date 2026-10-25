
"""Recipient-specific encrypted QR codes using RSA-OAEP and AES-GCM."""

import zxingcpp
import base64
import binascii
import json
import secrets
from pathlib import Path

import cv2
import numpy as np
import qrcode

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


FORMAT_NAME = "STEG-SECURE-QR"
FORMAT_VERSION = 1
KEY_ENCRYPTION = "RSA-OAEP-SHA256"
CONTENT_ENCRYPTION = "AES-256-GCM"
AAD = b"STEG-SECURE-QR:v1"


def generate_key_pair(private_key_path, public_key_path, passphrase):
    """Generate an RSA key pair and encrypt the private key file."""
    private_path = Path(private_key_path)
    public_path = Path(public_key_path)

    if private_path.resolve() == public_path.resolve():
        raise ValueError("Private and public keys need different file paths.")

    if not isinstance(passphrase, str) or len(passphrase) < 8:
        raise ValueError("Private-key passphrase must be at least 8 characters.")

    if private_path.exists() or public_path.exists():
        raise FileExistsError(
            "A key file already exists. Choose new paths to avoid overwriting keys."
        )

    private_path.parent.mkdir(parents=True, exist_ok=True)
    public_path.parent.mkdir(parents=True, exist_ok=True)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(
            passphrase.encode("utf-8")
        ),
    )

    public_bytes = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    private_path.write_bytes(private_bytes)
    public_path.write_bytes(public_bytes)

    return str(private_path), str(public_path)


def _load_public_key(public_key_path):
    """Load and validate an RSA public key."""
    key = serialization.load_pem_public_key(
        Path(public_key_path).read_bytes()
    )

    if not isinstance(key, rsa.RSAPublicKey):
        raise ValueError("The supplied public key is not an RSA key.")

    if key.key_size < 2048:
        raise ValueError("RSA keys must be at least 2048 bits.")

    return key


def _load_private_key(private_key_path, passphrase):
    """Load an RSA private key protected by its passphrase."""
    if not isinstance(passphrase, str) or not passphrase:
        raise ValueError("A private-key passphrase is required.")

    key = serialization.load_pem_private_key(
        Path(private_key_path).read_bytes(),
        password=passphrase.encode("utf-8"),
    )

    if not isinstance(key, rsa.RSAPrivateKey):
        raise ValueError("The supplied private key is not an RSA key.")

    if key.key_size < 2048:
        raise ValueError("RSA keys must be at least 2048 bits.")

    return key


def _encode_b64(data):
    """Encode bytes as ASCII Base64 text."""
    return base64.b64encode(data).decode("ascii")


def _decode_b64(value, field_name):
    """Decode a Base64 envelope field."""
    if not isinstance(value, str):
        raise ValueError(f"Invalid encrypted QR field: {field_name}.")

    try:
        return base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError) as error:
        raise ValueError(
            f"Invalid Base64 data in field: {field_name}."
        ) from error


def create_secure_qr(secret_text, public_key_path, output_qr_path):
    """Encrypt text for one recipient and save the encrypted QR image."""
    if not isinstance(secret_text, str) or not secret_text:
        raise ValueError("Secret text must not be empty.")

    public_key = _load_public_key(public_key_path)

    # A fresh AES-256 key is generated for every QR.
    session_key = AESGCM.generate_key(bit_length=256)
    nonce = secrets.token_bytes(12)

    ciphertext = AESGCM(session_key).encrypt(
        nonce,
        secret_text.encode("utf-8"),
        AAD,
    )

    # Only the intended recipient's public key can unwrap this session key.
    wrapped_key = public_key.encrypt(
        session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    envelope = {
        "format": FORMAT_NAME,
        "version": FORMAT_VERSION,
        "key_encryption": KEY_ENCRYPTION,
        "content_encryption": CONTENT_ENCRYPTION,
        "wrapped_key": _encode_b64(wrapped_key),
        "nonce": _encode_b64(nonce),
        "ciphertext": _encode_b64(ciphertext),
    }

    payload = json.dumps(
        envelope,
        separators=(",", ":"),
        sort_keys=True,
    )

    output_path = Path(output_qr_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    qr = qrcode.QRCode(
        version = None,
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size = 16,
        border = 6,
    )

    qr.add_data(payload)
    qr.make(fit = True)

    img = qr.make_image(fill_color = "black", back_color = "white")
    img.save(output_qr_path)

    return str(output_path)


def read_secure_qr_payload(image_path):
    """Read and validate the encrypted envelope from a QR image."""
    image_path = Path(image_path)

    if not image_path.is_file():
        raise FileNotFoundError(f"QR image not found: {image_path}")

    image_bytes = np.frombuffer(image_path.read_bytes(), dtype=np.uint8)
    image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Could not read the QR image.")

    results = zxingcpp.read_barcodes(image)

    if not results:
        raise ValueError("No readable QR code was found in the image.")

    decoded = results[0].text

    if not decoded:
        raise ValueError("No readable QR code was found in the image.")

    try:
        envelope = json.loads(decoded)
    except json.JSONDecodeError as error:
        raise ValueError("Invalid encrypted QR payload.") from error

    if not isinstance(envelope, dict):
        raise ValueError("Invalid encrypted QR payload.")

    if (
        envelope.get("format") != FORMAT_NAME
        or envelope.get("version") != FORMAT_VERSION
        or envelope.get("key_encryption") != KEY_ENCRYPTION
        or envelope.get("content_encryption") != CONTENT_ENCRYPTION
    ):
        raise ValueError("Unsupported or invalid encrypted QR format.")

    for field in ("wrapped_key", "nonce", "ciphertext"):
        if field not in envelope:
            raise ValueError(f"Encrypted QR is missing field: {field}.")

    # Validate encoding and basic cryptographic field lengths.
    wrapped_key = _decode_b64(envelope["wrapped_key"], "wrapped_key")
    nonce = _decode_b64(envelope["nonce"], "nonce")
    ciphertext = _decode_b64(envelope["ciphertext"], "ciphertext")

    if not wrapped_key or len(nonce) != 12 or len(ciphertext) < 16:
        raise ValueError("Invalid encrypted QR payload lengths.")

    return envelope


def decrypt_secure_qr(image_path, private_key_path, passphrase):
    """Decrypt a secure QR using the intended recipient's private key."""
    envelope = read_secure_qr_payload(image_path)
    private_key = _load_private_key(private_key_path, passphrase)

    wrapped_key = _decode_b64(envelope["wrapped_key"], "wrapped_key")
    nonce = _decode_b64(envelope["nonce"], "nonce")
    ciphertext = _decode_b64(envelope["ciphertext"], "ciphertext")

    try:
        session_key = private_key.decrypt(
            wrapped_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        if len(session_key) != 32:
            raise ValueError("Invalid AES session key.")

        plaintext = AESGCM(session_key).decrypt(
            nonce,
            ciphertext,
            AAD,
        )

        return plaintext.decode("utf-8")

    except (ValueError, InvalidTag) as error:
        raise ValueError(
            "Decryption failed: wrong private key or QR payload tampered with."
        ) from error
