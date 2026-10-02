# Steganography and Visual Cryptography

A final-year project focused on the implementation and study of **image steganography** and **visual cryptography** techniques.

## Current Module

**Basic Image Steganography using Least Significant Bit (LSB) Substitution**

The current implementation hides secret text inside an RGB image by modifying the least significant bit of each color channel.

The project is being developed incrementally, with cryptographic techniques and visual cryptography planned for later stages.

---

## Objectives

* Hide secret information inside an image.
* Extract hidden information from a stego image.
* Implement the process using a command-line interface.
* Validate image capacity before hiding data.
* Support UTF-8 text messages.
* Handle invalid input and oversized messages.
* Implement automated testing.
* Study the security and limitations of LSB steganography.
* Integrate cryptographic techniques in later versions.
* Implement visual cryptography in later versions.

---

## Technology Stack

* **Python 3**
* **Pillow** — image processing
* **pytest** — automated testing
* **Git** — version control
* **GitHub** — source-code hosting
* **Git Bash** — command-line environment

---

## Project Structure

```text
steganography-project/
│
├── src/
│   ├── encoder.py
│   ├── decoder.py
│   └── steg.py
│
├── images/
│   └── cover.png
│
├── output/
│   └── stego.png
│
├── tests/
│   └── test_steganography.py
│
├── README.md
├── requirements.txt
├── .gitignore
└── .git/
```

### File Description

| File / Directory   | Purpose                                 |
| ------------------ | --------------------------------------- |
| `src/encoder.py`   | Hides a secret message inside an image  |
| `src/decoder.py`   | Extracts a hidden message from an image |
| `src/steg.py`      | Unified command-line interface          |
| `tests/`           | Automated tests                         |
| `images/`          | Cover/input images                      |
| `output/`          | Generated stego images                  |
| `requirements.txt` | Python dependencies                     |
| `.gitignore`       | Files excluded from Git                 |

---

## How LSB Steganography Works

An RGB image contains three color channels for each pixel:

```text
Pixel
 ├── Red
 ├── Green
 └── Blue
```

Each color channel contains an 8-bit value.

For example:

```text
Original pixel:

Red   = 10110100
Green = 01101011
Blue  = 11001010
```

The encoder modifies only the **Least Significant Bit (LSB)**:

```text
Original:

10110100
01101011
11001010

Modified:

10110101
01101010
11001010
```

Only the final bit of each channel is changed. This allows information to be embedded while keeping the visual change to the image very small.

The decoder reads the LSBs from the RGB channels and reconstructs the hidden message.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/The-Plunderer/steganography-project.git
cd steganography-project
```

### 2. Create a Virtual Environment

On Windows:

```bash
py -m venv .venv
```

### 3. Activate the Virtual Environment

Using Git Bash:

```bash
source .venv/Scripts/activate
```

### 4. Install Dependencies

```bash
.venv/Scripts/python.exe -m pip install -r requirements.txt
```

The required packages are:

```text
Pillow
pytest
```

---

## Usage

### Encode a Secret Message

Use the `encode` command to hide a message inside a cover image:

```bash
.venv/Scripts/python.exe src/steg.py encode --image images/cover.png --output output/stego.png --message "Hello from my project!"
```

Example output:

```text
Message successfully hidden!
Input image : images/cover.png
Output image: output/stego.png
Message size: 22 bytes
```

The generated stego image will be saved as:

```text
output/stego.png
```

---

### Decode a Secret Message

Use the `decode` command to extract the hidden message:

```bash
.venv/Scripts/python.exe src/steg.py decode --image output/stego.png
```

Example output:

```text
Hidden message:
Hello from my project!
```

---

## Command-Line Help

To display the available commands:

```bash
.venv/Scripts/python.exe src/steg.py --help
```

The CLI currently supports:

```text
encode    Hide a secret message inside an image
decode    Extract a hidden message from an image
```

---

## Running Automated Tests

The project includes automated tests using `pytest`.

Run:

```bash
.venv/Scripts/python.exe -m pytest -v
```

The current test suite checks:

* Normal message encoding and decoding
* Unicode message handling
* Missing image handling
* Oversized message validation

Current result:

```text
4 passed
```

---

## Capacity Validation

The encoder checks whether the secret message can fit inside the selected image.

For an RGB image:

```text
Available bits = width × height × 3
```

The implementation reserves additional space for an end marker that allows the decoder to determine where the hidden message ends.

For the current test image:

```text
Image capacity      = 540000 bytes
Maximum message     = 539987 bytes
```

If the message exceeds the available capacity, the encoder returns an error instead of creating an invalid stego image.

---

## Error Handling

The application handles several common errors, including:

* Missing input images
* Invalid image files
* Permission errors
* Oversized messages
* Missing hidden messages
* Invalid hidden UTF-8 data

Example:

```bash
.venv/Scripts/python.exe src/steg.py decode --image output/nonexistent.png
```

Output:

```text
Error: Stego image not found: output/nonexistent.png
```

---

## Current Limitations

The current implementation is intended as a **basic educational implementation** of LSB image steganography.

### No Encryption

The hidden message is currently stored without encryption.

Anyone who knows the embedding method may be able to extract the message.

### PNG Recommended

The implementation currently works with PNG output.

Lossy formats such as JPEG are not recommended because compression can modify pixel values and destroy embedded LSB data.

### Text Payload Only

The current version supports UTF-8 text messages.

Arbitrary files such as PDFs, documents, or executable files are not supported yet.

### No Authentication

The current implementation does not provide message authentication or integrity verification.

### Basic LSB Technique

LSB substitution is simple and useful for learning, but it is not designed to provide strong protection against steganalysis.

---

## Development Roadmap

### Version 0.1 — Basic LSB Steganography

* [x] Encode text into an image
* [x] Decode text from an image
* [x] UTF-8 support
* [x] Capacity validation
* [x] Basic error handling
* [x] Command-line interface
* [x] Automated tests

### Version 0.2 — Improved CLI

* [ ] Improved command-line validation
* [ ] Better error messages
* [ ] Additional CLI options
* [ ] Improved documentation

### Version 0.3 — Cryptographic Protection

* [ ] Password-based protection
* [ ] Cryptographic encryption
* [ ] Message integrity verification

### Version 0.4 — Advanced Steganography

* [ ] Image-to-image steganography
* [ ] Improved embedding strategies
* [ ] Payload optimization
* [ ] Steganalysis considerations

### Version 0.5 — Visual Cryptography

* [ ] Implement visual cryptography
* [ ] Generate cryptographic shares
* [ ] Reconstruct the secret image
* [ ] Study pixel expansion
* [ ] Evaluate reconstruction quality

### Version 1.0 — Integrated System

* [ ] Combine cryptography and steganography
* [ ] Integrate visual cryptography
* [ ] Improve security
* [ ] Develop a complete user interface
* [ ] Perform final testing
* [ ] Complete project documentation

---

## Testing Status

Current implementation:

```text
Automated Tests: 4/4 PASSED
```

Test coverage:

```text
Encode → Decode          ✓
Unicode Message         ✓
Missing Image Handling  ✓
Oversized Message       ✓
```

---

## Project Status

**Current Stage:** Basic LSB Image Steganography

**Implementation Status:** Working

**Test Status:** 4/4 tests passing

**Next Development Stage:** Improved CLI and cryptographic protection

---

## Academic Project

**Project Title:** Steganography and Visual Cryptography

This project is being developed as part of a final-year academic project, with the goal of studying practical techniques for hiding information in digital media and implementing visual cryptography for secure information sharing.
