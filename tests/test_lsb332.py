import os
import sys

import numpy as np
from PIL import Image

# Allow Python to find modules inside src/
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "src")
    )
)

from lsb332 import encode_image, decode_image


TEST_DIR = "tests/test_data"
COVER_IMAGE = os.path.join(TEST_DIR, "cover.png")
SECRET_IMAGE = os.path.join(TEST_DIR, "secret.png")
STEGO_IMAGE = os.path.join(TEST_DIR, "stego_lsb332.png")
RECOVERED_IMAGE = os.path.join(TEST_DIR, "recovered_lsb332.png")


def create_test_images():
    """
    Create small deterministic cover and secret images.
    """

    os.makedirs(TEST_DIR, exist_ok=True)

    # Cover: 100 x 100 RGB image
    cover = np.zeros(
        (100, 100, 3),
        dtype=np.uint8
    )

    for y in range(100):
        for x in range(100):
            cover[y, x] = [
                (x * 2) % 256,
                (y * 2) % 256,
                (x + y) % 256
            ]

    Image.fromarray(cover).save(COVER_IMAGE)

    # Secret: 20 x 20 RGB image
    secret = np.zeros(
        (20, 20, 3),
        dtype=np.uint8
    )

    for y in range(20):
        for x in range(20):
            secret[y, x] = [
                255 if x >= 10 else 0,
                255 if y >= 10 else 0,
                255 if (x + y) % 2 == 0 else 0
            ]

    Image.fromarray(secret).save(SECRET_IMAGE)


def test_lsb332_encode_decode():
    create_test_images()

    encode_image(
        COVER_IMAGE,
        SECRET_IMAGE,
        STEGO_IMAGE
    )

    decode_image(
        STEGO_IMAGE,
        RECOVERED_IMAGE
    )

    original = np.array(
        Image.open(SECRET_IMAGE).convert("RGB")
    )

    recovered = np.array(
        Image.open(RECOVERED_IMAGE).convert("RGB")
    )

    assert original.shape == recovered.shape
    assert original.shape == (20, 20, 3)


def test_lsb332_dimensions():
    create_test_images()

    encode_image(
        COVER_IMAGE,
        SECRET_IMAGE,
        STEGO_IMAGE
    )

    decode_image(
        STEGO_IMAGE,
        RECOVERED_IMAGE
    )

    original_size = Image.open(
        SECRET_IMAGE
    ).size

    recovered_size = Image.open(
        RECOVERED_IMAGE
    ).size

    assert recovered_size == original_size


def test_lsb332_oversized_secret():
    create_test_images()

    oversized_secret = os.path.join(
        TEST_DIR,
        "oversized.png"
    )

    image = Image.new(
        "RGB",
        (101, 101),
        "red"
    )

    image.save(oversized_secret)

    try:
        encode_image(
            COVER_IMAGE,
            oversized_secret,
            STEGO_IMAGE
        )

        assert False, (
            "Expected oversized secret to raise ValueError"
        )

    except ValueError as error:
        assert "too large" in str(error).lower()


def test_lsb332_module_output_exists():
    create_test_images()

    encode_image(
        COVER_IMAGE,
        SECRET_IMAGE,
        STEGO_IMAGE
    )

    assert os.path.exists(STEGO_IMAGE)
    assert os.path.getsize(STEGO_IMAGE) > 0
