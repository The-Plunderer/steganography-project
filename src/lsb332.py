from PIL import Image
import numpy as np


METADATA_PIXELS = 4


def encode_image(cover_path, secret_path, output_path):
    """
    Hide a secret image inside a cover image using LSB (3,3,2).

    Red   -> 3 LSBs
    Green -> 3 LSBs
    Blue  -> 2 LSBs

    One cover pixel stores one 8-bit representation
    of one secret pixel.
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
    # Store secret image dimensions in the first 4 cover pixels
    # ---------------------------------------------------------

    metadata = np.array(
        [
            (secret_width >> 8) & 0xFF,
            secret_width & 0xFF,
            (secret_height >> 8) & 0xFF,
            secret_height & 0xFF,
        ],
        dtype=np.uint8
    )

    for i in range(METADATA_PIXELS):
        value = metadata[i]

        r_bits = (value >> 5) & 0b111
        g_bits = (value >> 2) & 0b111
        b_bits = value & 0b11

        pixel_y = i // cover_width
        pixel_x = i % cover_width

        stego[pixel_y, pixel_x, 0] = (
            stego[pixel_y, pixel_x, 0] & 0b11111000
        ) | r_bits

        stego[pixel_y, pixel_x, 1] = (
            stego[pixel_y, pixel_x, 1] & 0b11111000
        ) | g_bits

        stego[pixel_y, pixel_x, 2] = (
            stego[pixel_y, pixel_x, 2] & 0b11111100
        ) | b_bits

    # ---------------------------------------------------------
    # Flatten secret image
    # ---------------------------------------------------------

    secret_pixels_array = secret.reshape(-1, 3)

    # ---------------------------------------------------------
    # Embed secret image starting after metadata pixels
    # ---------------------------------------------------------

    for i, secret_pixel in enumerate(secret_pixels_array):

        cover_index = i + METADATA_PIXELS

        pixel_y = cover_index // cover_width
        pixel_x = cover_index % cover_width

        r_bits = secret_pixel[0] >> 5
        g_bits = secret_pixel[1] >> 5
        b_bits = secret_pixel[2] >> 6

        stego[pixel_y, pixel_x, 0] = (
            stego[pixel_y, pixel_x, 0] & 0b11111000
        ) | r_bits

        stego[pixel_y, pixel_x, 1] = (
            stego[pixel_y, pixel_x, 1] & 0b11111000
        ) | g_bits

        stego[pixel_y, pixel_x, 2] = (
            stego[pixel_y, pixel_x, 2] & 0b11111100
        ) | b_bits

    Image.fromarray(stego).save(output_path, format="PNG")

    print("LSB (3,3,2) encoding successful!")
    print(f"Cover image  : {cover_path}")
    print(f"Secret image : {secret_path}")
    print(f"Stego image  : {output_path}")
    print(f"Secret size  : {secret_width} x {secret_height}")


def decode_image(stego_path, output_path):
    """
    Extract a secret image from an LSB (3,3,2) stego image.
    """

    stego = np.array(
        Image.open(stego_path).convert("RGB"),
        dtype=np.uint8
    )

    stego_height, stego_width = stego.shape[:2]

    # ---------------------------------------------------------
    # Read the 4 metadata pixels
    # ---------------------------------------------------------

    metadata = []

    for i in range(METADATA_PIXELS):

        pixel_y = i // stego_width
        pixel_x = i % stego_width

        r = stego[pixel_y, pixel_x, 0] & 0b00000111
        g = stego[pixel_y, pixel_x, 1] & 0b00000111
        b = stego[pixel_y, pixel_x, 2] & 0b00000011

        value = (
            (r << 5)
            | (g << 2)
            | b
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
        stego_width * stego_height
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

        cover_index = i + METADATA_PIXELS

        pixel_y = cover_index // stego_width
        pixel_x = cover_index % stego_width

        r = stego[pixel_y, pixel_x, 0] & 0b00000111
        g = stego[pixel_y, pixel_x, 1] & 0b00000111
        b = stego[pixel_y, pixel_x, 2] & 0b00000011

        secret_y = i // secret_width
        secret_x = i % secret_width

        secret[secret_y, secret_x, 0] = r << 5
        secret[secret_y, secret_x, 1] = g << 5
        secret[secret_y, secret_x, 2] = b << 6

    Image.fromarray(secret).save(output_path, format="PNG")

    print("LSB (3,3,2) decoding successful!")
    print(f"Stego image : {stego_path}")
    print(f"Recovered   : {output_path}")
    print(f"Secret size : {secret_width} x {secret_height}")


if __name__ == "__main__":
    print("LSB (3,3,2) Image Steganography")
