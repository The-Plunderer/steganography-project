"""Consent-based contact QR generation, decoding, and vCard export."""

from pathlib import Path

import cv2
import numpy as np
import qrcode


def _escape_vcard(value):
    """Escape special characters in a vCard text value."""
    value = str(value)
    return (
        value.replace("\\", "\\\\")
        .replace("\n", "\\n")
        .replace(";", "\\;")
        .replace(",", "\\,")
    )


def create_vcard(
    full_name,
    phone="",
    email="",
    organization="",
    title="",
    address="",
    consent=False,
):
    """Create a vCard from contact details approved for sharing."""
    if consent is not True:
        raise PermissionError(
            "Explicit consent is required before sharing contact details."
        )

    full_name = str(full_name).strip()
    if not full_name:
        raise ValueError("Full name is required.")

    fields = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{_escape_vcard(full_name)}",
    ]

    optional_fields = [
        ("TEL;TYPE=CELL", phone),
        ("EMAIL", email),
        ("ORG", organization),
        ("TITLE", title),
        ("ADR;TYPE=HOME", address),
    ]

    for label, value in optional_fields:
        value = str(value).strip()
        if value:
            fields.append(f"{label}:{_escape_vcard(value)}")

    fields.append("END:VCARD")
    return "\r\n".join(fields) + "\r\n"


def _validate_vcard(vcard):
    """Reject data that is not recognizably a vCard."""
    if not isinstance(vcard, str):
        raise ValueError("Contact data must be text.")

    lines = vcard.replace("\r\n", "\n").splitlines()
    if (
        not lines
        or lines[0].strip().upper() != "BEGIN:VCARD"
        or lines[-1].strip().upper() != "END:VCARD"
        or not any(line.upper().startswith("VERSION:") for line in lines)
        or not any(line.upper().startswith("FN:") for line in lines)
    ):
        raise ValueError("Invalid vCard data.")

    return vcard


def generate_contact_qr(vcard, output_path):
    """Generate a QR image containing a validated vCard."""
    vcard = _validate_vcard(vcard)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(vcard)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")
    image.save(output_path)

    return str(output_path)


def decode_contact_qr(image_path):
    """Decode a QR image and return its vCard text."""
    image_path = Path(image_path)
    if not image_path.is_file():
        raise FileNotFoundError(f"QR image not found: {image_path}")

    with open(image_path, "rb") as image_file:
        image_bytes = np.frombuffer(image_file.read(), dtype=np.uint8)

    image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Could not read the QR image.")

    detector = cv2.QRCodeDetector()
    decoded, points, _ = detector.detectAndDecode(image)

    if not decoded:
        raise ValueError("No readable QR code was found in the image.")

    return _validate_vcard(decoded)


def export_vcard(vcard, output_path):
    """Export validated contact data to a .vcf file."""
    vcard = _validate_vcard(vcard)
    output_path = Path(output_path)

    if output_path.suffix.lower() != ".vcf":
        raise ValueError("Contact export path must end in .vcf.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(vcard, encoding="utf-8", newline="")
    return str(output_path)
