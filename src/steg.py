import argparse

from encoder import encode_message
from decoder import decode_message

from lsb332 import (
    encode_image as lsb_encode_image,
    decode_image as lsb_decode_image
)

from spiral332 import (
    encode_image as spiral_encode_image,
    decode_image as spiral_decode_image
)

from adaptive332 import (
    encode_image as adaptive_encode_image,
    decode_image as adaptive_decode_image
)

from encrypted_steg import (
    encrypt_and_embed,
    extract_and_decrypt
)


def get_image_encoder(method):
    """
    Return the image encoder corresponding to the selected method.
    """

    if method == "lsb332":
        return lsb_encode_image

    if method == "spiral332":
        return spiral_encode_image

    if method == "adaptive332":
        return adaptive_encode_image

    raise ValueError(
        f"Unsupported image encoding method: {method}"
    )


def get_image_decoder(method):
    """
    Return the image decoder corresponding to the selected method.
    """

    if method == "lsb332":
        return lsb_decode_image

    if method == "spiral332":
        return spiral_decode_image

    if method == "adaptive332":
        return adaptive_decode_image

    raise ValueError(
        f"Unsupported image decoding method: {method}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Steganography CLI"
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    # ---------------------------------------------------------
    # Text Encode
    # ---------------------------------------------------------
    encode_parser = subparsers.add_parser(
        "encode",
        help="Hide a text message inside an image"
    )

    encode_parser.add_argument(
        "--image",
        required=True,
        help="Path to the cover image"
    )

    encode_parser.add_argument(
        "--message",
        help="Text message to hide"
    )

    encode_parser.add_argument(
        "--message-file",
        help="Path to a text file containing the message"
    )

    encode_parser.add_argument(
        "--output",
        required=True,
        help="Path for the generated stego image"
    )

    # ---------------------------------------------------------
    # Text Decode
    # ---------------------------------------------------------
    decode_parser = subparsers.add_parser(
        "decode",
        help="Extract a text message from an image"
    )

    decode_parser.add_argument(
        "--image",
        required=True,
        help="Path to the stego image"
    )

    # ---------------------------------------------------------
    # Text Capacity
    # ---------------------------------------------------------
    capacity_parser = subparsers.add_parser(
        "capacity",
        help="Show text message capacity of an image"
    )

    capacity_parser.add_argument(
        "--image",
        required=True,
        help="Path to the image"
    )

    # ---------------------------------------------------------
    # Image Encode
    # ---------------------------------------------------------
    image_encode_parser = subparsers.add_parser(
        "image-encode",
        help="Hide one image inside another image"
    )

    image_encode_parser.add_argument(
        "--method",
        choices=["lsb332", "spiral332", "adaptive332"],
        required=True,
        help="Steganography method"
    )

    image_encode_parser.add_argument(
        "--cover",
        required=True,
        help="Path to the cover image"
    )

    image_encode_parser.add_argument(
        "--secret",
        required=True,
        help="Path to the secret image"
    )

    image_encode_parser.add_argument(
        "--output",
        required=True,
        help="Path for the generated stego image"
    )

    # ---------------------------------------------------------
    # Image Decode
    # ---------------------------------------------------------
    image_decode_parser = subparsers.add_parser(
        "image-decode",
        help="Recover a hidden image"
    )

    image_decode_parser.add_argument(
        "--method",
        choices=["lsb332", "spiral332", "adaptive332"],
        required=True,
        help="Steganography method"
    )

    image_decode_parser.add_argument(
        "--image",
        required=True,
        help="Path to the stego image"
    )

    image_decode_parser.add_argument(
        "--output",
        required=True,
        help="Path for the recovered image"
    )

    # ---------------------------------------------------------
    # Secure Image Encode
    # ---------------------------------------------------------
    secure_encode_parser = subparsers.add_parser(
        "secure-image-encode",
        help="Encrypt and hide one image inside another image"
    )

    secure_encode_parser.add_argument(
        "--cover",
        required=True,
        help="Path to the cover image"
    )

    secure_encode_parser.add_argument(
        "--secret",
        required=True,
        help="Path to the secret image"
    )

    secure_encode_parser.add_argument(
        "--password",
        required=True,
        help="Password used for encryption"
    )

    secure_encode_parser.add_argument(
        "--output",
        required=True,
        help="Path for the generated encrypted stego image"
    )

    # ---------------------------------------------------------
    # Secure Image Decode
    # ---------------------------------------------------------
    secure_decode_parser = subparsers.add_parser(
        "secure-image-decode",
        help="Extract and decrypt a hidden image"
    )

    secure_decode_parser.add_argument(
        "--image",
        required=True,
        help="Path to the encrypted stego image"
    )

    secure_decode_parser.add_argument(
        "--password",
        required=True,
        help="Password used for decryption"
    )

    secure_decode_parser.add_argument(
        "--output",
        required=True,
        help="Path for the recovered secret image"
    )

    args = parser.parse_args()

    # ---------------------------------------------------------
    # Text Encode
    # ---------------------------------------------------------
    if args.command == "encode":
        try:
            if args.message is None and args.message_file is None:
                raise ValueError(
                    "Provide either --message or --message-file."
                )

            if args.message is not None and args.message_file is not None:
                raise ValueError(
                    "Use either --message or --message-file, not both."
                )

            if args.message_file:
                with open(
                    args.message_file,
                    "r",
                    encoding="utf-8"
                ) as file:
                    message = file.read()
            else:
                message = args.message

            encode_message(
                args.image,
                message,
                args.output
            )

            print("\nMessage encoded successfully.")
            print(f"Stego image: {args.output}")

        except (ValueError, OSError) as error:
            print(f"\nError: {error}")

    # ---------------------------------------------------------
    # Text Decode
    # ---------------------------------------------------------
    elif args.command == "decode":
        try:
            message = decode_message(
                args.image
            )

            print("\nDecoded message:")
            print(message)

        except (ValueError, OSError) as error:
            print(f"\nError: {error}")

    # ---------------------------------------------------------
    # Text Capacity
    # ---------------------------------------------------------
    elif args.command == "capacity":
        try:
            from PIL import Image

            image = Image.open(args.image).convert("RGB")

            width, height = image.size

            total_bits = width * height * 3
            total_bytes = total_bits // 8

            print(f"\nImage size: {width} x {height}")
            print(f"Approximate capacity: {total_bytes} bytes")

        except (ValueError, OSError) as error:
            print(f"\nError: {error}")

    # ---------------------------------------------------------
    # Image Encode
    # ---------------------------------------------------------
    elif args.command == "image-encode":
        try:
            encoder = get_image_encoder(
                args.method
            )

            encoder(
                args.cover,
                args.secret,
                args.output
            )

            print("\nImage steganography successful.")
            print(f"Method: {args.method}")
            print(f"Stego image: {args.output}")

        except (ValueError, OSError) as error:
            print(f"\nError: {error}")

    # ---------------------------------------------------------
    # Image Decode
    # ---------------------------------------------------------
    elif args.command == "image-decode":
        try:
            decoder = get_image_decoder(
                args.method
            )

            decoder(
                args.image,
                args.output
            )

            print("\nImage recovery successful.")
            print(f"Method: {args.method}")
            print(f"Recovered image: {args.output}")

        except (ValueError, OSError) as error:
            print(f"\nError: {error}")

    # ---------------------------------------------------------
    # Secure Image Encode
    # ---------------------------------------------------------
    elif args.command == "secure-image-encode":
        try:
            encrypt_and_embed(
                args.cover,
                args.secret,
                args.password,
                args.output
            )

            print(
                "\nEncrypted image steganography successful."
            )
            print(f"Stego image: {args.output}")

        except (ValueError, OSError) as error:
            print(f"\nError: {error}")

    # ---------------------------------------------------------
    # Secure Image Decode
    # ---------------------------------------------------------
    elif args.command == "secure-image-decode":
        try:
            extract_and_decrypt(
                args.image,
                args.password,
                args.output
            )

            print(
                "\nEncrypted image recovery successful."
            )
            print(f"Recovered image: {args.output}")

        except (ValueError, OSError) as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    main()