from PIL import Image


END_MARKER = b"#####END#####"


def encode_message(input_image, output_image, message):
    try:
        image = Image.open(input_image)
        image = image.convert("RGB")

        # Convert message to UTF-8 bytes
        message_bytes = message.encode("utf-8")

        # Add end marker
        data = message_bytes + END_MARKER

        # Convert bytes into binary
        binary_data = "".join(
            format(byte, "08b") for byte in data
        )

        # Get image pixels
        pixels = list(image.get_flattened_data())

        # Calculate image capacity
        capacity = len(pixels) * 3

        if len(binary_data) > capacity:
            max_bytes = capacity // 8

            raise ValueError(
                f"Message is too large. "
                f"Maximum capacity is approximately {max_bytes} bytes."
            )

        new_pixels = []
        data_index = 0

        for pixel in pixels:
            r, g, b = pixel
            channels = [r, g, b]

            for i in range(3):
                if data_index < len(binary_data):
                    channels[i] = (
                        channels[i] & ~1
                    ) | int(binary_data[data_index])

                    data_index += 1

            new_pixels.append(tuple(channels))

        image.putdata(new_pixels)
        image.save(output_image, format="PNG")

        print("\nMessage successfully hidden!")
        print(f"Input image : {input_image}")
        print(f"Output image: {output_image}")
        print(f"Message size: {len(message_bytes)} bytes")

    except FileNotFoundError:
        print(f"Error: Input image not found: {input_image}")

    except PermissionError:
        print("Error: Permission denied while accessing the image.")

    except OSError as error:
        print(f"Error: Unable to process image: {error}")

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    input_image = input("Enter cover image path: ").strip()
    output_image = input("Enter output image path: ").strip()
    message = input("Enter secret message: ")

    encode_message(input_image, output_image, message)