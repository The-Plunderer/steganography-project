# Steganography and Visual Cryptography

A final-year B.Tech Computer Science and Engineering project focused on studying and implementing **Steganography, Cryptography, Adaptive Image Steganography, and Visual Cryptography**.

The project explores multiple techniques for hiding information inside digital images, protecting hidden information using authenticated encryption, and eventually reconstructing secret information through Visual Cryptography.

---

# 1. Project Overview

The project currently implements three major layers:

```text
                    INFORMATION SECURITY
                            |
             +--------------+--------------+
             |                             |
             v                             v
       STEGANOGRAPHY                  CRYPTOGRAPHY
             |                             |
             |                       AES-256-GCM
             |                       PBKDF2-SHA256
             |                             |
             +--------------+--------------+
                            |
                            v
                 SECURE STEGANOGRAPHY
                            |
                            v
                  VISUAL CRYPTOGRAPHY
                     (Next Stage)
```

The current implementation includes:

* Basic text steganography
* UTF-8 text hiding and extraction
* Image-to-image steganography
* LSB `(3,3,2)` image steganography
* Spiral `(3,3,2)` image steganography
* Adaptive `(1 + 4 + 3)` image steganography
* Adaptive Green/Blue channel selection
* Red-channel 2-bit channel indicator
* Image capacity validation
* Unified command-line interface
* Password-protected encrypted image steganography
* AES-256-GCM encryption
* PBKDF2-HMAC-SHA256 key derivation
* Random salt and nonce generation
* Authentication and integrity verification
* Wrong-password detection
* Corrupted encrypted-data detection
* Pixel-perfect recovery of encrypted secret images
* Automated testing using `pytest`
* Git/GitHub-based version control

**Visual Cryptography is the next major implementation stage.**

---

# 2. Project Objectives

The main objectives of this project are to:

* Understand information hiding in digital images.
* Implement basic LSB text steganography.
* Hide and recover text messages.
* Support UTF-8 text messages.
* Hide one image inside another image.
* Implement multiple image traversal techniques.
* Compare sequential and spiral traversal.
* Implement adaptive image steganography.
* Dynamically select between Green and Blue channels.
* Store a channel-selection indicator inside the Red channel.
* Validate image capacity before embedding.
* Study the limitations of reduced-bit image representations.
* Encrypt secret image data before embedding.
* Protect encrypted data against unauthorized modification.
* Detect incorrect passwords.
* Detect corrupted encrypted payloads.
* Combine cryptography and steganography.
* Implement Visual Cryptography.
* Investigate colour Visual Cryptography.
* Evaluate image quality using metrics such as PSNR.
* Study pixel expansion and reconstruction quality.
* Compare security, capacity, visual quality, and computational complexity.

---

# 3. Technology Stack

| Technology        | Purpose                               |
| ----------------- | ------------------------------------- |
| Python 3          | Main programming language             |
| Pillow            | Image loading, processing, and saving |
| NumPy             | Pixel and image-array manipulation    |
| cryptography      | AES-GCM and PBKDF2 implementation     |
| pytest            | Automated testing                     |
| Git               | Version control                       |
| GitHub            | Repository hosting                    |
| Git Bash / UCRT64 | Command-line environment              |
| PyCharm           | Development environment               |

The project dependencies are defined in:

```text
requirements.txt
```

Current dependencies:

```text
Pillow
numpy
pytest
cryptography
```

---

# 4. Repository Structure

The current repository structure is:

```text
steganography-project/
│
├── images/
│   ├── cover.png
│   └── secret.png
│
├── src/
│   ├── adaptive332.py
│   ├── crypto_utils.py
│   ├── decoder.py
│   ├── encoder.py
│   ├── encrypted_steg.py
│   ├── lsb332.py
│   ├── spiral332.py
│   └── steg.py
│
├── tests/
│   ├── test_adaptive332.py
│   ├── test_cli.py
│   ├── test_crypto_utils.py
│   ├── test_encrypted_steg.py
│   ├── test_lsb332.py
│   ├── test_spiral332.py
│   └── test_steganography.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

Generated output images are used during testing and command execution but are not required to be stored in the repository.

---

# 5. Source Files

| File                    | Purpose                                                            |
| ----------------------- | ------------------------------------------------------------------ |
| `src/encoder.py`        | Encodes text messages into images                                  |
| `src/decoder.py`        | Decodes hidden text messages                                       |
| `src/steg.py`           | Unified command-line interface                                     |
| `src/lsb332.py`         | Sequential LSB `(3,3,2)` image steganography                       |
| `src/spiral332.py`      | Spiral `(3,3,2)` image steganography                               |
| `src/adaptive332.py`    | Adaptive Green/Blue image steganography                            |
| `src/crypto_utils.py`   | PBKDF2 key derivation and AES-GCM encryption/decryption            |
| `src/encrypted_steg.py` | Serializes, encrypts, embeds, extracts, and decrypts secret images |

---

# 6. Test Files

| File                           | Purpose                                     |
| ------------------------------ | ------------------------------------------- |
| `tests/test_steganography.py`  | Basic text steganography                    |
| `tests/test_lsb332.py`         | LSB `(3,3,2)` image steganography           |
| `tests/test_spiral332.py`      | Spiral `(3,3,2)` image steganography        |
| `tests/test_adaptive332.py`    | Adaptive332 channel selection and embedding |
| `tests/test_cli.py`            | Unified CLI behaviour                       |
| `tests/test_crypto_utils.py`   | Cryptographic utilities                     |
| `tests/test_encrypted_steg.py` | Encrypted image steganography               |

---

# 7. Input Images

The project currently uses:

```text
images/cover.png
images/secret.png
```

### Cover Image

The cover image is the image into which the secret information is embedded.

```text
Cover Image
    |
    v
Embedding Process
    |
    v
Stego Image
```

### Secret Image

The secret image contains the information that is intended to be hidden.

---

# 8. Basic Text Steganography

The first implementation hides text messages inside RGB images using Least Significant Bit substitution.

An RGB pixel contains:

```text
Pixel
 ├── Red
 ├── Green
 └── Blue
```

Each channel contains 8 bits.

For example:

```text
Original Pixel

Red   = 10110100
Green = 01101011
Blue  = 11001010
```

After embedding a small amount of information:

```text
Modified Pixel

Red   = 10110101
Green = 01101010
Blue  = 11001010
```

Only low-order bits are changed.

The decoder extracts the embedded bits and reconstructs the original text.

The implementation also supports UTF-8 messages.

---

# 9. Text Encoding Workflow

The basic text-steganography pipeline is:

```text
Text Message
     |
     v
UTF-8 Encoding
     |
     v
Binary Data
     |
     v
LSB Embedding
     |
     v
Stego Image
```

The reverse process is:

```text
Stego Image
     |
     v
LSB Extraction
     |
     v
Binary Data
     |
     v
UTF-8 Decoding
     |
     v
Original Message
```

---

# 10. Text Encode

The `encode` command hides a text message inside an image.

Example:

```bash
py src/steg.py encode --image images/cover.png --message "Hello from my project!" --output stego.png
```

A message can also be loaded from a file:

```bash
py src/steg.py encode --image images/cover.png --message-file secret.txt --output stego.png
```

The CLI accepts either:

```text
--message
```

or:

```text
--message-file
```

---

# 11. Text Decode

To extract a hidden text message:

```bash
py src/steg.py decode --image stego.png
```

The decoder reconstructs and prints the hidden message.

---

# 12. Image-to-Image Steganography

The project supports hiding one image inside another.

The general workflow is:

```text
Cover Image
     +
Secret Image
     |
     v
Steganographic Encoding
     |
     v
Stego Image
     |
     v
Steganographic Decoding
     |
     v
Recovered Image
```

Three image-steganography methods are currently implemented:

```text
1. LSB332
2. Spiral332
3. Adaptive332
```

---

# 13. LSB `(3,3,2)` Image Steganography

The LSB332 method allocates the available low-order bits as:

```text
Red   → 3 bits
Green → 3 bits
Blue  → 2 bits

Total → 8 payload bits per cover pixel
```

Conceptually:

```text
Cover Pixel

Red   : XXXXXXXX
Green : XXXXXXXX
Blue  : XXXXXXXX

             |
             v

Embedded Pixel

Red   : XXXXXRRR
Green : XXXXXGGG
Blue  : XXXXXXBB
```

Therefore:

```text
3 + 3 + 2 = 8 bits
```

The method processes cover-image pixels sequentially.

---

# 14. LSB Traversal

The LSB332 implementation processes pixels row by row:

```text
(0,0) → (0,1) → (0,2) → (0,3) → ...
   ↓
next row
   ↓
next row
```

This provides a simple and predictable embedding sequence.

The method is useful as the baseline against which the Spiral332 and Adaptive332 techniques can be compared.

---

# 15. LSB Image Encoding

Example:

```bash
py src/steg.py image-encode --method lsb332 --cover images/cover.png --secret images/secret.png --output output/stego_lsb332.png
```

---

# 16. LSB Image Decoding

Example:

```bash
py src/steg.py image-decode --method lsb332 --image output/stego_lsb332.png --output output/recovered_lsb332.png
```

Because only 8 bits are used to represent a 24-bit RGB secret pixel, the ordinary LSB332 representation is not pixel-perfect.

Conceptually:

```text
Original Secret Pixel
        |
        v
24-bit RGB information
        |
        v
8-bit embedded representation
        |
        v
Recovered Pixel
```

Therefore:

```text
Original Secret Image
        ≠
Recovered LSB332 Image
```

at exact RGB-pixel level.

This is expected behaviour for the reduced-bit representation.

---

# 17. Spiral `(3,3,2)` Image Steganography

Spiral332 uses the same bit allocation as LSB332:

```text
Red   → 3 bits
Green → 3 bits
Blue  → 2 bits
```

However, the major difference is the **pixel traversal order**.

Instead of processing the image sequentially, pixels are traversed in a spiral pattern.

Conceptually:

```text
(0,0) → (0,1) → (0,2)
                   ↓
(1,0) ← (1,1) ← (1,2)
  ↓
(2,0) → (2,1) → (2,2)
```

Therefore:

```text
LSB332
    |
    +--> Sequential traversal
    |
    +--> 3-3-2 allocation


Spiral332
    |
    +--> Spiral traversal
    |
    +--> 3-3-2 allocation
```

The implementation is contained in:

```text
src/spiral332.py
```

---

# 18. Spiral Image Encoding

Example:

```bash
py src/steg.py image-encode --method spiral332 --cover images/cover.png --secret images/secret.png --output output/stego_spiral332.png
```

---

# 19. Spiral Image Decoding

Example:

```bash
py src/steg.py image-decode --method spiral332 --image output/stego_spiral332.png --output output/recovered_spiral332.png
```

---

# 20. Adaptive332 Image Steganography

Adaptive332 is the latest image-steganography method implemented in the project.

Unlike LSB332 and Spiral332, which always use a fixed `3-3-2` allocation, Adaptive332 dynamically determines whether **Green or Blue** should receive the additional payload bit.

The method is designed around the following principle:

```text
Select the lower-intensity channel
between Green and Blue.

        |
        v

Give that channel
the additional payload bit.
```

The method still stores exactly:

```text
8 payload bits per cover pixel
```

---

# 21. Adaptive332 Bit Allocation

Each cover pixel contains:

```text
Red
Green
Blue
```

Adaptive332 allocates the payload as follows.

### Red Channel

Red stores:

```text
1 payload bit
+
2-bit channel indicator
```

Therefore:

```text
Red = 1 payload bit + 2 indicator bits
```

### Green and Blue Channels

One of the two channels receives 4 payload bits.

The other receives 3 payload bits.

Therefore:

```text
Case 1:

Red   → 1 payload bit
Green → 4 payload bits
Blue  → 3 payload bits

Total = 1 + 4 + 3
      = 8 payload bits
```

or:

```text
Case 2:

Red   → 1 payload bit
Green → 3 payload bits
Blue  → 4 payload bits

Total = 1 + 3 + 4
      = 8 payload bits
```

The allocation is therefore:

```text
                Adaptive332
                     |
          +----------+----------+
          |                     |
          v                     v
      Green selected        Blue selected
          |                     |
     R = 1 + indicator     R = 1 + indicator
     G = 4 payload bits    G = 3 payload bits
     B = 3 payload bits    B = 4 payload bits
          |                     |
          +----------+----------+
                     |
                     v
              8 payload bits
```

---

# 22. Adaptive Channel Selection

The Green and Blue channel intensities of the cover pixel are compared.

The implementation uses:

```text
if Green <= Blue:
    select Green
else:
    select Blue
```

Therefore:

```text
Green <= Blue
       |
       v
Green receives 4 bits
Blue receives 3 bits
```

while:

```text
Blue < Green
       |
       v
Blue receives 4 bits
Green receives 3 bits
```

This selection is performed by:

```text
choose_embedding_channel()
```

in:

```text
src/adaptive332.py
```

---

# 23. Red-Channel Indicator

The decoder must know which channel received the additional payload bit.

Adaptive332 therefore stores a 2-bit indicator in the least significant bits of Red.

The indicator values currently defined are:

```text
00 → Green
01 → Blue
```

The remaining values are reserved:

```text
10 → Reserved
11 → Reserved
```

The implementation currently treats reserved values as Green during decoding.

The indicator therefore acts as a small control field:

```text
Red Channel

Bit 7  Bit 6  Bit 5  Bit 4  Bit 3  Bit 2  Bit 1  Bit 0
  |      |      |      |      |      |      |      |
  +------+------+------+------+      +------+------+ 
       Cover information              Indicator

                              +----+
                              |    |
                              v    v
                             00 / 01
                             
                              0 = Green
                              1 = Blue
```

The actual payload bit is stored separately from the indicator.

---

# 24. Adaptive332 Pixel Embedding

For every secret RGB pixel:

```text
Secret Pixel
     |
     +---- Red
     |
     +---- Green
     |
     +---- Blue
```

The Red component contributes its highest-order payload bit:

```text
Secret Red
    |
    v
1 payload bit
```

The Green and Blue components are distributed according to the selected channel.

### Green Selected

```text
Secret Red   → 1 bit
Secret Green → 4 bits
Secret Blue  → 3 bits

Total = 8 bits
```

### Blue Selected

```text
Secret Red   → 1 bit
Secret Green → 3 bits
Secret Blue  → 4 bits

Total = 8 bits
```

---

# 25. Adaptive332 Encoding Logic

The complete pixel-level process is:

```text
                 Cover Pixel
                     |
              +------+------+
              |             |
            Green          Blue
              |             |
              +------+------+
                     |
                     v
             Compare intensity
                     |
          +----------+----------+
          |                     |
       Green <= Blue          Blue < Green
          |                     |
          v                     v
      Select Green          Select Blue
          |                     |
          v                     v
     G = 4 bits             B = 4 bits
     B = 3 bits             G = 3 bits
          |                     |
          +----------+----------+
                     |
                     v
             Store indicator
               inside Red
                     |
                     v
              Adaptive Stego
                  Pixel
```

---

# 26. Adaptive332 Decoding

During decoding, the Red channel is examined first.

```text
Stego Pixel
     |
     v
Read Red indicator
     |
     +----------+----------+
     |                     |
    00                    01
     |                     |
     v                     v
  Green                  Blue
 selected               selected
     |                     |
     v                     v
G = 4, B = 3          G = 3, B = 4
     |                     |
     +----------+----------+
                |
                v
         Recover RGB pixel
```

The decoder uses the indicator to determine how many payload bits must be extracted from Green and Blue.

---

# 27. Adaptive332 Example

Suppose the cover pixel is:

```text
R = 100
G = 50
B = 100
```

Because:

```text
G <= B
50 <= 100
```

Green is selected.

Therefore:

```text
Red   → 1 payload bit + indicator
Green → 4 payload bits
Blue  → 3 payload bits
```

For another cover pixel:

```text
R = 100
G = 150
B = 80
```

Because:

```text
B < G
80 < 150
```

Blue is selected.

Therefore:

```text
Red   → 1 payload bit + indicator
Green → 3 payload bits
Blue  → 4 payload bits
```

This demonstrates the adaptive nature of the algorithm.

---

# 28. Adaptive332 CLI Integration

Adaptive332 is integrated into the unified CLI.

The available image methods are:

```text
lsb332
spiral332
adaptive332
```

The CLI therefore provides:

```bash
py src/steg.py image-encode --method adaptive332 --cover images/cover.png --secret images/secret.png --output output/stego_adaptive332.png
```

Expected output:

```text
Adaptive steganography encoding successful.
Cover image: <width> x <height>
Secret image: <width> x <height>
Output: output/stego_adaptive332.png

Image steganography successful.
Method: adaptive332
Stego image: output/stego_adaptive332.png
```

---

# 29. Adaptive332 Image Decoding

The corresponding decoding command is:

```bash
py src/steg.py image-decode --method adaptive332 --image output/stego_adaptive332.png --output output/recovered_adaptive332.png
```

Expected output:

```text
Adaptive steganography decoding successful.
Recovered secret image: <width> x <height>
Output: output/recovered_adaptive332.png

Image recovery successful.
Method: adaptive332
Recovered image: output/recovered_adaptive332.png
```

---

# 30. Adaptive332 Capacity

Adaptive332 stores:

```text
8 payload bits
```

per cover pixel used for secret image data.

Therefore:

```text
1 cover pixel
       |
       v
8 payload bits
       |
       v
1 byte of secret-image information
```

The first four pixels are reserved for metadata.

Therefore:

```text
Available secret-image pixels
=
Total cover pixels - 4
```

The implementation checks:

```text
Secret pixels <= Cover pixels - 4
```

before encoding.

If the secret image is too large, the encoder raises a capacity error.

---

# 31. Image Metadata

The image-based methods store secret-image dimensions in the first four pixels.

The metadata stores:

```text
Secret Width
Secret Height
```

using the standard `(3,3,2)` representation.

The structure is:

```text
Pixel 0 → Width high byte
Pixel 1 → Width low byte
Pixel 2 → Height high byte
Pixel 3 → Height low byte
```

The remaining pixels contain the secret image payload.

---

# 32. Comparison of Image Steganography Methods

| Feature            | LSB332               | Spiral332           | Adaptive332                |
| ------------------ | -------------------- | ------------------- | -------------------------- |
| Pixel traversal    | Sequential           | Spiral              | Sequential                 |
| Red payload        | 3 bits               | 3 bits              | 1 bit                      |
| Green payload      | 3 bits               | 3 bits              | 3 or 4 bits                |
| Blue payload       | 2 bits               | 2 bits              | 3 or 4 bits                |
| Channel selection  | Fixed                | Fixed               | Adaptive                   |
| Red indicator      | No                   | No                  | Yes                        |
| Payload / pixel    | 8 bits               | 8 bits              | 8 bits                     |
| Metadata           | Yes                  | Yes                 | Yes                        |
| Exact RGB recovery | No                   | No                  | No                         |
| Main idea          | Fixed LSB allocation | Alternate traversal | Dynamic channel allocation |

The three approaches therefore provide different research directions:

```text
LSB332
  |
  +--> Baseline method


Spiral332
  |
  +--> Traversal variation


Adaptive332
  |
  +--> Channel-selection variation
```

---

# 33. Important Note About Normal Image Recovery

The normal image-steganography methods use a reduced representation of each secret RGB pixel.

An original RGB pixel contains:

```text
8 bits Red
8 bits Green
8 bits Blue

Total = 24 bits
```

The current normal image methods embed:

```text
8 payload bits
```

per cover pixel.

Therefore:

```text
24-bit RGB secret pixel
          |
          v
     8-bit payload
          |
          v
   Reduced recovery
```

The recovered image is therefore **not expected to be pixel-perfect**.

This is an intentional property of the current educational implementation and is consistent with the existing LSB332/Spiral332 design.

---

# 34. Image Capacity Command

The CLI also provides an image capacity command:

```bash
py src/steg.py capacity --image images/cover.png
```

The command reports the approximate text capacity of the image.

The current calculation is based on:

```text
width × height × 3 bits
```

followed by conversion from bits to bytes.

---

# 35. Unified CLI

All major functionality is exposed through:

```text
src/steg.py
```

The current command structure includes:

```text
encode
decode
capacity
image-encode
image-decode
secure-image-encode
secure-image-decode
```

To view the available commands:

```bash
py src/steg.py --help
```

For image encoding:

```bash
py src/steg.py image-encode --help
```

For image decoding:

```bash
py src/steg.py image-decode --help
```

---

# 36. Secure Image Steganography

The project also includes an encrypted image-steganography pipeline.

Unlike normal image steganography, the secret image is encrypted before being embedded.

The workflow is:

```text
Secret Image
     |
     v
Serialize Image
     |
     v
Password
     |
     v
PBKDF2-HMAC-SHA256
     |
     v
256-bit AES Key
     |
     v
AES-256-GCM
     |
     v
Encrypted Payload
     |
     v
(3,3,2) Embedding
     |
     v
Encrypted Stego Image
```

This provides two security layers:

```text
Cryptography
     +
Steganography
```

---

# 37. Cryptographic Configuration

The cryptographic implementation is contained in:

```text
src/crypto_utils.py
```

Current configuration:

| Parameter         |               Value |
| ----------------- | ------------------: |
| AES key size      | 256 bits / 32 bytes |
| Salt size         |            16 bytes |
| Nonce size        |            12 bytes |
| PBKDF2 iterations |             600,000 |
| KDF               |  PBKDF2-HMAC-SHA256 |
| Encryption        |             AES-GCM |

---

# 38. PBKDF2-HMAC-SHA256

The user password is not directly used as an AES key.

Instead:

```text
Password
    +
Random Salt
    |
    v
PBKDF2-HMAC-SHA256
    |
    v
32-byte AES Key
```

A random 16-byte salt is generated for every encryption operation.

The current configuration uses:

```text
PBKDF2-HMAC-SHA256
600,000 iterations
32-byte derived key
```

---

# 39. AES-256-GCM

The encrypted implementation uses AES-GCM.

The encryption process is:

```text
Plaintext
    |
    v
AES-256-GCM
    |
    +---- Ciphertext
    |
    +---- Authentication Tag
```

A random 12-byte nonce is generated for every encryption operation.

The encrypted data contains:

```text
salt + nonce + ciphertext
```

The AES-GCM authentication tag is included in the generated ciphertext.

---

# 40. Secure Image Payload

The encrypted image implementation is contained in:

```text
src/encrypted_steg.py
```

The payload contains a header with:

```text
Magic
Version
Payload Length
```

Current values:

```text
Magic   = ESTG
Version = 1
```

Conceptually:

```text
+----------------+---------+----------------+
| Magic (4 byte) | Version | Payload Length |
+----------------+---------+----------------+
|              Encrypted Payload             |
+---------------------------------------------+
```

---

# 41. Secret Image Serialization

Before encryption, the secret image is serialized.

The serialized format contains:

```text
4 bytes  → Magic
1 byte   → Version
4 bytes  → Width
4 bytes  → Height
Remaining → RGB pixel data
```

Current serialization metadata:

```text
Magic   = STG1
Version = 1
```

The secret image is converted to RGB before serialization.

---

# 42. Secure Image Encoding

Example:

```bash
py src/steg.py secure-image-encode --cover images/cover.png --secret images/secret.png --password ProjectPassword123 --output output/encrypted_stego.png
```

The process is:

```text
1. Read cover image
2. Read secret image
3. Serialize secret image
4. Generate random salt
5. Derive AES-256 key
6. Generate random nonce
7. Encrypt using AES-GCM
8. Construct encrypted payload
9. Embed payload using (3,3,2)
10. Save encrypted stego image
```

---

# 43. Secure Image Decoding

Example:

```bash
py src/steg.py secure-image-decode --image output/encrypted_stego.png --password ProjectPassword123 --output output/recovered_secret.png
```

The decoder performs:

```text
1. Read encrypted stego image
2. Extract payload header
3. Validate payload magic
4. Validate payload version
5. Extract encrypted data
6. Read stored salt
7. Read stored nonce
8. Derive AES key
9. Authenticate and decrypt using AES-GCM
10. Validate serialized image
11. Reconstruct RGB image
12. Save recovered image
```

---

# 44. Wrong Password Handling

AES-GCM authentication allows the decoder to detect an incorrect password.

Example:

```bash
py src/steg.py secure-image-decode --image output/encrypted_stego.png --password WrongPassword123 --output output/wrong.png
```

The cryptographic layer reports:

```text
Decryption failed. Incorrect password or corrupted data.
```

The decoder does not produce an unauthenticated decrypted image.

---

# 45. Corrupted Data Detection

The encrypted workflow also detects modification of encrypted data.

If encrypted payload data is changed:

```text
Encrypted Data
      |
      v
Modification
      |
      v
AES-GCM Authentication
      |
      v
Authentication Failure
```

The system reports:

```text
Decryption failed. Incorrect password or corrupted data.
```

If corruption occurs in the image container itself, Pillow may detect the problem before the cryptographic layer is reached.

---

# 46. Pixel-Perfect Secure Image Recovery

Normal image steganography stores a reduced representation of the secret image.

The encrypted workflow is different.

The complete RGB image is serialized before encryption:

```text
Original RGB Image
       |
       v
Complete RGB Bytes
       |
       v
Encryption
       |
       v
Encrypted Payload
       |
       v
Steganographic Embedding
```

After extraction:

```text
Encrypted Payload
       |
       v
Decryption
       |
       v
Original RGB Bytes
       |
       v
Image Reconstruction
```

Therefore, the secure image pipeline can reconstruct the original secret image **pixel-for-pixel**.

This property is verified by the automated test suite.

---

# 47. Normal vs Secure Image Steganography

| Feature                  | Normal Image Steganography | Secure Image Steganography |
| ------------------------ | -------------------------- | -------------------------- |
| Secret                   | Image                      | Image                      |
| Encryption               | No                         | Yes                        |
| AES-GCM                  | No                         | Yes                        |
| PBKDF2                   | No                         | Yes                        |
| Password                 | No                         | Yes                        |
| `(3,3,2)` embedding      | Yes                        | Yes                        |
| Pixel-perfect recovery   | No                         | Yes                        |
| Authentication           | No                         | Yes                        |
| Wrong-password detection | No                         | Yes                        |
| Corruption detection     | Limited                    | Yes                        |

The secure implementation therefore follows:

```text
Secret Image
     |
     v
Encryption
     |
     v
Encrypted Data
     |
     v
Steganographic Embedding
     |
     v
Cover Image
```

This means that even if an attacker discovers that data is hidden inside the image, the original secret is still protected by encryption.

---

# 48. Automated Testing

The project uses `pytest` for automated testing.

Run the complete test suite with:

```bash
py -m pytest -v
```

Current verified result:

```text
42 passed in 7.01s
```

Therefore:

```text
==============================
42 / 42 TESTS PASSING
==============================
```

The current test distribution is:

```text
Adaptive332          10 tests
CLI                   5 tests
Crypto utilities      6 tests
Encrypted steganography
                      6 tests
LSB332                4 tests
Spiral332             6 tests
Basic steganography   4 tests
------------------------------
TOTAL                42 tests
```

---

# 49. Adaptive332 Test Coverage

The Adaptive332 test module validates:

* Green channel selection
* Blue channel selection
* Green indicator generation
* Blue indicator generation
* Adaptive Green embedding
* Adaptive Blue embedding
* Indicator preservation
* Green-channel round trip
* Blue-channel round trip
* Expected reduced-bit reconstruction

Example:

```bash
py -m pytest tests/test_adaptive332.py -v
```

Current result:

```text
10 passed
```

---

# 50. Full Test Command

The complete project can be tested using:

```bash
py -m pytest -v
```

A successful run currently produces:

```text
42 passed in 7.01s
```

This confirms that the addition of Adaptive332 did not break the existing:

```text
Text Steganography
        +
LSB332
        +
Spiral332
        +
CLI
        +
Cryptography
        +
Encrypted Steganography
```

functionality.

---

# 51. Example Adaptive332 Test

A simplified Adaptive332 test scenario is:

```text
Cover:

R = 100
G = 50
B = 100

        |
        v

G <= B

        |
        v

Green selected

        |
        v

Red   → 1 payload bit
Green → 4 payload bits
Blue  → 3 payload bits

        |
        v

Indicator = 00
```

The decoder reads the indicator and reconstructs the corresponding reduced-bit RGB pixel.

---

# 52. Git Workflow

The project uses Git for version control.

Check repository status:

```bash
git status
```

Stage changes:

```bash
git add .
```

Commit changes:

```bash
git commit -m "Update README documentation"
```

Push changes:

```bash
git push origin main
```

The repository is:

```text
The-Plunderer/steganography-project
```

The Adaptive332 implementation was committed as:

```text
769dbad
```

with commit message:

```text
Add adaptive332 image steganography
```

The working tree was verified clean after the implementation was pushed.

---

# 53. Current Implementation Status

## Completed

* [x] Basic text steganography
* [x] UTF-8 text support
* [x] Text decoding
* [x] Text capacity calculation
* [x] Image-to-image steganography
* [x] LSB `(3,3,2)`
* [x] Spiral `(3,3,2)`
* [x] Adaptive332
* [x] Adaptive Green/Blue selection
* [x] Red-channel 2-bit indicator
* [x] Adaptive332 CLI integration
* [x] Image capacity validation
* [x] Unified CLI
* [x] AES-256-GCM encryption
* [x] PBKDF2-HMAC-SHA256
* [x] Random salt generation
* [x] Random nonce generation
* [x] Encrypted image serialization
* [x] Encrypted image embedding
* [x] Encrypted image extraction
* [x] Wrong-password handling
* [x] Corruption detection
* [x] Pixel-perfect encrypted image recovery
* [x] Automated test suite
* [x] **42/42 tests passing**

## Planned

* [ ] Visual Cryptography
* [ ] 2-out-of-2 visual cryptography
* [ ] Multiple visual shares
* [ ] Secret reconstruction from shares
* [ ] Colour Visual Cryptography
* [ ] Threshold schemes
* [ ] Image-quality evaluation
* [ ] PSNR analysis
* [ ] Pixel-expansion analysis
* [ ] Contrast analysis
* [ ] Security evaluation
* [ ] Performance benchmarking
* [ ] Steganalysis evaluation
* [ ] Web interface

---

# 54. Visual Cryptography — Next Major Stage

Visual Cryptography is the next major component of the project.

The intended concept is to divide a secret image into multiple shares.

For a basic 2-out-of-2 scheme:

```text
             Secret Image
                  |
                  v
        Visual Cryptography
                  |
          +-------+-------+
          |               |
          v               v
       Share 1          Share 2
          |               |
          +-------+-------+
                  |
                  v
            Reconstruction
                  |
                  v
             Secret Image
```

The individual shares should not independently reveal the complete secret.

The reconstruction process combines the required shares.

---

# 55. Future Visual Cryptography Research

The Visual Cryptography stage will investigate:

### 2-out-of-2 schemes

```text
Share 1 + Share 2
       |
       v
   Secret Image
```

### k-out-of-n schemes

```text
n generated shares
        |
        v
Any k valid shares
        |
        v
Secret reconstruction
```

### Colour Visual Cryptography

The project will also investigate colour-based visual cryptographic schemes.

Important research parameters include:

* Pixel expansion
* Contrast
* Reconstruction quality
* Computational complexity
* Share size
* Colour preservation
* PSNR
* Security
* Threshold behaviour

---

# 56. Planned Project Evolution

The overall project is progressing through several stages:

```text
Stage 1
Basic Text Steganography
        |
        v
Stage 2
Image Steganography
        |
        v
Stage 3
LSB332
        |
        v
Stage 4
Spiral332
        |
        v
Stage 5
Adaptive332
        |
        v
Stage 6
Cryptography + Steganography
        |
        v
Stage 7
Visual Cryptography
        |
        v
Stage 8
Colour Visual Cryptography
        |
        v
Stage 9
Evaluation and Comparison
```

---

# 57. Project Architecture

The current architecture can be summarized as:

```text
                           CLI
                       src/steg.py
                           |
        +------------------+------------------+
        |                  |                  |
        v                  v                  v
      TEXT               IMAGE             SECURE
   STEGANOGRAPHY      STEGANOGRAPHY     STEGANOGRAPHY
        |                  |                  |
        |          +-------+--------+         |
        |          |       |        |         |
        v          v       v        v         v
   encoder.py   lsb332  spiral   adaptive   encrypted_steg
   decoder.py    .py     332.py    332.py        |
                                             +----+----+
                                             |         |
                                             v         v
                                        crypto_utils  AES-GCM
                                             |
                                             v
                                      PBKDF2-HMAC-SHA256
```

The future architecture will add:

```text
                 Visual Cryptography
                         |
              +----------+----------+
              |                     |
              v                     v
          Share Generation     Reconstruction
              |
              v
       Colour VC / Threshold
```

---

# 58. Security Model

The project uses two complementary security concepts.

## Steganography

Steganography attempts to conceal the existence of information.

```text
"Hide the data."
```

## Cryptography

Cryptography protects the contents of the information.

```text
"Protect the data even if it is discovered."
```

Together:

```text
Secret Image
     |
     v
Encryption
     |
     v
Encrypted Data
     |
     v
Steganographic Embedding
     |
     v
Stego Image
```

Therefore:

```text
Steganography
       +
Cryptography
       =
Layered Protection
```

---

# 59. Research Comparison

The current implementation provides several approaches that can be compared experimentally.

| Method       | Traversal  | Allocation    | Adaptive | Encryption |
| ------------ | ---------- | ------------- | -------- | ---------- |
| LSB332       | Sequential | 3-3-2         | No       | No         |
| Spiral332    | Spiral     | 3-3-2         | No       | No         |
| Adaptive332  | Sequential | 1 + 4/3 + 3/4 | Yes      | No         |
| Secure Image | Sequential | 3-3-2 payload | No       | AES-GCM    |

Potential comparison metrics include:

```text
Capacity
   |
   +-- Payload per pixel

Image Quality
   |
   +-- PSNR
   +-- MSE

Security
   |
   +-- Payload protection
   +-- Authentication
   +-- Steganalysis resistance

Performance
   |
   +-- Encoding time
   +-- Decoding time

Adaptive behaviour
   |
   +-- Green/Blue selection frequency
   +-- Channel modification
```

---

# 60. Limitations

The current implementation is an educational and research prototype.

Important limitations include:

1. Basic steganography does not guarantee resistance against advanced steganalysis.
2. Image transformations such as resizing, recompression, or aggressive editing may destroy embedded data.
3. Normal LSB332, Spiral332, and Adaptive332 use reduced-bit secret representations and therefore do not provide exact RGB recovery.
4. The secure pipeline provides pixel-perfect recovery because the complete image is serialized before encryption.
5. Password security depends on the strength of the password supplied by the user.
6. The current encrypted workflow is intended for project research and demonstration rather than production deployment.
7. Adaptive332 currently reserves indicator values `10` and `11`, but the decoder currently maps them to Green rather than rejecting them.
8. Visual Cryptography has not yet been implemented.
9. Colour Visual Cryptography and threshold schemes are still future work.
10. Steganalysis resistance has not yet been experimentally evaluated.

---

# 61. Current Project Milestone

The current implementation has reached the following milestone:

```text
                 PROJECT STATUS
                       |
       +---------------+---------------+
       |               |               |
       v               v               v
  Steganography   Cryptography      Testing
       |               |               |
       v               v               v
   LSB332          AES-GCM          42/42
   Spiral332       PBKDF2           PASSING
   Adaptive332     Secure Image
       |               |
       +-------+-------+
               |
               v
        Secure Steganography
               |
               v
       Visual Cryptography
          NEXT STAGE
```

---

# 62. Conclusion

The project has progressed from a basic text-steganography implementation into a multi-layer image security system combining **steganography, adaptive information hiding, and cryptography**.

The current system supports:

```text
Text Steganography
        +
Image Steganography
        +
LSB (3,3,2)
        +
Spiral (3,3,2)
        +
Adaptive332
        +
AES-256-GCM
        +
PBKDF2-HMAC-SHA256
        +
Authenticated Encrypted Image Embedding
        +
Automated Testing
```

The Adaptive332 implementation extends the project beyond fixed bit allocation. It dynamically chooses between the Green and Blue channels according to their relative intensity and stores the selected channel using a 2-bit indicator in the Red channel.

The current Adaptive332 design maintains:

```text
1 Red payload bit
+
4 payload bits in selected channel
+
3 payload bits in remaining channel
=
8 payload bits per cover pixel
```

The encrypted image pipeline provides an additional security layer by encrypting the complete secret image before embedding it. AES-256-GCM provides authenticated encryption, while PBKDF2-HMAC-SHA256 derives the encryption key from the user's password.

The implementation has been validated using the complete automated test suite:

```text
42 / 42 tests passing
```

The next major stage is **Visual Cryptography**, where the project will move from hiding information inside a single image toward generating multiple shares and reconstructing a secret through share combination.

The overall direction of the project is therefore:

```text
              INFORMATION HIDING
                       |
              +--------+--------+
              |                 |
              v                 v
       STEGANOGRAPHY       CRYPTOGRAPHY
              |                 |
       +------+-----+           |
       |      |     |           |
      LSB   Spiral Adaptive     |
       |      |     |           |
       +------+-----+           |
              |                 |
              +--------+--------+
                       |
                       v
              SECURE STEGANOGRAPHY
                       |
                       v
              VISUAL CRYPTOGRAPHY
                       |
                       v
            COLOUR VISUAL CRYPTOGRAPHY
                       |
                       v
             COMPLETE RESEARCH SYSTEM
```

---

# 63. Quick Start

Clone the repository:

```bash
git clone https://github.com/The-Plunderer/steganography-project.git
```

Enter the project directory:

```bash
cd steganography-project
```

Install dependencies:

```bash
py -m pip install -r requirements.txt
```

Check the CLI:

```bash
py src/steg.py --help
```

Run all tests:

```bash
py -m pytest -v
```

Expected current result:

```text
42 passed
```

---

# 64. Example Complete Workflow

### Step 1 — Encode text

```bash
py src/steg.py encode --image images/cover.png --message "Hello from Steganography!" --output output/stego_text.png
```

### Step 2 — Decode text

```bash
py src/steg.py decode --image output/stego_text.png
```

### Step 3 — Encode using LSB332

```bash
py src/steg.py image-encode --method lsb332 --cover images/cover.png --secret images/secret.png --output output/stego_lsb332.png
```

### Step 4 — Encode using Spiral332

```bash
py src/steg.py image-encode --method spiral332 --cover images/cover.png --secret images/secret.png --output output/stego_spiral332.png
```

### Step 5 — Encode using Adaptive332

```bash
py src/steg.py image-encode --method adaptive332 --cover images/cover.png --secret images/secret.png --output output/stego_adaptive332.png
```

### Step 6 — Decode Adaptive332

```bash
py src/steg.py image-decode --method adaptive332 --image output/stego_adaptive332.png --output output/recovered_adaptive332.png
```

### Step 7 — Secure image encoding

```bash
py src/steg.py secure-image-encode --cover images/cover.png --secret images/secret.png --password ProjectPassword123 --output output/encrypted_stego.png
```

### Step 8 — Secure image decoding

```bash
py src/steg.py secure-image-decode --image output/encrypted_stego.png --password ProjectPassword123 --output output/recovered_secret.png
```

---

# 65. Development Status

```text
Current Branch:
main

Current Adaptive332 Commit:
769dbad

Current Test Status:
42 / 42 passing

Current Major Stage:
Steganography + Cryptography

Next Major Stage:
Visual Cryptography
```

---

# 66. Future Development Roadmap

```text
[x] Basic text steganography
[x] UTF-8 support
[x] Image steganography
[x] LSB332
[x] Spiral332
[x] Adaptive332
[x] Unified CLI
[x] AES-256-GCM
[x] PBKDF2-HMAC-SHA256
[x] Secure image steganography
[x] Automated testing
[x] 42/42 tests passing

[ ] Visual Cryptography
[ ] 2-out-of-2 shares
[ ] Threshold Visual Cryptography
[ ] Colour Visual Cryptography
[ ] Share reconstruction
[ ] PSNR evaluation
[ ] Pixel-expansion evaluation
[ ] Contrast evaluation
[ ] Steganalysis evaluation
[ ] Performance benchmarking
[ ] Web interface
```

---

# 67. Final Project Direction

The final system is intended to combine:

```text
             ┌──────────────────────┐
             │  INFORMATION HIDING  │
             └──────────┬───────────┘
                        |
             ┌──────────+───────────┐
             |                      |
             v                      v
      Steganography            Cryptography
             |                      |
       +-----+------+          AES-256-GCM
       |     |      |          PBKDF2-SHA256
      LSB  Spiral Adaptive           |
       |     |      |                |
       +-----+------+----------------+
                    |
                    v
          Secure Image System
                    |
                    v
          Visual Cryptography
                    |
                    v
       Colour Visual Cryptography
                    |
                    v
       Evaluation & Comparison
                    |
                    v
           FINAL PROJECT
```

The project therefore evolves from **basic information hiding** toward a complete research-oriented system combining:

**Steganography + Adaptive Steganography + Cryptography + Visual Cryptography.**
