import pytest

from src.qr_contact import (
    create_vcard,
    decode_contact_qr,
    export_vcard,
    generate_contact_qr,
)


def sample_vcard():
    return create_vcard(
        full_name="Rahul Sharma",
        phone="+919876543210",
        email="rahul@example.com",
        organization="Example Technologies",
        title="Software Engineer",
        consent=True,
    )


def test_consent_is_required():
    with pytest.raises(PermissionError):
        create_vcard(
            full_name="Rahul Sharma",
            phone="+919876543210",
            consent=False,
        )


def test_name_is_required():
    with pytest.raises(ValueError):
        create_vcard(full_name=" ", consent=True)


def test_vcard_contains_only_supplied_details():
    vcard = create_vcard(
        full_name="Rahul Sharma",
        email="rahul@example.com",
        consent=True,
    )

    assert "FN:Rahul Sharma" in vcard
    assert "EMAIL:rahul@example.com" in vcard
    assert "TEL;TYPE=CELL:" not in vcard
    assert "BEGIN:VCARD" in vcard
    assert "END:VCARD" in vcard


def test_qr_generation_and_decoding_round_trip(tmp_path):
    vcard = sample_vcard()
    qr_path = tmp_path / "contact.png"

    generate_contact_qr(vcard, qr_path)
    decoded = decode_contact_qr(qr_path)

    assert decoded == vcard


def test_export_vcard(tmp_path):
    vcard = sample_vcard()
    output_path = tmp_path / "contact.vcf"

    export_vcard(vcard, output_path)

    assert output_path.exists()
    assert output_path.read_bytes() == vcard.encode("utf-8")


def test_export_requires_vcf_extension(tmp_path):
    with pytest.raises(ValueError):
        export_vcard(sample_vcard(), tmp_path / "contact.txt")


def test_invalid_vcard_is_rejected():
    with pytest.raises(ValueError):
        generate_contact_qr("This is not a vCard", "invalid.png")


def test_missing_qr_image_is_rejected(tmp_path):
    with pytest.raises(FileNotFoundError):
        decode_contact_qr(tmp_path / "missing.png")
