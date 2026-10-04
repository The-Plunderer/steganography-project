from PIL import Image
import numpy as np


METADATA_PIXELS = 4


def generate_spiral_coordinates(height, width):
    """
    Generate pixel coordinates in clockwise spiral order.

    Example for a 3x3 image:

    (0,0) -> (0,1) -> (0,2)
                         |
    (1,0) <- (1,1) <- (1,2)
      |
    (2,0) -> (2,1) -> (2,2)
    """

    coordinates = []

    top = 0
    bottom = height - 1
    left = 0
    right = width - 1

    while top <= bottom and left <= right:

        # Left -> Right
        for x in range(left, right + 1):
            coordinates.append((top, x))

        top += 1

        # Top -> Bottom
        for y in range(top, bottom + 1):
            coordinates.append((y, right))

        right -= 1

        # Right -> Left
        if top <= bottom:
            for x in range(right, left - 1, -1):
                coordinates.append((bottom, x))

            bottom -= 1

        # Bottom -> Top
        if left <= right:
            for y in range(bottom, top - 1, -1):
                coordinates.append((y, left))

            left += 1

    return coordinates


def embed_byte_into_pixel(pixel, value):
    """
    Embed one 8-bit value into a pixel using LSB (3,3,2).

    Red   -> 3 bits
    Green -> 3 bits
    Blue  -> 2 bits
    """

    r_bits = (value >> 5) & 0b111
    g_bits = (value >> 2) & 0b111
    b_bits = value & 0b11

    pixel[0] = (pixel[0] & 0b11111000) | r_bits
    pixel[1] = (pixel[1] & 0b11111000) | g_bits
    pixel[2] = (pixel[2] & 0b11111100) | b_bits


def extract_byte_from_pixel(pixel):
    """
    Extract one 8-bit value from a pixel using LSB (3,3,2).
    """

    r = pixel[0] & 0b00000111
    g = pixel[1] & 0b00000111
    b = pixel[2] & 0b00000011

    return (
        (int(r) << 5)
        | (int(g) << 2)
        | int(b)
    )


def encode_image(cover_path, secret_path, output_path):
    """
    Hide a secret image inside a cover image using
    Spiral (3,3,2) traversal.
    """

    cover = np.array(
        Image.open(cover_path).convert("RGB"),
        dtype=np.uint8
    )

    secret = np.array(
        Image.open(secret_path).convert("RGB"),
        dtype=np.uint8
    )

    cover_height, cover_width = cover.shape[:2]
    secret_height, secret_width = secret.shape[:2]

    cover_pixels = cover_height * cover_width
    secret_pixels = secret_height * secret_width

    available_pixels = cover_pixels - METADATA_PIXELS

    if secret_pixels > available_pixels:
        raise ValueError(
            "Secret image is too large for the cover image."
        )

    stego = cover.copy()

    # ---------------------------------------------------------
    # Generate spiral traversal
    # ---------------------------------------------------------

    coordinates = generate_spiral_coordinates(
        cover_height,
        cover_width
    )

    # ---------------------------------------------------------
    # Store secret image dimensions
    # in the first 4 spiral pixels
    # ---------------------------------------------------------

    metadata = [
        (secret_width >> 8) & 0xFF,
        secret_width & 0xFF,
        (secret_height >> 8) & 0xFF,
        secret_height & 0xFF
    ]

    for i in range(METADATA_PIXELS):

        y, x = coordinates[i]

        embed_byte_into_pixel(
            stego[y, x],
            metadata[i]
        )

    # ---------------------------------------------------------
    # Flatten secret image
    # ---------------------------------------------------------

    secret_pixels_array = secret.reshape(-1, 3)

    # ---------------------------------------------------------
    # Embed secret pixels following spiral order
    # ---------------------------------------------------------

    for i, secret_pixel in enumerate(secret_pixels_array):

        y, x = coordinates[i + METADATA_PIXELS]

        r_bits = int(secret_pixel[0]) >> 5
        g_bits = int(secret_pixel[1]) >> 5
        b_bits = int(secret_pixel[2]) >> 6

        value = (
            (r_bits << 5)
            | (g_bits << 2)
            | b_bits
        )

        embed_byte_into_pixel(
            stego[y, x],
            value
        )

    Image.fromarray(stego).save(
        output_path,
        format="PNG"
    )

    print("Spiral (3,3,2) encoding successful!")
    print(f"Cover image  : {cover_path}")
    print(f"Secret image : {secret_path}")
    print(f"Stego image  : {output_path}")
    print(f"Secret size  : {secret_width} x {secret_height}")


def decode_image(stego_path, output_path):
    """
    Extract a secret image from a Spiral (3,3,2) stego image.
    """

    stego = np.array(
        Image.open(stego_path).convert("RGB"),
        dtype=np.uint8
    )

    stego_height, stego_width = stego.shape[:2]

    coordinates = generate_spiral_coordinates(
        stego_height,
        stego_width
    )

    # ---------------------------------------------------------
    # Read metadata
    # ---------------------------------------------------------

    metadata = []

    for i in range(METADATA_PIXELS):

        y, x = coordinates[i]

        value = extract_byte_from_pixel(
            stego[y, x]
        )

        metadata.append(value)

    secret_width = (
        (int(metadata[0]) << 8)
        | int(metadata[1])
    )

    secret_height = (
        (int(metadata[2]) << 8)
        | int(metadata[3])
    )

    # ---------------------------------------------------------
    # Validate dimensions
    # ---------------------------------------------------------

    if (
        secret_width == 0
        or secret_height == 0
        or secret_width > stego_width
        or secret_height > stego_height
    ):
        raise ValueError(
            "Invalid hidden image dimensions."
        )

    secret_pixels = secret_width * secret_height

    available_pixels = (
        stego_height * stego_width
        - METADATA_PIXELS
    )

    if secret_pixels > available_pixels:
        raise ValueError(
            "Hidden image dimensions exceed available capacity."
        )

    # ---------------------------------------------------------
    # Recover secret image
    # ---------------------------------------------------------

    secret = np.zeros(
        (secret_height, secret_width, 3),
        dtype=np.uint8
    )

    for i in range(secret_pixels):

        y, x = coordinates[i + METADATA_PIXELS]

        value = extract_byte_from_pixel(
            stego[y, x]
        )

        r = (value >> 5) & 0b111
        g = (value >> 2) & 0b111
        b = value & 0b11

        secret_y = i // secret_width
        secret_x = i % secret_width

        secret[secret_y, secret_x, 0] = r << 5
        secret[secret_y, secret_x, 1] = g << 5
        secret[secret_y, secret_x, 2] = b << 6

    Image.fromarray(secret).save(
        output_path,
        format="PNG"
    )

    print("Spiral (3,3,2) decoding successful!")
    print(f"Stego image : {stego_path}")
    print(f"Recovered   : {output_path}")
    print(f"Secret size : {secret_width} x {secret_height}")


if __name__ == "__main__":
    print("Spiral (3,3,2) Image Steganography")
