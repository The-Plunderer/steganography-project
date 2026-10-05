# Steganography and Visual Cryptography

A final-year project for studying and implementing techniques used to hide and protect information inside digital images.

The current implementation covers:

* Basic text steganography using LSB substitution
* UTF-8 text hiding and extraction
* Image-to-image steganography using LSB `(3,3,2)`
* Image-to-image steganography using Spiral `(3,3,2)`
* Image capacity validation
* A unified command-line interface
* Password-protected encrypted image steganography
* AES-256-GCM encryption
* PBKDF2-HMAC-SHA256 password-based key derivation
* Random salt and nonce generation
* Authentication and integrity verification
* Wrong-password detection
* Corrupted encrypted-data detection
* Pixel-perfect recovery of encrypted secret images
* Automated testing with `pytest`

Visual Cryptography is planned as the next major stage of the project.

---

# 1. Project Objectives

The main objectives of this project are to:

* Understand how information can be hidden inside digital images.
* Implement basic LSB text steganography.
* Hide and recover text messages.
* Hide one image inside another image.
* Implement multiple pixel traversal methods.
* Compare normal LSB traversal with Spiral traversal.
* Check image capacity before embedding data.
* Study the limitations of basic image steganography.
* Understand password-based cryptographic protection.
* Encrypt secret image data before embedding it.
* Protect encrypted data against unauthorized modification.
* Detect incorrect passwords and corrupted encrypted data.
* Combine cryptography and steganography into a single pipeline.
* Implement Visual Cryptography in a later stage.
* Evaluate the security, quality, and limitations of the complete system.

---

# 2. Technology Stack

| Technology   | Purpose                               |
| ------------ | ------------------------------------- |
| Python 3     | Main programming language             |
| Pillow       | Image loading, processing, and saving |
| NumPy        | Image-array and pixel manipulation    |
| cryptography | AES-GCM and PBKDF2 implementation     |
| pytest       | Automated testing                     |
| Git          | Version control                       |
| GitHub       | Repository hosting                    |
| Git Bash     | Command-line environment              |
| PyCharm      | Development environment               |

The Python dependencies are defined in:

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

# 3. Current Repository Structure

The current repository structure is:

```text
steganography-project/
│
├── images/
│   ├── cover.png
│   └── secret.png
│
├── src/
│   ├── crypto_utils.py
│   ├── decoder.py
│   ├── encoder.py
│   ├── encrypted_steg.py
│   ├── lsb332.py
│   ├── spiral332.py
│   └── steg.py
│
├── tests/
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

Generated output images are used during testing and command execution but are **not currently stored in a committed `output/` directory**.

---

# 4. Source Files

| File                    | Purpose                                                            |
| ----------------------- | ------------------------------------------------------------------ |
| `src/encoder.py`        | Encodes text messages into images                                  |
| `src/decoder.py`        | Decodes hidden text messages                                       |
| `src/steg.py`           | Unified command-line interface                                     |
| `src/lsb332.py`         | Image-to-image LSB `(3,3,2)` implementation                        |
| `src/spiral332.py`      | Image-to-image Spiral `(3,3,2)` implementation                     |
| `src/crypto_utils.py`   | PBKDF2 key derivation and AES-GCM encryption/decryption            |
| `src/encrypted_steg.py` | Serializes, encrypts, embeds, extracts, and decrypts secret images |

---

# 5. Test Files

| File                           | Purpose                                    |
| ------------------------------ | ------------------------------------------ |
| `tests/test_steganography.py`  | Tests basic text steganography             |
| `tests/test_lsb332.py`         | Tests LSB `(3,3,2)` image steganography    |
| `tests/test_spiral332.py`      | Tests Spiral `(3,3,2)` image steganography |
| `tests/test_cli.py`            | Tests the unified command-line interface   |
| `tests/test_crypto_utils.py`   | Tests cryptographic utilities              |
| `tests/test_encrypted_steg.py` | Tests encrypted image steganography        |

---

# 6. Input Images

The repository currently contains two input images:

```text
images/cover.png
images/secret.png
```

### `cover.png`

The cover image is the image into which data is embedded.

### `secret.png`

The secret image is the image or information being hidden.

---

# 7. Basic Text Steganography

The first implementation hides a text message inside an RGB image.

An RGB pixel contains:

```text
Pixel
 ├── Red
 ├── Green
 └── Blue
```

Each channel contains 8 bits.

The basic text steganography implementation modifies the least significant bits of the image channels to store the message.

Conceptually:

```text
Original Pixel

Red   = 10110100
Green = 01101011
Blue  = 11001010


After embedding

Red   = 10110101
Green = 01101010
Blue  = 11001010
```

Only the least significant bits are modified, so the visual difference is generally very small.

The decoder extracts the stored bits and reconstructs the original message.

The implementation also supports UTF-8 text.

---

# 8. Image-to-Image Steganography

The project also supports hiding one image inside another.

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

Two image-embedding methods are currently implemented:

```text
1. LSB (3,3,2)
2. Spiral (3,3,2)
```

---

# 9. LSB `(3,3,2)`

The `(3,3,2)` scheme allocates the least significant bits of each RGB channel as follows:

```text
Red   → 3 bits
Green → 3 bits
Blue  → 2 bits

Total → 8 bits per cover pixel
```

Conceptually:

```text
Cover Pixel

Red   : XXXXXXXX
Green : XXXXXXXX
Blue  : XXXXXXXX

             ↓

Embedded Pixel

Red   : XXXXXRRR
Green : XXXXXGGG
Blue  : XXXXXXBB
```

where:

```text
R = secret-image information
G = secret-image information
B = secret-image information
```

The current implementation uses this 3-3-2 allocation for image-to-image embedding.

---

# 10. LSB Traversal

The LSB implementation processes pixels in normal row-by-row order.

Conceptually:

```text
(0,0) → (0,1) → (0,2) → ...
   ↓
next row
   ↓
next row
```

The secret image's dimensions and pixel information are encoded according to the implementation in `src/lsb332.py`.

During decoding, the stored information is used to reconstruct the secret image.

Because the `(3,3,2)` representation stores only 8 bits per secret pixel instead of the original 24-bit RGB representation, ordinary image recovery is not pixel-perfect.

Therefore:

```text
Original Secret Image
        ≠
Recovered LSB Image
```

at the exact RGB-pixel level.

---

# 11. Spiral `(3,3,2)`

The Spiral implementation uses the same 3-3-2 bit allocation but changes the order in which cover-image pixels are processed.

For example, a small image can be traversed conceptually as:

```text
(0,0) → (0,1) → (0,2)
                   ↓
(1,0) ← (1,1) ← (1,2)
  ↓
(2,0) → (2,1) → (2,2)
```

The exact traversal is implemented in:

```text
src/spiral332.py
```

The important difference is:

```text
LSB332
→ sequential pixel traversal

Spiral332
→ spiral pixel traversal
```

The bit allocation remains:

```text
Red   → 3 bits
Green → 3 bits
Blue  → 2 bits
```

---

# 12. Unified CLI

All major functionality is exposed through:

```text
src/steg.py
```

The CLI currently provides these commands:

```text
encode
decode
capacity
image-encode
image-decode
secure-image-encode
secure-image-decode
```

To display the available commands:

```bash
python src/steg.py --help
```

If using the project's virtual environment:

```bash
.venv/Scripts/python.exe src/steg.py --help
```

---

# 13. Text Encode

The `encode` command hides a text message inside an image.

### Using a direct message

```bash
.venv/Scripts/python.exe src/steg.py encode --image images/cover.png --message "Hello from my project!" --output stego.png
```

The arguments are:

```text
--image
    Path to the cover image

--message
    Text message to hide

--output
    Path for the generated stego image
```

The command prints:

```text
Message encoded successfully.
Stego image: stego.png
```

---

# 14. Text Encode Using a File

A message can also be read from a text file.

```bash
.venv/Scripts/python.exe src/steg.py encode --image images/cover.png --message-file secret.txt --output stego.png
```

The CLI requires either:

```text
--message
```

or:

```text
--message-file
```

but not both.

---

# 15. Text Decode

The `decode` command extracts a hidden text message.

```bash
.venv/Scripts/python.exe src/steg.py decode --image stego.png
```

The CLI prints:

```text
Decoded message:
<hidden message>
```

---

# 16. Image Capacity

The `capacity` command reports the approximate text capacity of an image.

```bash
.venv/Scripts/python.exe src/steg.py capacity --image images/cover.png
```

The command reports:

```text
Image size: <width> x <height>
Approximate capacity: <bytes> bytes
```

The current calculation is based on:

```text
width × height × 3 bits
```

followed by conversion from bits to bytes.

---

# 17. Image Encode

The `image-encode` command hides one image inside another.

It requires:

```text
--method
--cover
--secret
--output
```

The available methods are:

```text
lsb332
spiral332
```

---

## 17.1 LSB Image Encoding

```bash
.venv/Scripts/python.exe src/steg.py image-encode --method lsb332 --cover images/cover.png --secret images/secret.png --output stego_lsb332.png
```

Expected output:

```text
Image steganography successful.
Method: lsb332
Stego image: stego_lsb332.png
```

---

## 17.2 Spiral Image Encoding

```bash
.venv/Scripts/python.exe src/steg.py image-encode --method spiral332 --cover images/cover.png --secret images/secret.png --output stego_spiral332.png
```

Expected output:

```text
Image steganography successful.
Method: spiral332
Stego image: stego_spiral332.png
```

---

# 18. Image Decode

The `image-decode` command recovers an image hidden using one of the image-steganography methods.

It requires:

```text
--method
--image
--output
```

---

## 18.1 LSB Image Decoding

```bash
.venv/Scripts/python.exe src/steg.py image-decode --method lsb332 --image stego_lsb332.png --output recovered_lsb332.png
```

---

## 18.2 Spiral Image Decoding

```bash
.venv/Scripts/python.exe src/steg.py image-decode --method spiral332 --image stego_spiral332.png --output recovered_spiral332.png
```

---

# 19. Secure Image Steganography

The project now includes a separate encrypted image-steganography pipeline.

The secure workflow is:

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

This differs from normal image steganography because the secret image is encrypted **before** it is embedded.

---

# 20. Cryptographic Configuration

The cryptographic implementation is contained in:

```text
src/crypto_utils.py
```

The current constants are:

```text
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32
PBKDF2_ITERATIONS = 600_000
```

Therefore:

| Parameter         |       Current value |
| ----------------- | ------------------: |
| AES key           | 256 bits / 32 bytes |
| Salt              |            16 bytes |
| Nonce             |            12 bytes |
| PBKDF2 iterations |             600,000 |
| KDF hash          |             SHA-256 |
| Encryption        |             AES-GCM |

---

# 21. PBKDF2-HMAC-SHA256

The password supplied by the user is not directly used as an AES key.

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
32-byte AES key
```

A new random 16-byte salt is generated for every encryption operation.

The implementation uses:

```text
PBKDF2-HMAC-SHA256
600,000 iterations
32-byte derived key
```

---

# 22. AES-256-GCM

The encrypted implementation uses AES-GCM through the Python `cryptography` library.

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

The implementation generates a random 12-byte nonce.

The final encrypted data returned by `encrypt_data()` is:

```text
salt + nonce + ciphertext
```

The authentication tag is included as part of the AES-GCM ciphertext produced by the `cryptography` library.

---

# 23. Secure Image Payload

The encrypted-image implementation is contained in:

```text
src/encrypted_steg.py
```

The module uses a payload header containing:

```text
Magic
Version
Payload Length
```

The current encrypted payload identifier is:

```text
ESTG
```

and the current payload version is:

```text
1
```

The payload structure is conceptually:

```text
+----------------+---------+----------------+
| Magic (4 byte) | Version | Payload Length |
+----------------+---------+----------------+
|              Encrypted Payload             |
+---------------------------------------------+
```

The encrypted payload itself contains the cryptographic data produced by `src/crypto_utils.py`.

---

# 24. Secret Image Serialization

Before encryption, the secret image is converted into a byte representation.

The serialized image contains:

```text
4 bytes  → Magic
1 byte   → Version
4 bytes  → Width
4 bytes  → Height
Remaining → RGB pixel data
```

The image serialization uses:

```text
Magic   = STG1
Version = 1
```

The secret image is converted to RGB before serialization.

During decryption, the stored dimensions and RGB pixel data are used to reconstruct the original image.

---

# 25. Secure Image Encode

The secure CLI command is:

```text
secure-image-encode
```

It requires:

```text
--cover
--secret
--password
--output
```

Example:

```bash
.venv/Scripts/python.exe src/steg.py secure-image-encode --cover images/cover.png --secret images/secret.png --password ProjectPassword123 --output encrypted_stego.png
```

The operation performs:

```text
1. Read cover image
2. Read secret image
3. Serialize secret image
4. Generate random salt
5. Derive AES-256 key using PBKDF2
6. Generate random nonce
7. Encrypt using AES-GCM
8. Add encrypted payload header
9. Embed payload using (3,3,2)
10. Save encrypted stego image
```

Successful output:

```text
Encrypted image steganography successful.
Stego image: encrypted_stego.png
```

---

# 26. Secure Image Decode

The secure CLI command is:

```text
secure-image-decode
```

It requires:

```text
--image
--password
--output
```

Example:

```bash
.venv/Scripts/python.exe src/steg.py secure-image-decode --image encrypted_stego.png --password ProjectPassword123 --output recovered_secret.png
```

The operation performs:

```text
1. Read encrypted stego image
2. Extract the payload header
3. Validate the payload magic
4. Validate the payload version
5. Extract encrypted data
6. Read the stored salt
7. Read the stored nonce
8. Derive the AES key from the supplied password
9. Authenticate and decrypt using AES-GCM
10. Validate serialized image data
11. Reconstruct the RGB image
12. Save the recovered secret image
```

Successful output:

```text
Encrypted image recovery successful.
Recovered image: recovered_secret.png
```

---

# 27. Wrong Password Handling

The secure decoder uses AES-GCM authentication to verify that the supplied password/key is correct.

For example:

```bash
.venv/Scripts/python.exe src/steg.py secure-image-decode --image encrypted_stego.png --password WrongPassword123 --output wrong.png
```

The cryptographic layer raises:

```text
Decryption failed. Incorrect password or corrupted data.
```

The CLI reports the error rather than producing invalid decrypted image data.

---

# 28. Corrupted Data Handling

The secure pipeline also detects invalid encrypted data.

If encrypted data is modified, AES-GCM authentication fails.

The cryptographic module handles the failure and reports:

```text
Decryption failed. Incorrect password or corrupted data.
```

If corruption occurs in the image container itself rather than the encrypted payload, Pillow may reject the image before the cryptographic stage is reached.

Therefore, corrupted input may produce either:

```text
Decryption failed. Incorrect password or corrupted data.
```

or an image-processing error such as:

```text
broken data stream when reading image file
```

depending on where the corruption occurs.

---

# 29. Pixel-Perfect Secure Image Recovery

The normal `(3,3,2)` image-steganography implementation is intentionally a reduced representation of the secret image.

The encrypted workflow is different.

The secret image is serialized into its complete RGB pixel data **before encryption**:

```text
Original RGB Image
       |
       v
Raw RGB Bytes
       |
       v
Encryption
       |
       v
Embedding
```

After extraction and decryption:

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

Therefore, the secure image workflow can recover the original secret image pixel-for-pixel.

The project test suite verifies this property.

---

# 30. Normal vs Secure Image Steganography

| Feature                  | `image-encode` | `secure-image-encode` |
| ------------------------ | -------------- | --------------------- |
| Secret                   | Image          | Image                 |
| Encryption               | No             | Yes                   |
| AES-GCM                  | No             | Yes                   |
| PBKDF2                   | No             | Yes                   |
| Password                 | No             | Yes                   |
| `(3,3,2)` embedding      | Yes            | Yes                   |
| Pixel-perfect recovery   | No             | Yes                   |
| Authentication           | No             | Yes                   |
| Wrong-password detection | No             | Yes                   |
| Corruption detection     | Limited        | Yes                   |

The secure implementation therefore provides a layered model:

```text
Cryptography
     +
Steganography
```

rather than relying on steganography alone.

---

# 31. Automated Testing

The project uses `pytest`.

Run the complete test suite with:

```bash
.venv/Scripts/python.exe -m pytest -q
```

The current test result is:

```text
32 passed
```

Therefore:

```text
==============================
32 passed
==============================
```

The test suite covers:

* Basic text steganography
* UTF-8 handling
* LSB `(3,3,2)`
* Spiral `(3,3,2)`
* CLI behaviour
* Image capacity
* Password validation
* PBKDF2 key derivation
* AES-GCM encryption/decryption
* Encrypted image serialization
* Encrypted image embedding/extraction
* Wrong-password handling
* Corrupted encrypted data handling
* Pixel-perfect encrypted image recovery

---

# 32. Testing Structure

The six current test modules are:

```text
tests/
│
├── test_steganography.py
│
├── test_lsb332.py
│
├── test_spiral332.py
│
├── test_cli.py
│
├── test_crypto_utils.py
│
└── test_encrypted_steg.py
```

Each module focuses on a specific layer of the implementation.

---

# 33. Git Workflow

The project is maintained using Git.

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

Push to the main branch:

```bash
git push
```

The repository is:

```text
The-Plunderer/steganography-project
```

---

# 34. Current Implementation Status

### Completed

* [x] Basic text steganography
* [x] UTF-8 text support
* [x] Text decoding
* [x] Text capacity calculation
* [x] Image-to-image steganography
* [x] LSB `(3,3,2)`
* [x] Spiral `(3,3,2)`
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
* [x] 32/32 tests passing

### Planned

* [ ] Visual Cryptography
* [ ] Multiple visual shares
* [ ] Secret reconstruction from shares
* [ ] Colour Visual Cryptography
* [ ] Image-quality evaluation
* [ ] PSNR analysis
* [ ] Pixel-expansion analysis
* [ ] Security and performance evaluation

---

# 35. Visual Cryptography — Planned Stage

Visual Cryptography is the next major component of the project.

The intended concept is to divide a secret image into multiple shares.

For example:

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

The future implementation can investigate:

* 2-out-of-2 schemes
* k-out-of-n threshold schemes
* Colour visual cryptography
* Pixel expansion
* Reconstruction quality
* Contrast
* Computational complexity

---

# 36. Future Development

Potential future improvements include:

## Steganography

* Additional embedding algorithms
* Adaptive steganography
* Improved payload capacity
* Colour-channel analysis
* Steganalysis resistance
* Image-quality measurements

## Cryptography

* Configurable cryptographic parameters
* Improved password policies
* Additional authenticated-encryption schemes
* More detailed key-management mechanisms

## Visual Cryptography

* 2-out-of-2 visual cryptography
* k-out-of-n threshold schemes
* Colour visual cryptography
* Improved reconstruction quality
* Reduced pixel expansion

## Application

* Web interface
* Drag-and-drop image processing
* Secure file embedding
* Share generation
* Performance benchmarking

---

# 37. Project Architecture

The current architecture can be summarized as:

```text
                         CLI
                      src/steg.py
                          |
          +---------------+---------------+
          |               |               |
          v               v               v
       Text           Image           Secure Image
    Steganography   Steganography    Steganography
          |               |               |
          v               v               v
     encoder.py     lsb332.py       encrypted_steg.py
     decoder.py     spiral332.py           |
                                           v
                                    crypto_utils.py
                                           |
                                           v
                                    PBKDF2 + AES-GCM
```

This separates the project into independent functional layers while allowing them to be accessed through a single CLI.

---

# 38. Security Model

The secure image workflow uses two independent security concepts:

### Steganography

Attempts to conceal the existence of the communication.

```text
"Hide the data."
```

### Cryptography

Protects the contents of the hidden data.

```text
"Protect the data even if it is discovered."
```

The project combines them:

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

Consequently, discovering the hidden payload does not by itself reveal the original secret image.

---

# 39. Limitations

The current implementation is an educational and research prototype.

Important limitations include:

1. Basic steganography does not guarantee resistance against steganalysis.
2. Image transformations such as resizing or compression may destroy embedded data.
3. Password security depends on the strength of the password supplied by the user.
4. The current encrypted workflow is designed for project demonstration and research rather than production deployment.
5. The secure payload still depends on successful preservation of the stego image.
6. Visual Cryptography has not yet been implemented.

---

# 40. Conclusion

The project has progressed from basic text steganography to a layered **cryptography + steganography** implementation.

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
AES-256-GCM
       +
PBKDF2-HMAC-SHA256
       +
Authenticated Encrypted Image Embedding
```

The secure-image workflow encrypts the complete secret image before embedding it into a cover image. AES-GCM provides confidentiality and authentication, while PBKDF2-HMAC-SHA256 derives a 256-bit encryption key from the user's password.

The current implementation has also been validated through an automated test suite with:

```text
32 / 32 tests passing
```

The next major stage is **Visual Cryptography**, which will extend the project from single-image information hiding toward multi-share secret reconstruction.

The overall project direction is therefore:

```text
        INFORMATION HIDING
                |
        +-------+-------+
        |               |
        v               v
   STEGANOGRAPHY    CRYPTOGRAPHY
        |               |
        +-------+-------+
                |
                v
      SECURE IMAGE SYSTEM
                |
                v
       VISUAL CRYPTOGRAPHY
                |
                v
       COMPLETE PROJECT
```
