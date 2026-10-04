# Steganography and Visual Cryptography

This is a final-year project for studying and implementing different techniques used to hide information inside digital images.

The project is being developed step by step. The current work focuses on basic image steganography, including text hiding, image-to-image steganography using LSB `(3,3,2)`, and a Spiral-based variation of the same technique.

Visual cryptography and cryptographic protection will be added in later stages.

---

## Current Progress

The following implementations are currently working:

* Text steganography using basic LSB substitution
* Image-to-image steganography using LSB `(3,3,2)`
* Image-to-image steganography using Spiral `(3,3,2)`
* Secret image extraction
* Image capacity validation
* UTF-8 text support
* Command-line interface for text steganography
* Automated testing using `pytest`

---

## Objectives

The main objectives of this project are:

* Understand how information can be hidden inside digital images.
* Implement basic LSB steganography.
* Hide an image inside another image.
* Compare normal LSB traversal with Spiral traversal.
* Check whether the secret data fits inside the cover image.
* Extract the hidden information from a stego image.
* Measure the quality of the resulting images.
* Study the limitations of basic steganography.
* Add cryptographic and visual cryptography techniques in later stages.

---

## Technology Stack

* **Python 3** — main programming language
* **Pillow** — image loading and saving
* **NumPy** — image array and pixel manipulation
* **pytest** — automated testing
* **Git** — version control
* **GitHub** — source-code hosting
* **Git Bash** — command-line environment
* **PyCharm** — development environment

---

## Project Structure

```text
steganography-project/
│
├── src/
│   ├── encoder.py
│   ├── decoder.py
│   ├── steg.py
│   ├── lsb332.py
│   └── spiral332.py
│
├── images/
│   ├── cover.png
│   └── secret.png
│
├── output/
│   ├── stego.png
│   ├── stego_lsb332.png
│   ├── recovered_lsb332.png
│   ├── stego_spiral332.png
│   └── recovered_spiral332.png
│
├── tests/
│   ├── test_steganography.py
│   ├── test_lsb332.py
│   └── test_spiral332.py
│
├── README.md
├── requirements.txt
├── .gitignore
└── .git/
```

### Main Files

| File                          | Purpose                                        |
| ----------------------------- | ---------------------------------------------- |
| `src/encoder.py`              | Hides a text message inside an image           |
| `src/decoder.py`              | Extracts a hidden text message                 |
| `src/steg.py`                 | Command-line interface for text steganography  |
| `src/lsb332.py`               | Image-to-image LSB `(3,3,2)` implementation    |
| `src/spiral332.py`            | Image-to-image Spiral `(3,3,2)` implementation |
| `tests/test_steganography.py` | Tests for text steganography                   |
| `tests/test_lsb332.py`        | Tests for LSB `(3,3,2)`                        |
| `tests/test_spiral332.py`     | Tests for Spiral `(3,3,2)`                     |
| `images/`                     | Input images used during development           |
| `output/`                     | Generated stego and recovered images           |
| `requirements.txt`            | Python dependencies                            |

---

# 1. Basic LSB Steganography

The first part of the project hides a text message inside an RGB image.

An RGB pixel contains three channels:

```text
Pixel
 ├── Red
 ├── Green
 └── Blue
```

Each channel has an 8-bit value.

For example:

```text
Red   = 10110100
Green = 01101011
Blue  = 11001010
```

The basic LSB implementation changes only the last bit of each channel.

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

Since only the least significant bits are changed, the difference between the original image and the stego image is normally very small.

The decoder reads these LSBs and reconstructs the original text message.

---

# 2. Image-to-Image Steganography

The next stage of the project is different from text steganography.

Instead of hiding a text message, a **secret image is hidden inside a cover image**.

For example:

```text
Cover Image + Secret Image
          │
          ▼
     Steganography
          │
          ▼
      Stego Image
          │
          ▼
       Extraction
          │
          ▼
    Recovered Image
```

The current image-to-image implementation uses an `(3,3,2)` bit allocation.

---

## What Does `(3,3,2)` Mean?

Each RGB pixel contains three 8-bit channels.

For the image-to-image implementation, the least significant bits are divided as follows:

```text
Red   → 3 LSBs
Green → 3 LSBs
Blue  → 2 LSBs

Total = 3 + 3 + 2
      = 8 bits
```

So one cover pixel provides **8 bits of storage**.

The secret pixel is converted into an 8-bit representation:

```text
Secret Red   → 3 most significant bits
Secret Green → 3 most significant bits
Secret Blue  → 2 most significant bits
```

These 8 bits are then placed into the 3-3-2 LSB positions of one cover pixel.

For example:

```text
Cover pixel

Red   : XXXXXXXX
Green : XXXXXXXX
Blue  : XXXXXXXX

             ↓

3-3-2 embedding

Red   : XXXXXRRR
Green : XXXXXGGG
Blue  : XXXXXXBB
```

Here `R`, `G` and `B` represent the bits taken from the secret image.

---

## Why Is the Recovered Image Not Exactly the Same?

The `(3,3,2)` method stores only 8 bits for every secret pixel.

A normal RGB pixel contains:

```text
Red   = 8 bits
Green = 8 bits
Blue  = 8 bits

Total = 24 bits
```

But our current method stores:

```text
Red   = 3 bits
Green = 3 bits
Blue  = 2 bits

Total = 8 bits
```

Therefore, the recovered image is a **quantized version** of the original secret image.

This is an expected limitation of the current implementation.

It also means that the recovered image should not be compared with the original using exact pixel equality.

---

# 3. LSB `(3,3,2)` Implementation

The LSB version processes the cover image in normal row-by-row order.

Conceptually:

```text
(0,0) → (0,1) → (0,2) → ...
   ↓
next row
   ↓
next row
```

The first few pixels are reserved for storing the dimensions of the secret image.

The remaining pixels are used for the secret image data.

The secret image dimensions are stored so that the decoder knows how large the recovered image should be.

---

# 4. Spiral `(3,3,2)` Implementation

The Spiral implementation uses the same `(3,3,2)` bit allocation, but changes the order in which cover pixels are processed.

For a 3 × 3 image, the traversal is:

```text
(0,0) → (0,1) → (0,2)
                   ↓
(1,0) ← (1,1) ← (1,2)
  ↓
(2,0) → (2,1) → (2,2)
```

The actual coordinate order is:

```text
[(0,0), (0,1), (0,2),
 (1,2), (2,2), (2,1),
 (2,0), (1,0), (1,1)]
```

The same order is used during decoding, so the secret image can be reconstructed correctly.

The main difference between the two methods is therefore the **pixel traversal order**, not the number of bits stored in each pixel.

---

# 5. Running the Project

## Installation

Clone the repository:

```bash
git clone https://github.com/The-Plunderer/steganography-project.git
cd steganography-project
```

Create a virtual environment:

```bash
py -m venv .venv
```

Activate it in Git Bash:

```bash
source .venv/Scripts/activate
```

Install the required packages:

```bash
.venv/Scripts/python.exe -m pip install -r requirements.txt
```

Current dependencies:

```text
Pillow
numpy
pytest
```

---

# 6. Text Steganography Commands

### Encode a Message

```bash
.venv/Scripts/python.exe src/steg.py encode --image images/cover.png --output output/stego.png --message "Hello from my project!"
```

### Decode a Message

```bash
.venv/Scripts/python.exe src/steg.py decode --image output/stego.png
```

### Show CLI Help

```bash
.venv/Scripts/python.exe src/steg.py --help
```

---

# 7. Image Steganography Commands

## LSB `(3,3,2)`

Encode the secret image:

```bash
.venv/Scripts/python.exe -c "from src.lsb332 import encode_image; encode_image('images/cover.png','images/secret.png','output/stego_lsb332.png')"
```

Decode it:

```bash
.venv/Scripts/python.exe -c "from src.lsb332 import decode_image; decode_image('output/stego_lsb332.png','output/recovered_lsb332.png')"
```

---

## Spiral `(3,3,2)`

Encode the secret image:

```bash
.venv/Scripts/python.exe -c "from src.spiral332 import encode_image; encode_image('images/cover.png','images/secret.png','output/stego_spiral332.png')"
```

Decode it:

```bash
.venv/Scripts/python.exe -c "from src.spiral332 import decode_image; decode_image('output/stego_spiral332.png','output/recovered_spiral332.png')"
```

---

# 8. Capacity

For the current `(3,3,2)` implementation, one cover pixel is used to store one 8-bit representation of one secret pixel.

Therefore, approximately:

```text
Maximum secret pixels
= Cover width × Cover height - metadata pixels
```

The current implementation reserves four pixels for the secret image dimensions.

For example, with a 1200 × 1200 cover image:

```text
Total cover pixels = 1200 × 1200
                   = 1,440,000 pixels

Reserved pixels    = 4

Available pixels   = 1,439,996
```

A 200 × 200 secret image contains:

```text
200 × 200 = 40,000 pixels
```

Therefore, the test secret image fits comfortably inside the cover image.

---

# 9. Test Results

The project has automated tests for the text, LSB image and Spiral image implementations.

Run all tests with:

```bash
.venv/Scripts/python.exe -m pytest -v
```

Current result:

```text
14 passed
```

The tests cover:

```text
Basic text encoding/decoding
Unicode message handling
Missing image handling
Oversized text message handling

LSB (3,3,2) encoding/decoding
LSB image dimensions
LSB oversized secret image
LSB output generation

Spiral coordinate generation
Spiral coordinate coverage
Spiral (3,3,2) encoding/decoding
Spiral image dimensions
Spiral oversized secret image
Spiral output generation
```

---

# 10. Image Quality Results

A 1200 × 1200 cover image and a 200 × 200 secret image were used for the current test.

### Cover Image vs Stego Image

```text
MSE  = 0.3550
PSNR = 52.6279 dB
```

The high PSNR indicates that the changes made to the cover image are relatively small.

### Secret Image vs Recovered Image

```text
MSE  = 1153.4543
PSNR = 17.5108 dB
```

The lower PSNR here is mainly caused by the 3-3-2 quantization of the secret image.

This is different from the cover-to-stego measurement. The first measurement tells us about the visual change to the cover image, while the second measures how closely the recovered secret resembles the original secret.

---

# 11. LSB vs Spiral

Both implementations use the same:

```text
Bit allocation : 3-3-2
Cover image    : 1200 × 1200
Secret image   : 200 × 200
```

For the current test:

| Metric                | LSB (3,3,2) | Spiral (3,3,2) |
| --------------------- | ----------: | -------------: |
| Cover-Stego MSE       |      0.3550 |         0.3550 |
| Cover-Stego PSNR      |  52.6279 dB |     52.6279 dB |
| Secret-Recovered MSE  |   1153.4543 |      1153.4543 |
| Secret-Recovered PSNR |  17.5108 dB |     17.5108 dB |
| Secret dimensions     |   200 × 200 |      200 × 200 |

The identical values are expected for this implementation because both methods use the same bit allocation and store the same values. The main difference is the order in which the cover pixels are visited.

Further experiments will be needed to determine whether the different spatial distribution provides any practical advantage.

---

# 12. Current Limitations

### Lossy Secret Image Reconstruction

The current `(3,3,2)` implementation stores only 8 bits of information for each 24-bit RGB secret pixel.

Therefore, the recovered secret image is not an exact copy of the original.

### No Encryption Yet

The current image data is not encrypted before embedding.

Encryption will be considered in a later stage of the project.

### PNG Recommended

PNG is preferred because it preserves pixel values.

Lossy formats such as JPEG can modify pixel values during compression and may destroy embedded LSB information.

### Basic Steganography

The current implementation is mainly intended for learning and experimentation. It does not claim to provide protection against advanced steganalysis.

### Visual Cryptography Not Implemented Yet

Visual cryptography is part of the overall project but has not been integrated into the current implementation.

---

# 13. Development Roadmap

### Stage 1 — Basic LSB Steganography

* [x] Encode text into an image
* [x] Decode text from an image
* [x] UTF-8 support
* [x] Capacity validation
* [x] Basic error handling
* [x] Command-line interface
* [x] Automated tests

### Stage 2 — Image Steganography

* [x] Image-to-image steganography
* [x] LSB `(3,3,2)`
* [x] Spiral `(3,3,2)`
* [x] Secret image extraction
* [x] Automated tests
* [x] Basic image quality evaluation

### Stage 3 — Cryptographic Protection

* [ ] Password-based protection
* [ ] Cryptographic encryption
* [ ] Message integrity verification

### Stage 4 — Visual Cryptography

* [ ] Generate visual cryptography shares
* [ ] Reconstruct the secret image
* [ ] Study pixel expansion
* [ ] Evaluate reconstruction quality

### Stage 5 — Integration

* [ ] Combine cryptography and steganography
* [ ] Integrate visual cryptography
* [ ] Improve security
* [ ] Perform final testing
* [ ] Complete project documentation

---

# Project Status

**Project:** Steganography and Visual Cryptography

**Current stage:** Image steganography using LSB and Spiral `(3,3,2)`

**Implementation:** Working

**Automated tests:** 14/14 passing

**Next major stage:** Cryptographic protection and visual cryptography

---

## Academic Project

This project is being developed as part of a final-year academic project. The current focus is on understanding the basic principles of steganography through implementation, testing and comparison of different pixel traversal methods.

Further development will focus on combining steganography with cryptographic techniques and visual cryptography.
