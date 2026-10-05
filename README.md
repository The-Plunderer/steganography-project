# Steganography and Visual Cryptography

This is a final-year project for studying and implementing different techniques used to hide information inside digital images.

The project is being developed step by step. The current implementation includes basic text steganography, image-to-image steganography using LSB `(3,3,2)`, Spiral `(3,3,2)` traversal, and password-protected encrypted image steganography.

The project currently focuses on understanding how information can be hidden inside images, how different pixel traversal methods affect steganographic embedding, and how cryptographic protection can be combined with steganography to protect the hidden information.

Visual cryptography remains a planned stage of the project.

---

## Current Progress

The following implementations are currently working:

* Text steganography using basic LSB substitution
* UTF-8 text hiding and extraction
* Image-to-image steganography using LSB `(3,3,2)`
* Image-to-image steganography using Spiral `(3,3,2)`
* Secret image extraction
* Image capacity validation
* Unified command-line interface
* Password-protected encrypted image steganography
* AES-256-GCM encryption
* PBKDF2-HMAC-SHA256 password-based key derivation
* Random salt generation
* Random nonce generation
* Authentication and integrity verification through AES-GCM
* Wrong-password detection
* Corrupted encrypted data detection
* Pixel-perfect recovery of encrypted secret images
* Automated testing using `pytest`
* 32 automated tests currently passing

---

## Objectives

The main objectives of this project are:

* Understand how information can be hidden inside digital images.
* Implement basic LSB steganography.
* Hide text inside an image.
* Hide one image inside another image.
* Compare normal LSB traversal with Spiral traversal.
* Check whether the secret data fits inside the cover image.
* Extract hidden information from a stego image.
* Measure the quality of stego images.
* Study the limitations of basic steganography.
* Understand password-based cryptographic protection.
* Encrypt secret image data before embedding it into a cover image.
* Protect encrypted data against unauthorized modification.
* Detect incorrect passwords and corrupted encrypted data.
* Combine cryptography and steganography into a single pipeline.
* Implement visual cryptography in a later stage.
* Evaluate the security and limitations of the complete system.

---

# Technology Stack

* **Python 3** — main programming language
* **Pillow** — image loading, processing and saving
* **NumPy** — image array and pixel manipulation
* **cryptography** — AES-GCM encryption and PBKDF2 key derivation
* **pytest** — automated testing
* **Git** — version control
* **GitHub** — source-code hosting
* **Git Bash** — command-line environment
* **PyCharm** — development environment

---

# Project Structure

```text
steganography-project/
│
├── src/
│   ├── encoder.py
│   ├── decoder.py
│   ├── steg.py
│   ├── lsb332.py
│   ├── spiral332.py
│   ├── crypto_utils.py
│   └── encrypted_steg.py
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
│   ├── recovered_spiral332.png
│   ├── cli_encrypted_stego.png
│   ├── cli_encrypted_recovered.png
│   └── cli_corrupted_stego.png
│
├── tests/
│   ├── test_steganography.py
│   ├── test_lsb332.py
│   ├── test_spiral332.py
│   ├── test_cli.py
│   ├── test_crypto_utils.py
│   └── test_encrypted_steg.py
│
├── README.md
├── requirements.txt
├── .gitignore
└── .git/
```

---

## Main Files

| File                           | Purpose                                                         |
| ------------------------------ | --------------------------------------------------------------- |
| `src/encoder.py`               | Hides a text message inside an image                            |
| `src/decoder.py`               | Extracts a hidden text message                                  |
| `src/steg.py`                  | Unified command-line interface                                  |
| `src/lsb332.py`                | Image-to-image LSB `(3,3,2)` implementation                     |
| `src/spiral332.py`             | Image-to-image Spiral `(3,3,2)` implementation                  |
| `src/crypto_utils.py`          | Password-based key derivation and AES-GCM encryption/decryption |
| `src/encrypted_steg.py`        | Encrypts and embeds secret images and extracts/decrypts them    |
| `tests/test_steganography.py`  | Tests for text steganography                                    |
| `tests/test_lsb332.py`         | Tests for LSB `(3,3,2)`                                         |
| `tests/test_spiral332.py`      | Tests for Spiral `(3,3,2)`                                      |
| `tests/test_cli.py`            | Tests for the unified CLI                                       |
| `tests/test_crypto_utils.py`   | Tests for cryptographic functions                               |
| `tests/test_encrypted_steg.py` | Tests for encrypted image steganography                         |
| `images/`                      | Input images used during development                            |
| `output/`                      | Generated stego and recovered images                            |
| `requirements.txt`             | Python dependencies                                             |

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

The implementation also supports UTF-8 text, allowing messages containing characters beyond standard ASCII.

---

# 2. Image-to-Image Steganography

The next stage of the project hides a **secret image inside a cover image**.

The general process is:

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

The current image-to-image implementation provides two traversal methods:

```text
1. LSB (3,3,2)
2. Spiral (3,3,2)
```

Both methods use the same bit allocation but differ in the order in which cover-image pixels are processed.

---

# 3. What Does `(3,3,2)` Mean?

Each RGB pixel contains three 8-bit channels.

For the image-to-image implementation, the least significant bits are divided as follows:

```text
Red   → 3 LSBs
Green → 3 LSBs
Blue  → 2 LSBs

Total = 3 + 3 + 2
      = 8 bits
```

Therefore, one cover pixel provides **8 bits of storage**.

The secret pixel is reduced to an 8-bit representation:

```text
Secret Red   → 3 most significant bits
Secret Green → 3 most significant bits
Secret Blue  → 2 most significant bits
```

These bits are then placed into the corresponding LSB positions of the cover pixel.

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

Here:

```text
R = secret red information
G = secret green information
B = secret blue information
```

---

# 4. Why Is the Recovered Image Not Exactly the Same?

A standard RGB pixel contains:

```text
Red   = 8 bits
Green = 8 bits
Blue  = 8 bits

Total = 24 bits
```

However, the `(3,3,2)` method stores only:

```text
Red   = 3 bits
Green = 3 bits
Blue  = 2 bits

Total = 8 bits
```

Therefore, the recovered secret image is a **quantized representation** of the original secret image.

This means the normal `(3,3,2)` implementation is intentionally lossy with respect to the secret image.

Consequently:

```text
Original secret image
        ≠
Recovered secret image
```

in terms of exact pixel values.

This is an expected characteristic of the current implementation.

---

# 5. LSB `(3,3,2)` Implementation

The LSB implementation processes cover-image pixels in normal row-by-row order.

Conceptually:

```text
(0,0) → (0,1) → (0,2) → ...
   ↓
next row
   ↓
next row
```

The first pixels are used for storing metadata such as the secret image dimensions.

The remaining pixels are used for secret image data.

During extraction, the stored dimensions allow the decoder to reconstruct the secret image with the correct width and height.

---

# 6. Spiral `(3,3,2)` Implementation

The Spiral implementation uses the same `(3,3,2)` bit allocation but changes the order in which cover pixels are processed.

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

The same coordinate sequence is used during decoding.

The difference between LSB and Spiral is therefore mainly:

```text
LSB:
Sequential row-by-row traversal

Spiral:
Spiral traversal
```

The bit allocation remains:

```text
3 bits Red
3 bits Green
2 bits Blue
```

---

# 7. Cryptographic Protection

The project has now been extended to provide cryptographic protection for secret images before they are embedded into the cover image.

The secure pipeline is:

```text
Secret Image
     │
     ▼
Serialize Image Data
     │
     ▼
Password
     │
     ▼
PBKDF2-HMAC-SHA256
     │
     ▼
256-bit Encryption Key
     │
     ▼
AES-256-GCM
     │
     ▼
Encrypted Payload
     │
     ▼
Embed into Cover Image
     │
     ▼
Encrypted Stego Image
```

During extraction, the reverse process is performed:

```text
Encrypted Stego Image
          │
          ▼
     Extract Payload
          │
          ▼
      Read Salt
          │
          ▼
      Read Nonce
          │
          ▼
       Password
          │
          ▼
PBKDF2-HMAC-SHA256
          │
          ▼
     256-bit Key
          │
          ▼
       AES-GCM
          │
          ▼
    Decrypted Image
```

---

# 8. Password-Based Key Derivation

The project does not directly use the user's password as an AES key.

Instead, a cryptographic key is derived from the password using:

```text
PBKDF2-HMAC-SHA256
```

The current cryptographic configuration is:

```text
Key size            = 256 bits
Key size            = 32 bytes

Salt size           = 16 bytes

PBKDF2 iterations   = 600,000

Hash function       = SHA-256
```

The salt is generated randomly for each encryption operation.

Conceptually:

```text
Password + Random Salt
          │
          ▼
PBKDF2-HMAC-SHA256
          │
          ▼
     AES-256 Key
```

The random salt prevents the same password from producing the same derived key across independent encryption operations.

---

# 9. AES-GCM Encryption

The encrypted image implementation uses:

```text
AES-GCM
```

with a 256-bit key.

AES-GCM provides both:

```text
Confidentiality
+
Integrity / Authentication
```

The current nonce size is:

```text
12 bytes
```

The encryption process therefore uses:

```text
Password
   │
   ▼
PBKDF2
   │
   ▼
AES-256 Key
   │
   ├── Random Nonce
   │
   ▼
AES-GCM Encryption
   │
   ▼
Encrypted Payload + Authentication Tag
```

The authentication mechanism is important because the system must detect not only incorrect passwords but also modified or corrupted encrypted data.

---

# 10. Cryptographic Utility Module

The cryptographic functions are implemented in:

```text
src/crypto_utils.py
```

The module is responsible for:

* Generating random salts.
* Generating random nonces.
* Deriving AES keys from passwords.
* Encrypting data using AES-GCM.
* Decrypting authenticated encrypted data.
* Detecting incorrect passwords.
* Detecting corrupted or modified encrypted data.
* Validating cryptographic parameters.

The main configuration constants are:

```text
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32
PBKDF2_ITERATIONS = 600,000
```

---

# 11. Encrypted Image Steganography

The encrypted image implementation is located in:

```text
src/encrypted_steg.py
```

It combines:

```text
Image Serialization
        +
Password-Based Encryption
        +
Image Steganography
```

The complete process is:

```text
                Secret Image
                     │
                     ▼
             Image Serialization
                     │
                     ▼
                  AES-GCM
                     ▲
                     │
                  Password
                     │
                     ▼
             Encrypted Payload
                     │
                     ▼
              Image Embedding
                     ▲
                     │
               Cover Image
                     │
                     ▼
             Encrypted Stego
```

This provides an additional layer of protection compared with ordinary image steganography.

Without encryption, an attacker who successfully extracts the hidden data may be able to reconstruct the secret.

With encryption:

```text
Extracted Payload
       │
       ▼
Encrypted Data
       │
       ▼
Correct Password Required
       │
       ▼
Original Secret Image
```

---

# 12. Running the Project

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

The current dependencies are:

```text
Pillow
numpy
pytest
cryptography
```

---

# 13. Command-Line Interface

The project provides a unified command-line interface through:

```bash
.venv/Scripts/python.exe src/steg.py
```

Display the available commands:

```bash
.venv/Scripts/python.exe src/steg.py --help
```

The current CLI provides:

```text
encode
decode
capacity
image-encode
image-decode
secure-image-encode
secure-image-decode
```

The CLI therefore supports both normal and encrypted image steganography.

---

# 14. Text Steganography Commands

## Encode a Message

```bash
.venv/Scripts/python.exe src/steg.py encode --image images/cover.png --output output/stego.png --message "Hello from my project!"
```

## Decode a Message

```bash
.venv/Scripts/python.exe src/steg.py decode --image output/stego.png
```

## Encode a Message from a Text File

```bash
.venv/Scripts/python.exe src/steg.py encode --image images/cover.png --output output/stego.png --message-file secret.txt
```

## Show Text Capacity

```bash
.venv/Scripts/python.exe src/steg.py capacity --image images/cover.png
```

---

# 15. Normal Image Steganography Commands

The image-to-image implementations are accessed through the same CLI.

## LSB `(3,3,2)`

Encode:

```bash
.venv/Scripts/python.exe src/steg.py image-encode --method lsb332 --cover images/cover.png --secret images/secret.png --output output/stego_lsb332.png
```

Decode:

```bash
.venv/Scripts/python.exe src/steg.py image-decode --method lsb332 --image output/stego_lsb332.png --output output/recovered_lsb332.png
```

## Spiral `(3,3,2)`

Encode:

```bash
.venv/Scripts/python.exe src/steg.py image-encode --method spiral332 --cover images/cover.png --secret images/secret.png --output output/stego_spiral332.png
```

Decode:

```bash
.venv/Scripts/python.exe src/steg.py image-decode --method spiral332 --image output/stego_spiral332.png --output output/recovered_spiral332.png
```

The `--method` option currently supports:

```text
lsb332
spiral332
```

---

# 16. Secure Image Steganography Commands

The secure image functionality provides encryption before the secret image is embedded.

## Secure Image Encode

The following command encrypts the secret image and embeds it into the cover image:

```bash
.venv/Scripts/python.exe src/steg.py secure-image-encode --cover images/cover.png --secret images/secret.png --password ProjectPassword123 --output output/cli_encrypted_stego.png
```

A successful operation produces:

```text
Encrypted image steganography successful.
Stego image: output/cli_encrypted_stego.png
```

---

## Secure Image Decode

The following command extracts and decrypts the hidden image:

```bash
.venv/Scripts/python.exe src/steg.py secure-image-decode --image output/cli_encrypted_stego.png --password ProjectPassword123 --output output/cli_encrypted_recovered.png
```

A successful operation produces:

```text
Encrypted image recovery successful.
Recovered image: output/cli_encrypted_recovered.png
```

---

# 17. Wrong Password Handling

The encrypted image pipeline verifies the supplied password during decryption.

For example:

```bash
.venv/Scripts/python.exe src/steg.py secure-image-decode --image output/cli_encrypted_stego.png --password WrongPassword123 --output output/wrong_password_recovered.png
```

The system correctly rejects the operation:

```text
Error: Decryption failed. Incorrect password or corrupted data.
```

This demonstrates that an incorrect password cannot successfully decrypt the protected secret image.

---

# 18. Corrupted Data Handling

The encrypted stego image was also tested against deliberate modification.

A copy of the encrypted stego image can be created:

```bash
cp output/cli_encrypted_stego.png output/cli_corrupted_stego.png
```

A byte can then be modified:

```bash
.venv/Scripts/python.exe -c "from pathlib import Path; p=Path('output/cli_corrupted_stego.png'); data=bytearray(p.read_bytes()); data[-20] ^= 1; p.write_bytes(data); print('Corrupted stego image created.')"
```

The corrupted image is then tested:

```bash
.venv/Scripts/python.exe src/steg.py secure-image-decode --image output/cli_corrupted_stego.png --password ProjectPassword123 --output output/corrupted_recovered.png
```

The system detects the corrupted image data.

Depending on where the corruption occurs, the image container itself may reject the modified file before the encrypted payload can be processed.

An observed result was:

```text
Error: broken data stream when reading image file
```

This demonstrates that the implementation does not silently accept damaged image data.

---

# 19. Pixel-Perfect Encrypted Image Recovery

Unlike the normal `(3,3,2)` image steganography implementation, the encrypted image pipeline preserves the original secret image data.

The following comparison was performed:

```bash
.venv/Scripts/python.exe -c "from PIL import Image; import numpy as np; a=np.array(Image.open('images/secret.png').convert('RGB')); b=np.array(Image.open('output/cli_encrypted_recovered.png').convert('RGB')); print('Pixel-perfect:', np.array_equal(a,b)); print('Different pixels:', np.count_nonzero(np.any(a!=b,axis=2)))"
```

The result was:

```text
Pixel-perfect: True
Different pixels: 0
```

Therefore:

```text
Original Secret Image
        ==
Recovered Secret Image
```

at the pixel level.

This is an important difference from the normal `(3,3,2)` implementation.

---

# 20. Normal vs Encrypted Image Steganography

The project now provides two different approaches.

| Feature                   | Normal `(3,3,2)` | Encrypted Image |
| ------------------------- | ---------------- | --------------- |
| Secret image hiding       | Yes              | Yes             |
| LSB-based embedding       | Yes              | Yes             |
| Image encryption          | No               | Yes             |
| Password required         | No               | Yes             |
| AES-GCM                   | No               | Yes             |
| PBKDF2                    | No               | Yes             |
| Authentication            | No               | Yes             |
| Wrong-password detection  | No               | Yes             |
| Pixel-perfect recovery    | No               | Yes             |
| Secret image quantization | Yes              | No              |
| Integrity protection      | Limited          | Cryptographic   |

The normal `(3,3,2)` implementation is primarily useful for studying image steganography and bit-level embedding.

The encrypted implementation adds cryptographic protection before embedding the secret image.

---

# 21. Capacity

For the normal `(3,3,2)` implementation, approximately one cover pixel is used to store one 8-bit representation of one secret pixel.

Therefore:

```text
Maximum secret pixels
≈ Cover width × Cover height - metadata pixels
```

The current implementation reserves four pixels for storing secret image dimensions.

For example, with a 1200 × 1200 cover image:

```text
Total cover pixels = 1200 × 1200
                   = 1,440,000 pixels

Reserved pixels    = 4

Available pixels   = 1,439,996
```

A 200 × 200 secret image contains:

```text
200 × 200
= 40,000 pixels
```

Therefore, the example secret image fits comfortably inside the cover image.

The encrypted implementation must also account for encryption metadata and encrypted payload overhead when determining whether a secret image can fit into the cover image.

---

# 22. Image Quality Results

A 1200 × 1200 cover image and a 200 × 200 secret image were used for the original `(3,3,2)` implementation.

## Cover Image vs Stego Image

```text
MSE  = 0.3550
PSNR = 52.6279 dB
```

The high PSNR indicates that the changes made to the cover image are relatively small.

---

## Secret Image vs Recovered Image

For the normal `(3,3,2)` implementation:

```text
MSE  = 1153.4543
PSNR = 17.5108 dB
```

The lower PSNR is mainly caused by the `(3,3,2)` quantization of the secret image.

This is different from the cover-to-stego measurement.

The first measurement evaluates how much the cover image changes after embedding.

The second measurement evaluates how closely the recovered secret image resembles the original secret image.

---

# 23. LSB vs Spiral

Both normal implementations use:

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

The identical values are expected because both methods use the same bit allocation and store the same information.

The main difference is the spatial order in which cover pixels are visited.

Further experiments are required to determine whether Spiral traversal provides practical advantages against statistical or spatial steganalysis.

---

# 24. Testing

The project uses `pytest` for automated testing.

Run all tests with:

```bash
.venv/Scripts/python.exe -m pytest -q
```

The current test result is:

```text
32 passed in approximately 7 seconds
```

The test suite covers:

```text
Basic text encoding and decoding
Unicode message handling
Missing image handling
Oversized text message handling

LSB (3,3,2) encoding and decoding
LSB image dimensions
LSB oversized secret image
LSB output generation

Spiral coordinate generation
Spiral coordinate coverage
Spiral (3,3,2) encoding and decoding
Spiral image dimensions
Spiral oversized secret image
Spiral output generation

CLI help
CLI LSB (3,3,2) encode/decode
CLI Spiral (3,3,2) encode/decode

Cryptographic key derivation
Password validation
Salt validation
Encryption/decryption
AES-GCM authentication
Incorrect password handling

Encrypted image embedding
Encrypted image extraction
Encrypted image encode/decode pipeline
Encrypted image pixel-perfect recovery
CLI secure image encode/decode
CLI wrong-password handling
```

The complete test suite currently reports:

```text
32 passed
```

---

# 25. Example Secure Pipeline

The complete encrypted image workflow can be represented as:

```text
             ┌─────────────────┐
             │   Secret Image  │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Serialize Image │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │     Password    │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │     PBKDF2      │
             │  HMAC-SHA256    │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │   AES-256-GCM   │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Encrypted Image │
             │     Payload     │
             └────────┬────────┘
                      │
                      ▼
        ┌───────────────────────────┐
        │     Cover Image           │
        │            +              │
        │   Encrypted Payload       │
        └─────────────┬─────────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Encrypted Stego │
             │      Image      │
             └─────────────────┘
```

The recovery process reverses the operation:

```text
Encrypted Stego Image
          │
          ▼
   Extract Payload
          │
          ▼
   Recover Salt/Nonce
          │
          ▼
       Password
          │
          ▼
       PBKDF2
          │
          ▼
     AES-256-GCM
          │
          ▼
    Authentication
          │
          ▼
    Decrypted Data
          │
          ▼
   Reconstruct Image
          │
          ▼
   Original Secret
```

---

# 26. Security Properties

The current encrypted implementation provides several important security properties.

## Confidentiality

The secret image is encrypted before being embedded.

Therefore, extracting the hidden payload does not directly reveal the original image.

---

## Password-Based Protection

The encryption key is derived from the password using:

```text
PBKDF2-HMAC-SHA256
```

The password itself is not used directly as the AES key.

---

## Random Salt

A random salt is used during key derivation.

This makes independent encryption operations produce independent derived keys even when the same password is used.

---

## Random Nonce

AES-GCM uses a randomly generated nonce.

The current nonce size is:

```text
12 bytes
```

---

## Integrity and Authentication

AES-GCM provides an authentication tag.

If the encrypted payload is modified, authentication can fail during decryption.

This prevents the system from treating altered encrypted data as valid plaintext.

---

## Incorrect Password Detection

A wrong password results in unsuccessful authentication/decryption.

The CLI reports:

```text
Error: Decryption failed. Incorrect password or corrupted data.
```

---

# 27. Current Limitations

## Lossy Normal Secret Image Reconstruction

The normal `(3,3,2)` method stores only 8 bits of information for each 24-bit RGB secret pixel.

Therefore, normal image extraction is lossy.

---

## Encryption Does Not Automatically Improve Steganographic Detectability

Encryption protects the **content** of the hidden data.

It does not automatically make the existence of the hidden data undetectable.

Steganalysis remains a separate security problem.

---

## PNG Recommended

PNG is preferred because it preserves pixel values.

Lossy formats such as JPEG may modify pixel values during compression and can destroy LSB-based embedded information.

---

## Basic Steganography

The current implementation is primarily intended for learning, experimentation and academic research.

It does not claim to provide protection against advanced steganalysis techniques.

---

## Password Management

The password is required for successful decryption.

If the password is lost, the encrypted secret image cannot be recovered through the implemented decryption pipeline.

Passwords should therefore be handled securely and should not be hard-coded in production applications.

---

## Visual Cryptography Not Yet Integrated

Visual cryptography is part of the overall project but has not yet been integrated into the current implementation.

---

# 28. Development Roadmap

## Stage 1 — Basic LSB Steganography

* [x] Encode text into an image
* [x] Decode text from an image
* [x] UTF-8 support
* [x] Capacity validation
* [x] Basic error handling
* [x] Command-line interface
* [x] Automated tests

---

## Stage 2 — Image Steganography

* [x] Image-to-image steganography
* [x] LSB `(3,3,2)`
* [x] Spiral `(3,3,2)`
* [x] Secret image extraction
* [x] Automated tests
* [x] Basic image quality evaluation

---

## Stage 3 — Cryptographic Protection

* [x] Password-based protection
* [x] PBKDF2-HMAC-SHA256 key derivation
* [x] AES-256-GCM encryption
* [x] Random salt generation
* [x] Random nonce generation
* [x] Authentication and integrity verification
* [x] Wrong-password detection
* [x] Encrypted image embedding
* [x] Encrypted image extraction
* [x] Pixel-perfect encrypted image recovery
* [x] CLI support
* [x] Automated tests

---

## Stage 4 — Visual Cryptography

* [ ] Generate visual cryptography shares
* [ ] Reconstruct the secret image
* [ ] Study pixel expansion
* [ ] Evaluate reconstruction quality
* [ ] Compare different visual cryptography schemes

---

## Stage 5 — Integration

* [ ] Combine cryptography and steganography with visual cryptography
* [ ] Integrate visual cryptography into the CLI
* [ ] Compare normal and encrypted steganography
* [ ] Evaluate security properties
* [ ] Perform advanced image-quality analysis
* [ ] Study resistance against basic steganalysis
* [ ] Perform final testing
* [ ] Complete final project documentation

---

# 29. Git and Version Control

Git is used to track the development of the project.

The current cryptographic implementation was committed using:

```bash
git commit -m "Add encrypted image steganography"
```

The commit was successfully pushed to the GitHub repository.

Repository:

```text
https://github.com/The-Plunderer/steganography-project
```

The project currently uses the `main` branch.

---

# 30. Verification Before Commit

Before committing the encrypted steganography implementation, the following checks were performed.

## Staged Difference Check

```bash
git diff --cached --check
```

Result:

```text
No formatting errors reported.
```

## Test Suite

```bash
.venv/Scripts/python.exe -m pytest -q
```

Result:

```text
32 passed
```

## Git Statistics

The encrypted steganography implementation introduced approximately:

```text
928 insertions
90 deletions
```

across the updated project files.

The major additions were:

```text
src/crypto_utils.py
src/encrypted_steg.py
tests/test_crypto_utils.py
tests/test_encrypted_steg.py
```

---

# Project Status

**Project:** Steganography and Visual Cryptography

**Current stage:** Cryptographically protected image steganography

**Basic text steganography:** Working

**LSB `(3,3,2)`:** Working

**Spiral `(3,3,2)`:** Working

**Encrypted image steganography:** Working

**AES-256-GCM:** Implemented

**PBKDF2-HMAC-SHA256:** Implemented

**Wrong-password detection:** Working

**Encrypted image integrity verification:** Implemented

**Pixel-perfect encrypted image recovery:** Verified

**CLI:** Working

**Automated tests:** 32/32 passing

**Visual cryptography:** Planned

**Final integration:** In progress

---

## Academic Project

This project is being developed as part of a final-year academic project.

The implementation is being developed incrementally to study:

```text
Basic Steganography
        ↓
Image Steganography
        ↓
Alternative Pixel Traversal
        ↓
Cryptographic Protection
        ↓
Encrypted Steganography
        ↓
Visual Cryptography
        ↓
Integrated Secure Information Hiding System
```

The current implementation demonstrates how cryptography can be combined with image steganography to provide an additional layer of protection for hidden information.

The next major stage of development is the implementation and evaluation of **Visual Cryptography**, followed by integration of steganography, cryptography and visual cryptography into a unified academic project.
