# CipherLab Pro

### Classical Cryptography Studio

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Tkinter-2E8B57)
![Project](https://img.shields.io/badge/Project-Educational-7B61A8)
![Tests](https://img.shields.io/badge/Tests-13%20passing-success)

A desktop application built with **Python** and **Tkinter** for demonstrating classical encryption and decryption algorithms through a graphical interface.

> **Created by Yaqub Ismail Solan (يعقوب إسماعيل صولان)**  
> Third-year Engineering Student · Al-Razi University · Yemen

---

## Overview

CipherLab Pro brings nine classical cipher techniques into one local desktop workspace. Select an algorithm, enter its key or parameters, choose encryption or decryption, and inspect or export the result.

This project is intended for **education and classroom demonstrations**. Classical ciphers are not suitable for protecting modern confidential information.

## Features

- Dark Tkinter desktop interface.
- Nine classical cipher implementations.
- Encryption and decryption modes.
- Key hints and parameter validation.
- Demonstration examples.
- Copy, swap, and export result actions.
- Operation counter and local processing history.
- Local processing; no internet connection is required.
- Automated unit tests for the cipher functions.

## Supported algorithms

| # | Algorithm | Key / parameters |
|---:|---|---|
| 1 | Caesar Cipher | Integer shift |
| 2 | Additive Cipher | Integer shift |
| 3 | Multiplicative Cipher | Integer relatively prime to 26 |
| 4 | Affine Cipher | `a,b`, where `gcd(a, 26) = 1` |
| 5 | Vigenère Cipher | English keyword |
| 6 | Auto-Key Vigenère Cipher | Initial English keyword |
| 7 | Playfair Cipher | English keyword; I/J share one cell |
| 8 | Hill Cipher (2×2) | Four integers: `a,b,c,d` |
| 9 | Keyless Transposition (Reversal) | No key |

**Implementation clarification:** The operation named “Keyless Transposition” reverses the cleaned letter sequence. It is a simple educational reversal operation, not a general columnar transposition cipher.

## Requirements

- Python 3.10 or newer.
- Tkinter. It is included with many Python installations; some Linux distributions package it separately.
- No third-party Python packages are required.

## Run the application

1. Install Python 3.10 or newer.
2. Download or clone this repository.
3. Open a terminal in the project directory.
4. Run:

```bash
python main.py
```

On some systems, use `python3 main.py`.

## Run the tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

The test suite checks encryption/decryption round trips, invalid keys, the nine-algorithm registry, and prepared Playfair text behavior.

## How to use

1. Launch the application.
2. Select a cipher from the sidebar.
3. Enter the required key or parameters shown in the key hint.
4. Enter or paste the input text.
5. Select **ENCRYPT** or **DECRYPT**.
6. Click **RUN OPERATION**.
7. Copy, swap, or export the result as needed.

## Educational notes and limitations

- Classical ciphers are historically important but are not secure by modern standards.
- Base64 is an encoding scheme, **not encryption**.
- Playfair decryption returns prepared letter pairs; it does not automatically remove filler `X` characters or restore omitted spaces.
- Hill Cipher uses a 2×2 key matrix and requires an invertible matrix modulo 26.
- The application processes text locally and does not send input to a server.
- Do not use this application to protect passwords, personal data, financial information, or other sensitive information.

## Project structure

```text
CipherLab-Pro/
├── .github/
│   └── workflows/
│       └── tests.yml
├── tests/
│   └── test_ciphers.py
├── .gitignore
├── CONTRIBUTING.md
├── Ciphers-2.py
├── CHANGELOG.md
├── README.md
└── main.py
```

## Author

**Yaqub Ismail Solan (يعقوب إسماعيل صولان)**  
Third-year Engineering Student  
**Al-Razi University · Yemen**

## Future improvements

- Add verified application screenshots and a short demonstration GIF.
- Add step-by-step visual explanations for each cipher.
- Expand automated tests and improve algorithm-specific validation.
- Add more classical cipher demonstrations.

---

*An educational university project. Feedback and learning-focused contributions are welcome.*
