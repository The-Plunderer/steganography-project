import os
import sys

from PIL import Image

# Allow Python to find the modules inside src/
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    )
)

from encoder import encode_message
from decoder import decode_message


TEST_COVER = "images/cover.png"
TEST_OUTPUT = "output/test_stego.png"


def test_encode_and_decode():
    message = "Automated steganography test!"

    encode_message(
        TEST_COVER,
        TEST_OUTPUT,
        message
    )

    decoded_message = decode_message(TEST_OUTPUT)

    assert decoded_message == message


def test_unicode_message():
    message = "Hello! नमस्ते 🌍"

    encode_message(
        TEST_COVER,
        TEST_OUTPUT,
        message
    )

    decoded_message = decode_message(TEST_OUTPUT)

    assert decoded_message == message


def test_missing_image():
    try:
        decode_message("output/nonexistent.png")
        assert False
    except ValueError as error:
        assert "Stego image not found" in str(error)


def test_oversized_message():
    image = Image.open(TEST_COVER).convert("RGB")

    capacity_bytes = (
        (image.width * image.height * 3) // 8
    )

    oversized_message = "A" * capacity_bytes

    try:
        encode_message(
            TEST_COVER,
            TEST_OUTPUT,
            oversized_message
        )
        assert False
    except ValueError as error:
        assert "Message is too large" in str(error)