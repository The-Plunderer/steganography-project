\# Steganography and Visual Cryptography



A project focused on implementing and studying \*\*image steganography\*\* and \*\*visual cryptography\*\* techniques.



\## Current Module



\*\*Basic Image Steganography using Least Significant Bit (LSB) Substitution\*\*



The current implementation hides a secret text message inside an RGB image by modifying the least significant bit of each color channel.



The project is being developed incrementally, with cryptography and visual cryptography planned for later stages.



\---



\## Objectives



\* Hide secret information inside an image.

\* Extract hidden information from a stego image.

\* Implement the process using a command-line interface.

\* Validate image capacity before hiding data.

\* Support UTF-8 text messages.

\* Handle invalid input and oversized messages.

\* Develop automated tests for the implementation.

\* Study the security and limitations of LSB steganography.

\* Later integrate cryptographic techniques.

\* Later implement visual cryptography.



\---



\## Technology Stack



\* \*\*Python 3\*\*

\* \*\*Pillow\*\* — image processing

\* \*\*pytest\*\* — automated testing

\* \*\*Git\*\* — version control

\* \*\*GitHub\*\* — source-code hosting

\* \*\*Git Bash\*\* — command-line environment



\---



\## Project Structure



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

│   └── test\_steganography.py

│

├── README.md

├── requirements.txt

├── .gitignore

└── .git/

```



\### File Description



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



\---



\## How LSB Steganography Works



In an RGB image, each pixel contains three color channels:



```text

Pixel

&#x20;├── Red

&#x20;├── Green

&#x20;└── Blue

```



Each channel contains an 8-bit value.



For example:



```text

Original pixel:



Red   = 10110100

Green = 01101011

Blue  = 11001010

```



The encoder modifies only the \*\*least significant bit (LSB)\*\*:



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



The visual difference is extremely small, while the modified bits can store information.



The decoder reads the LSBs from the RGB channels and reconstructs the hidden message.



\---



\## Installation



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



Install the project dependencies:



```bash

python -m pip install -r requirements.txt

```



If the Windows `python` command is unavailable, use:



```bash

.venv/Scripts/python.exe -m pip install -r requirements.txt

```



\---



\## Usage



\### 1. Encode a Secret Message



The `encode` command hides a message inside a cover image.



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



The generated image will be saved as:



```text

output/stego.png

```



\---



\### 2. Decode a Secret Message



The `decode` command extracts the hidden message.



```bash

.venv/Scripts/python.exe src/steg.py decode --image output/stego.png

```



Example output:



```text

Hidden message:

Hello from my project!

```



\---



\## Command-Line Help



To display the available commands:



```bash

.venv/Scripts/python.exe src/steg.py --help

```



Example:



```text

usage: steg.py \[-h] {encode,decode} ...



Basic LSB Image Steganography Tool



positional arguments:

&#x20; {encode,decode}

&#x20;   encode         Hide a secret message inside an image

&#x20;   decode         Extract a hidden message from an image

```



\---



\## Running the Tests



The project includes automated tests using `pytest`.



Run:



```bash

.venv/Scripts/python.exe -m pytest -v

```



Current test coverage includes:



\* Normal message encoding and decoding

\* Unicode message handling

\* Missing image handling

\* Oversized message validation



Expected result:



```text

4 passed

```



\---



\## Capacity Validation



The encoder checks whether the secret message can fit inside the selected image.



For an RGB image:



```text

Number of available bits = width × height × 3

```



The implementation also reserves space for an end marker used by the decoder to determine where the hidden message ends.



If the message is too large, the encoder reports an error instead of producing an invalid stego image.



\---



\## Current Limitations



The current implementation is an educational/basic implementation of LSB steganography.



\### 1. No Encryption



The hidden message is not encrypted.



Anyone who knows the steganography method can potentially extract the message.



\### 2. PNG Recommended



The current implementation saves the stego image as PNG.



Lossy formats such as JPEG can modify pixel values during compression and may destroy the hidden LSB data.



\### 3. Text Messages Only



The current version hides UTF-8 text messages.



Binary files and arbitrary file formats are not supported yet.



\### 4. No Authentication



The current implementation does not provide authentication or integrity verification.



\### 5. Basic LSB Method



LSB substitution is simple and educational, but it is not designed to provide strong resistance against steganalysis.



\---



\## Development Roadmap



\### Version 0.1 — Basic LSB Steganography



\* \[x] Encode text into an image

\* \[x] Decode text from an image

\* \[x] UTF-8 support

\* \[x] Capacity validation

\* \[x] Basic error handling

\* \[x] Command-line interface

\* \[x] Automated tests



\### Version 0.2 — Improved CLI



\* \[ ] Improved command-line validation

\* \[ ] Better error messages

\* \[ ] Additional command-line options

\* \[ ] Improved project documentation



\### Version 0.3 — Secure Message Handling



\* \[ ] Password-based protection

\* \[ ] Cryptographic encryption

\* \[ ] Message integrity verification



\### Version 0.4 — Advanced Steganography



\* \[ ] Image-to-image steganography

\* \[ ] Improved embedding strategies

\* \[ ] Steganalysis considerations



\### Version 0.5 — Visual Cryptography



\* \[ ] Implement visual cryptography

\* \[ ] Generate cryptographic shares

\* \[ ] Reconstruct the secret image

\* \[ ] Study pixel expansion and reconstruction quality



\### Version 1.0 — Integrated System



\* \[ ] Combine cryptography and steganography

\* \[ ] Integrate visual cryptography

\* \[ ] Improve security

\* \[ ] Create a complete user interface

\* \[ ] Final testing and documentation



\---



\## Testing Status



Current implementation:



```text

Automated Tests: 4/4 PASSED

```



The tests currently verify:



```text

Encode → Decode          ✓

Unicode Message         ✓

Missing Image Handling  ✓

Oversized Message       ✓

```



\---



\## Project Status



\*\*Current Stage:\*\* Basic LSB Image Steganography



\*\*Implementation Status:\*\* Working



\*\*Test Status:\*\* 4/4 tests passing



\*\*Next Development Stage:\*\* Improved CLI and secure message handling



\---



\## Team Project



This project is being developed as part of a final-year academic project on:



\*\*Steganography and Visual Cryptography\*\*



