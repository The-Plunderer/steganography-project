import struct

from PIL import Image

try:
    from src.crypto_utils import encrypt_data, decrypt_data
except ModuleNotFoundError:
    from crypto_utils import encrypt_data, decrypt_data

PAYLOAD_MAGIC = b"ESTG"
PAYLOAD_VERSION = 1

PAYLOAD_HEADER_FORMAT = "!4sBI"
PAYLOAD_HEADER_SIZE = struct.calcsize(PAYLOAD_HEADER_FORMAT)


MAGIC = b"STG1"
VERSION = 1

HEADER_FORMAT = "!4sBII"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


def serialize_image(image_path):
    """
    Convert an RGB image into a byte payload.

    Format:
        4 bytes  -> magic
        1 byte   -> version
        4 bytes  -> width
        4 bytes  -> height
        remaining -> RGB pixel data
    """

    image = Image.open(image_path).convert("RGB")

    width, height = image.size
    pixel_data = image.tobytes()

    header = struct.pack(
        HEADER_FORMAT,
        MAGIC,
        VERSION,
        width,
        height
    )

    return header + pixel_data


def deserialize_image(data, output_path):
    """
    Convert a serialized image payload back into an RGB image.
    """

    if len(data) < HEADER_SIZE:
        raise ValueError("Serialized image data is too short.")

    magic, version, width, height = struct.unpack(
        HEADER_FORMAT,
        data[:HEADER_SIZE]
    )

    if magic != MAGIC:
        raise ValueError("Invalid encrypted steganography payload.")

    if version != VERSION:
        raise ValueError(
            f"Unsupported payload version: {version}"
        )

    if width <= 0 or height <= 0:
        raise ValueError("Invalid image dimensions.")

    pixel_data = data[HEADER_SIZE:]

    expected_size = width * height * 3

    if len(pixel_data) != expected_size:
        raise ValueError(
            "Image data size does not match the stored dimensions."
        )

    image = Image.frombytes(
        "RGB",
        (width, height),
        pixel_data
    )

    image.save(output_path)

    return image

def encrypt_image(image_path, password):
    """
    Serialize and encrypt an image.

    Returns:
        Encrypted image payload as bytes.
    """

    data = serialize_image(image_path)

    return encrypt_data(data, password)


def decrypt_image(encrypted_data, password, output_path):
    """
    Decrypt and deserialize an image.
    """

    data = decrypt_data(
        encrypted_data,
        password
    )

    return deserialize_image(
        data,
        output_path
    )

def embed_byte_into_pixel(pixel, value):
    """
    Store one byte using the (3,3,2) bit allocation.

    Red   -> 3 bits
    Green -> 3 bits
    Blue  -> 2 bits
    """

    r, g, b = pixel

    r = (r & 0b11111000) | ((value >> 5) & 0b00000111)
    g = (g & 0b11111000) | ((value >> 2) & 0b00000111)
    b = (b & 0b11111100) | (value & 0b00000011)

    return r, g, b


def extract_byte_from_pixel(pixel):
    """
    Extract one byte from a (3,3,2)-encoded pixel.
    """

    r, g, b = pixel

    return (
        ((r & 0b00000111) << 5)
        | ((g & 0b00000111) << 2)
        | (b & 0b00000011)
    )


def embed_payload(cover_path, payload, output_path):
    """
    Embed an arbitrary byte payload into a cover image
    using the (3,3,2) method.
    """

    if not isinstance(payload, bytes):
        raise TypeError("Payload must be bytes.")

    image = Image.open(cover_path).convert("RGB")

    width, height = image.size
    capacity = width * height

    total_required = PAYLOAD_HEADER_SIZE + len(payload)

    if total_required > capacity:
        raise ValueError(
            f"Payload too large. Required: {total_required} "
            f"bytes, capacity: {capacity} bytes."
        )

    header = struct.pack(
        PAYLOAD_HEADER_FORMAT,
        PAYLOAD_MAGIC,
        PAYLOAD_VERSION,
        len(payload)
    )

    data = header + payload

    # inside extract_payload()
    pixels = list(image.get_flattened_data())

    for index, value in enumerate(data):
        pixels[index] = embed_byte_into_pixel(
            pixels[index],
            value
        )

    stego = Image.new(
        "RGB",
        (width, height)
    )

    stego.putdata(pixels)
    stego.save(output_path)

    return output_path


def extract_payload(stego_path):
    """
    Extract an arbitrary byte payload from a stego image.
    """

    image = Image.open(stego_path).convert("RGB")

    pixels = list(image.get_flattened_data())

    if len(pixels) < PAYLOAD_HEADER_SIZE:
        raise ValueError(
            "Stego image is too small to contain a payload."
        )

    header_bytes = bytes(
        extract_byte_from_pixel(pixels[index])
        for index in range(PAYLOAD_HEADER_SIZE)
    )

    magic, version, payload_length = struct.unpack(
        PAYLOAD_HEADER_FORMAT,
        header_bytes
    )

    if magic != PAYLOAD_MAGIC:
        raise ValueError(
            "Invalid encrypted steganography payload."
        )

    if version != PAYLOAD_VERSION:
        raise ValueError(
            f"Unsupported payload version: {version}"
        )

    capacity = len(pixels) - PAYLOAD_HEADER_SIZE

    if payload_length > capacity:
        raise ValueError(
            "Payload length exceeds image capacity."
        )

    start = PAYLOAD_HEADER_SIZE
    end = start + payload_length

    return bytes(
        extract_byte_from_pixel(pixels[index])
        for index in range(start, end)
    )

def encrypt_and_embed(
    cover_path,
    secret_path,
    password,
    output_path
):
    """
    Encrypt a secret image and embed it into a cover image.
    """

    encrypted = encrypt_image(
        secret_path,
        password
    )

    return embed_payload(
        cover_path,
        encrypted,
        output_path
    )


def extract_and_decrypt(
    stego_path,
    password,
    output_path
):
    """
    Extract an encrypted image payload and decrypt it.
    """

    encrypted = extract_payload(
        stego_path
    )

    return decrypt_image(
        encrypted,
        password,
        output_path
    )
