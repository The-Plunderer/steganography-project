from PIL import Image


END_MARKER = b"#####END#####"


def decode_message(input_image):
    try:
        image = Image.open(input_image)
        image = image.convert("RGB")

        pixels = list(image.get_flattened_data())

        binary_data = ""

        # Extract the LSB from every RGB channel
        for pixel in pixels:
            r, g, b = pixel

            for channel in (r, g, b):
                binary_data += str(channel & 1)

        data = bytearray()

        # Convert binary data back into bytes
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i + 8]

            if len(byte) < 8:
                break

            data.append(int(byte, 2))

            # Stop as soon as the end marker is found
            if data.endswith(END_MARKER):
                message_bytes = data[:-len(END_MARKER)]

                try:
                    return message_bytes.decode("utf-8")
                except UnicodeDecodeError:
                    raise ValueError(
                        "Hidden data was found, but it is not valid UTF-8 text."
                    )

        raise ValueError(
            "No valid hidden message was found in this image."
        )

    except FileNotFoundError:
        raise ValueError(f"Stego image not found: {input_image}")

    except OSError as error:
        raise ValueError(f"Unable to process image: {error}")


if __name__ == "__main__":
    input_image = input("Enter stego image path: ").strip()

    try:
        message = decode_message(input_image)

        print("\nHidden message:")
        print(message)

    except ValueError as error:
        print(f"\nError: {error}")
