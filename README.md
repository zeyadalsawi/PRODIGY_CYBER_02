# Simple Image Encryption Tool

This tool allows you to encrypt and decrypt images using basic pixel manipulation (XOR with a numeric key). It provides a simple GUI for easy use.

## How to Use

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the tool:
   ```bash
   python main.py
   ```
3. Select an image, enter a numeric key (0-255), and choose Encrypt or Decrypt.

## How It Works
- The tool applies an XOR operation to each pixel's RGB values with the given key.
- Encryption and decryption use the same process (XOR is reversible).

## Supported Formats
- PNG, JPG, JPEG, BMP, TIFF

## Notes
- Use the same key for decryption as used for encryption.
- The output image will be saved in the same directory as the original, with `_encrypted` or `_decrypted` appended to the filename.
