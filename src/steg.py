import argparse

from PIL import Image

from encoder import encode_message
from decoder import decode_message
from lsb332 import encode_image as lsb_encode_image
from lsb332 import decode_image as lsb_decode_image
from spiral332 import encode_image as spiral_encode_image
from spiral332 import decode_image as spiral_decode_image


END_MARKER_SIZE = 13


def show_capacity(image_path):
    try:
        image = Image.open(image_path).convert("RGB")

        width, height = image.size
        channels = 3

        capacity_bits = width * height * channels
        capacity_bytes = capacity_bits // 8
        max_message_bytes = capacity_bytes - END_MARKER_SIZE

        print("\nImage Capacity")
        print("------------------------------")
        print(f"Image             : {image_path}")
        print(f"Width             : {width} pixels")
        print(f"Height            : {height} pixels")
        print(f"Color channels    : {channels}")
        print(f"Total capacity    : {capacity_bytes} bytes")
        print(f"Maximum message   : {max_message_bytes} bytes")

    except FileNotFoundError:
        print(f"\nError: Image not found: {image_path}")

    except OSError as error:
        print(f"\nError: Unable to process image: {error}")


def get_image_encoder(method):
    if method == "lsb332":
        return lsb_encode_image

    if method == "spiral332":
        return spiral_encode_image

    raise ValueError(f"Unsupported image steganography method: {method}")


def get_image_decoder(method):
    if method == "lsb332":
        return lsb_decode_image

    if method == "spiral332":
        return spiral_decode_image

    raise ValueError(f"Unsupported image steganography method: {method}")


def main():
    parser = argparse.ArgumentParser(
        description="Steganography Tool for text and image hiding"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # ---------------------------------------------------------
    # Text Encode
    # ---------------------------------------------------------
    encode_parser = subparsers.add_parser(
        "encode",
        help="Hide a secret message inside an image"
    )

    encode_parser.add_argument(
        "--image",
        required=True,
        help="Path to the cover image"
    )

    encode_parser.add_argument(
        "--output",
        required=True,
        help="Path for the generated stego image"
    )

    message_group = encode_parser.add_mutually_exclusive_group(
        required=True
    )

    message_group.add_argument(
        "--message",
        help="Secret message to hide"
    )

    message_group.add_argument(
        "--message-file",
        help="Path to a text file containing the secret message"
    )

    # ---------------------------------------------------------
    # Text Decode
    # ---------------------------------------------------------
    decode_parser = subparsers.add_parser(
        "decode",
        help="Extract a hidden message from an image"
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
        help="Show the message capacity of an image"
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
        required=True,
        choices=["lsb332", "spiral332"],
        help="Image steganography method"
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
        help="Extract a hidden image from a stego image"
    )

    image_decode_parser.add_argument(
        "--method",
        required=True,
        choices=["lsb332", "spiral332"],
        help="Image steganography method"
    )

    image_decode_parser.add_argument(
        "--image",
        required=True,
        help="Path to the stego image"
    )

    image_decode_parser.add_argument(
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
            if args.message_file:
                try:
                    with open(
                        args.message_file,
                        "r",
                        encoding="utf-8"
                    ) as file:
                        message = file.read()

                except FileNotFoundError:
                    print(
                        f"\nError: Message file not found: "
                        f"{args.message_file}"
                    )
                    return

                except OSError as error:
                    print(
                        f"\nError: Unable to read message file: "
                        f"{error}"
                    )
                    return

            else:
                message = args.message

            encode_message(
                args.image,
                args.output,
                message
            )

        except (ValueError, OSError) as error:
            print(f"\nError: {error}")

    # ---------------------------------------------------------
    # Text Decode
    # ---------------------------------------------------------
    elif args.command == "decode":
        try:
            message = decode_message(args.image)

            print("\nHidden message:")
            print(message)

        except (ValueError, OSError) as error:
            print(f"\nError: {error}")

    # ---------------------------------------------------------
    # Text Capacity
    # ---------------------------------------------------------
    elif args.command == "capacity":
        show_capacity(args.image)

    # ---------------------------------------------------------
    # Image Encode
    # ---------------------------------------------------------
    elif args.command == "image-encode":
        try:
            encoder = get_image_encoder(args.method)

            encoder(
                args.cover,
                args.secret,
                args.output
            )

        except (ValueError, OSError) as error:
            print(f"\nError: {error}")

    # ---------------------------------------------------------
    # Image Decode
    # ---------------------------------------------------------
    elif args.command == "image-decode":
        try:
            decoder = get_image_decoder(args.method)

            decoder(
                args.image,
                args.output
            )

        except (ValueError, OSError) as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    main()
