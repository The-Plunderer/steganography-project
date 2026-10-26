from pathlib import Path

from getpass import getpass

from qr_secure import (
    generate_key_pair,
    create_secure_qr,
    decrypt_secure_qr,
)

import argparse

from encoder import encode_message
from decoder import decode_message

from lsb332 import (
    encode_image as lsb_encode_image,
    decode_image as lsb_decode_image,
)

from spiral332 import (
    encode_image as spiral_encode_image,
    decode_image as spiral_decode_image,
)

from adaptive332 import (
    encode_image as adaptive_encode_image,
    decode_image as adaptive_decode_image,
)

from encrypted_steg import (
    encrypt_and_embed,
    extract_and_decrypt,
)

from qr_contact import (
    create_vcard,
    generate_contact_qr,
    decode_contact_qr,
    export_vcard,
)



def get_image_encoder(method):
    """Return the image encoder for the selected method."""
    if method == "lsb332":
        return lsb_encode_image

    if method == "spiral332":
        return spiral_encode_image

    if method == "adaptive332":
        return adaptive_encode_image

    raise ValueError(f"Unsupported image encoding method: {method}")


def get_image_decoder(method):
    """Return the image decoder for the selected method."""
    if method == "lsb332":
        return lsb_decode_image

    if method == "spiral332":
        return spiral_decode_image

    if method == "adaptive332":
        return adaptive_decode_image

    raise ValueError(f"Unsupported image decoding method: {method}")


def main():
    parser = argparse.ArgumentParser(
        description="Steganography CLI"
    )

    subparsers = parser.add_subparsers(dest="command")

    # ---------------------------------------------------------
    # Text Encode
    # ---------------------------------------------------------
    encode_parser = subparsers.add_parser(
        "encode",
        help="Encode a text message into an image",
    )
    encode_parser.add_argument(
        "--image", required=True, help="Input cover image"
    )
    encode_parser.add_argument(
        "--message", default=None, help="Message to encode"
    )
    encode_parser.add_argument(
        "--message-file", default=None, help="Text file containing the message"
    )
    encode_parser.add_argument(
        "--output", required=True, help="Output stego image"
    )

    # ---------------------------------------------------------
    # Text Decode
    # ---------------------------------------------------------
    decode_parser = subparsers.add_parser(
        "decode",
        help="Decode a text message from an image",
    )
    decode_parser.add_argument(
        "--image", required=True, help="Input stego image"
    )

    # ---------------------------------------------------------
    # Text Capacity
    # ---------------------------------------------------------
    capacity_parser = subparsers.add_parser(
        "capacity",
        help="Estimate text capacity of an image",
    )
    capacity_parser.add_argument(
        "--image", required=True, help="Input image"
    )

    # ---------------------------------------------------------
    # Image Encode
    # ---------------------------------------------------------
    image_encode_parser = subparsers.add_parser(
        "image-encode",
        help="Hide a secret image inside a cover image",
    )
    image_encode_parser.add_argument(
        "--method",
        choices=["lsb332", "spiral332", "adaptive332"],
        required=True,
        help="Image steganography method",
    )
    image_encode_parser.add_argument(
        "--cover", required=True, help="Cover image path"
    )
    image_encode_parser.add_argument(
        "--secret", required=True, help="Secret image path"
    )
    image_encode_parser.add_argument(
        "--output", required=True, help="Output stego image path"
    )

    # ---------------------------------------------------------
    # Image Decode
    # ---------------------------------------------------------
    image_decode_parser = subparsers.add_parser(
        "image-decode",
        help="Recover a secret image",
    )
    image_decode_parser.add_argument(
        "--method",
        choices=["lsb332", "spiral332", "adaptive332"],
        required=True,
        help="Image steganography method",
    )
    image_decode_parser.add_argument(
        "--image", required=True, help="Input stego image path"
    )
    image_decode_parser.add_argument(
        "--output", required=True, help="Recovered secret image path"
    )

    # ---------------------------------------------------------
    # Secure Image Encode
    # ---------------------------------------------------------
    secure_encode_parser = subparsers.add_parser(
        "secure-image-encode",
        help="Encrypt and hide a secret image",
    )
    secure_encode_parser.add_argument(
        "--cover", required=True, help="Cover image path"
    )
    secure_encode_parser.add_argument(
        "--secret", required=True, help="Secret image path"
    )
    secure_encode_parser.add_argument(
        "--password", required=True, help="Encryption password"
    )
    secure_encode_parser.add_argument(
        "--output", required=True, help="Output encrypted stego image"
    )

    # ---------------------------------------------------------
    # Secure Image Decode
    # ---------------------------------------------------------
    secure_decode_parser = subparsers.add_parser(
        "secure-image-decode",
        help="Extract and decrypt a secret image",
    )
    secure_decode_parser.add_argument(
        "--image", required=True, help="Input encrypted stego image"
    )
    secure_decode_parser.add_argument(
        "--password", required=True, help="Decryption password"
    )
    secure_decode_parser.add_argument(
        "--output", required=True, help="Recovered secret image path"
    )

    # ---------------------------------------------------------
    # Contact QR Create
    # ---------------------------------------------------------
    contact_create_parser = subparsers.add_parser(
        "contact-qr-create",
        help="Create a contact QR with explicit sharing consent",
    )
    contact_create_parser.add_argument(
        "--name", required=True, help="Contact's full name"
    )
    contact_create_parser.add_argument(
        "--phone", default="", help="Phone number approved for sharing"
    )
    contact_create_parser.add_argument(
        "--email", default="", help="Email approved for sharing"
    )
    contact_create_parser.add_argument(
        "--organization", default="", help="Organization"
    )
    contact_create_parser.add_argument(
        "--title", default="", help="Job title"
    )
    contact_create_parser.add_argument(
        "--address", default="", help="Address approved for sharing"
    )
    contact_create_parser.add_argument(
        "--consent",
        action="store_true",
        help="Confirm that the contact explicitly agreed to share these details",
    )
    contact_create_parser.add_argument(
        "--output", required=True, help="Output QR image path"
    )

    # ---------------------------------------------------------
    # Contact QR Scan
    # ---------------------------------------------------------
    contact_scan_parser = subparsers.add_parser(
        "contact-qr-scan",
        help="Decode and display a contact QR",
    )
    contact_scan_parser.add_argument(
        "--image", required=True, help="Contact QR image path"
    )

    # ---------------------------------------------------------
    # Contact Export
    # ---------------------------------------------------------
    contact_export_parser = subparsers.add_parser(
        "contact-export",
        help="Export a contact QR to a vCard file",
    )
    contact_export_parser.add_argument(
        "--image", required=True, help="Contact QR image path"
    )
    contact_export_parser.add_argument(
        "--output", required=True, help="Output .vcf file path"
    )

    # ---------------------------------------------------------
    # Secure QR Key Generation
    # ---------------------------------------------------------
    secure_keygen_parser = subparsers.add_parser(
        "secure-qr-keygen",
        help="Generate recipient-specific RSA keys for secure QR",
    )
    secure_keygen_parser.add_argument(
        "--private-key",
        required=True,
        help="Output path for the encrypted private key",
    )
    secure_keygen_parser.add_argument(
        "--public-key",
        required=True,
        help="Output path for the public key",
    )

    # ---------------------------------------------------------
    # Secure QR Create
    # ---------------------------------------------------------
    secure_qr_create_parser = subparsers.add_parser(
        "secure-qr-create",
        help="Encrypt a message for a recipient and create a QR",
    )
    secure_qr_create_parser.add_argument(
        "--message",
        default=None,
        help="Message to encrypt",
    )
    secure_qr_create_parser.add_argument(
        "--message-file",
        default=None,
        help="UTF-8 text file containing the message",
    )
    secure_qr_create_parser.add_argument(
        "--public-key",
        required=True,
        help="Recipient's public key",
    )
    secure_qr_create_parser.add_argument(
        "--output",
        required=True,
        help="Output encrypted QR image",
    )

    # ---------------------------------------------------------
    # Secure QR Decrypt
    # ---------------------------------------------------------
    secure_qr_decrypt_parser = subparsers.add_parser(
        "secure-qr-decrypt",
        help="Decrypt a secure QR using the recipient's private key",
    )
    secure_qr_decrypt_parser.add_argument(
        "--image",
        required=True,
        help="Encrypted QR image",
    )
    secure_qr_decrypt_parser.add_argument(
        "--private-key",
        required=True,
        help="Recipient's encrypted private key",
    )
    secure_qr_decrypt_parser.add_argument(
        "--output",
        default=None,
        help="Optional file for the recovered message",
    )

    # Parse command-line arguments only after all parsers are defined.
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
                    encoding="utf-8",
                ) as file:
                    message = file.read()
            else:
                message = args.message

            encode_message(args.image, args.output, message)

            print("\nMessage encoded successfully.")
            print(f"Stego image: {args.output}")

        except (ValueError, OSError) as error:
            print(f"\nError: {error}")

    # ---------------------------------------------------------
    # Text Decode
    # ---------------------------------------------------------
    elif args.command == "decode":
        try:
            message = decode_message(args.image)

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
            encoder = get_image_encoder(args.method)
            encoder(args.cover, args.secret, args.output)

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
            decoder = get_image_decoder(args.method)
            decoder(args.image, args.output)

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
                args.output,
            )

            print("\nEncrypted image steganography successful.")
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
                args.output,
            )

            print("\nEncrypted image recovery successful.")
            print(f"Recovered image: {args.output}")

        except (ValueError, OSError) as error:
            print(f"\nError: {error}")

    # ---------------------------------------------------------
    # Contact QR Create
    # ---------------------------------------------------------
    elif args.command == "contact-qr-create":
        try:
            vcard = create_vcard(
                full_name=args.name,
                phone=args.phone,
                email=args.email,
                organization=args.organization,
                title=args.title,
                address=args.address,
                consent=args.consent,
            )

            generate_contact_qr(vcard, args.output)

            print("\nContact QR created successfully.")
            print(f"QR image: {args.output}")
            print("Anyone scanning this QR may read its contact details.")

        except (ValueError, OSError, PermissionError) as error:
            print(f"\nError: {error}")

    # ---------------------------------------------------------
    # Contact QR Scan
    # ---------------------------------------------------------
    elif args.command == "contact-qr-scan":
        try:
            vcard = decode_contact_qr(args.image)

            print("\nDecoded contact vCard:")
            print(vcard)

        except (ValueError, OSError) as error:
            print(f"\nError: {error}")

    # ---------------------------------------------------------
    # Contact Export
    # ---------------------------------------------------------
    elif args.command == "contact-export":
        try:
            vcard = decode_contact_qr(args.image)
            export_vcard(vcard, args.output)

            print("\nContact exported successfully.")
            print(f"vCard file: {args.output}")

        except (ValueError, OSError) as error:
            print(f"\nError: {error}")

    # ---------------------------------------------------------
    # Secure QR Key Generation
    # ---------------------------------------------------------
    elif args.command == "secure-qr-keygen":
        try:
            if args.private_key == args.public_key:
                raise ValueError(
                    "Private and public keys must use different paths."
                )

            passphrase = getpass(
                "Create a passphrase for the private key: "
            )
            confirmation = getpass("Confirm the passphrase: ")

            if passphrase != confirmation:
                raise ValueError("Passphrases do not match.")

            generate_key_pair(
                args.private_key,
                args.public_key,
                passphrase,
            )

            print("\nRecipient key pair created successfully.")
            print(f"Private key: {args.private_key}")
            print(f"Public key: {args.public_key}")
            print("Keep the private key and its passphrase secret.")

        except (ValueError, OSError, PermissionError) as error:
            print(f"\nError: {error}")

    # ---------------------------------------------------------
    # Secure QR Create
    # ---------------------------------------------------------
    elif args.command == "secure-qr-create":
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
                    encoding="utf-8",
                ) as file:
                    message = file.read()
            else:
                message = args.message

            create_secure_qr(
                message,
                args.public_key,
                args.output,
            )

            print("\nSecure QR created successfully.")
            print(f"QR image: {args.output}")
            print("The QR contains an encrypted payload.")

        except (ValueError, OSError, PermissionError) as error:
            print(f"\nError: {error}")

    # ---------------------------------------------------------
    # Secure QR Decrypt
    # ---------------------------------------------------------
    elif args.command == "secure-qr-decrypt":
        try:
            passphrase = getpass(
                "Enter the recipient private-key passphrase: "
            )

            message = decrypt_secure_qr(
                args.image,
                args.private_key,
                passphrase,
            )

            if args.output:
                output_path = Path(args.output)

                if output_path.exists():
                    raise FileExistsError(
                        f"Output file already exists: {output_path}"
                    )

                output_path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )
                output_path.write_text(
                    message,
                    encoding="utf-8",
                )

                print("\nSecure QR decrypted successfully.")
                print(f"Recovered message saved to: {output_path}")
            else:
                print("\nDecrypted message:")
                print(message)

        except (ValueError, OSError, PermissionError) as error:
            print(f"\nError: {error}")

if __name__ == "__main__":
    main()
