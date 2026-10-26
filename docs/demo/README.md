# Image Steganography Demonstrations

This directory contains sample outputs from three image steganography algorithms implemented in this project.

## 1. LSB332

Embeds secret image data using the least significant bits of the cover image's RGB channels.

- Encoded image: [stego_lsb332.png](stego_lsb332.png)
- Recovered image: [recovered_lsb332.png](recovered_lsb332.png)

## 2. Spiral332

Traverses image pixels in a spiral order while embedding secret image data.

- Encoded image: [stego_spiral332.png](stego_spiral332.png)
- Recovered image: [recovered_spiral332.png](recovered_spiral332.png)

## 3. Adaptive332

Uses a two-bit indicator in the red channel to select either the green or blue channel for additional embedding.

- Encoded image: [stego_adaptive332.png](stego_adaptive332.png)
- Recovered image: [recovered_adaptive332.png](recovered_adaptive332.png)

## Reproducing the demonstrations

Run the commands below from the repository root with the project's Python environment activated.

### LSB332

    py src/steg.py image-encode --method lsb332 --cover images/cover.png --secret images/secret.png --output output/stego_lsb332.png
    py src/steg.py image-decode --method lsb332 --image output/stego_lsb332.png --output output/recovered_lsb332.png

### Spiral332

    py src/steg.py image-encode --method spiral332 --cover images/cover.png --secret images/secret.png --output output/stego_spiral332.png
    py src/steg.py image-decode --method spiral332 --image output/stego_spiral332.png --output output/recovered_spiral332.png

### Adaptive332

    py src/steg.py image-encode --method adaptive332 --cover images/cover.png --secret images/secret.png --output output/stego_adaptive332.png
    py src/steg.py image-decode --method adaptive332 --image output/stego_adaptive332.png --output output/recovered_adaptive332.png

## Notes

- The cover image contains the embedded secret image data.
- The recovered image is reconstructed from the stego image.
- Recovered pixel values may differ from the original secret image.
- These examples demonstrate image steganography but do not establish resistance to steganalysis.
