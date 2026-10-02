import argparse

from encoder import encode_message
from decoder import decode_message


def main():
    parser = argparse.ArgumentParser(
        description="Basic LSB Image Steganography Tool"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # Encode command
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

    encode_parser.add_argument(
        "--message",
        required=True,
        help="Secret message to hide"
    )

    # Decode command
    decode_parser = subparsers.add_parser(
        "decode",
        help="Extract a hidden message from an image"
    )

    decode_parser.add_argument(
        "--image",
        required=True,
        help="Path to the stego image"
    )

    args = parser.parse_args()

    if args.command == "encode":
        encode_message(
            args.image,
            args.output,
            args.message
        )

    elif args.command == "decode":
        try:
            message = decode_message(args.image)

            print("\nHidden message:")
            print(message)

        except ValueError as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    main()