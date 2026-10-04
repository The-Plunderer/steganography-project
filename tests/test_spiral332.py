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

from spiral332 import (
    encode_image,
    decode_image,
    generate_spiral_coordinates,
)


TEST_DIR = "tests/test_data"
COVER_IMAGE = os.path.join(TEST_DIR, "cover_spiral.png")
SECRET_IMAGE = os.path.join(TEST_DIR, "secret_spiral.png")
STEGO_IMAGE = os.path.join(TEST_DIR, "stego_spiral332.png")
RECOVERED_IMAGE = os.path.join(
    TEST_DIR,
    "recovered_spiral332.png"
)


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


def test_spiral_coordinates():
    coordinates = generate_spiral_coordinates(3, 3)

    expected = [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 2),
        (2, 1),
        (2, 0),
        (1, 0),
        (1, 1),
    ]

    assert coordinates == expected


def test_spiral_coordinates_cover_every_pixel():
    height = 10
    width = 15

    coordinates = generate_spiral_coordinates(
        height,
        width
    )

    assert len(coordinates) == height * width
    assert len(set(coordinates)) == height * width

    for y, x in coordinates:
        assert 0 <= y < height
        assert 0 <= x < width


def test_spiral332_encode_decode():
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


def test_spiral332_dimensions():
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


def test_spiral332_oversized_secret():
    create_test_images()

    oversized_secret = os.path.join(
        TEST_DIR,
        "oversized_spiral.png"
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


def test_spiral332_module_output_exists():
    create_test_images()

    encode_image(
        COVER_IMAGE,
        SECRET_IMAGE,
        STEGO_IMAGE
    )

    assert os.path.exists(STEGO_IMAGE)
    assert os.path.getsize(STEGO_IMAGE) > 0
