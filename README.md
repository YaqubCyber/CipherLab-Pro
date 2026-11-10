# CipherLab Pro
### Classical Cryptography Studio

A desktop learning application built with **Python** and **Tkinter** for demonstrating classical encryption and decryption techniques through a clean graphical interface.

> **Academic project** by **Aqoub Ismail Sawlah (عقوب إسماعيل صولة)**  
> Third-year Engineering Student · Al-Razi University · Yemen

---

## Overview

CipherLab Pro brings nine classical cipher techniques into one local desktop workspace. Select an algorithm, enter its key or parameters, choose encryption or decryption, and inspect or export the result.

The application is intended for **education and classroom demonstrations**. It is not designed to protect real-world confidential information.

## Features

- Dark desktop interface with button-based algorithm selection.
- Encryption and decryption modes.
- Nine classical cipher implementations.
- Key hints and parameter validation.
- Demo examples for each algorithm.
- Copy, swap, and export result actions.
- Operation counter and local processing history.
- Runs locally without an internet connection.
- Automated unit tests for core cipher behavior.

## Supported algorithms

| # | Algorithm | Key / parameters |
|---:|---|---|
| 1 | Caesar Cipher | Integer shift |
| 2 | Additive Cipher | Integer shift |
| 3 | Multiplicative Cipher | Integer relatively prime to 26 |
| 4 | Affine Cipher | `a,b` where `gcd(a, 26) = 1` |
| 5 | Vigenère Cipher | English keyword |
| 6 | Auto-Key Vigenère Cipher | Initial English keyword |
| 7 | Playfair Cipher | English keyword; combines I/J |
| 8 | Hill Cipher (2×2) | Four integers: `a,b,c,d` |
| 9 | Keyless Transposition (Reversal) | No key |

**Implementation note:** The project’s “Keyless Transposition” operation reverses the cleaned letter sequence. It is a simple educational reversal operation, not a general columnar transposition cipher.

## Requirements

- Python 3.10 or newer (the project uses only Python's standard library).
- Tkinter, which is included with many Python installations. On some Linux distributions it must be installed separately.

No third-party Python packages are required.

## Run the application

1. Install Python 3.10+.
2. Download or clone this repository.
3. Open a terminal in the project directory.
4. Run:

```bash
python main.py
```

On some systems, use `python3 main.py`.

## Run tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

The test suite checks encryption/decryption round trips, invalid key handling, the algorithm registry, and Playfair's prepared-text behavior.

## How to use

1. Launch the application with `python main.py`.
2. Select a cipher from the left sidebar.
3. Enter the required key or parameters shown in the key hint.
4. Paste or type text in the input panel.
5. Select **ENCRYPT** or **DECRYPT**.
6. Click **RUN OPERATION**.
7. Copy, swap, or export the output as needed.

## Educational notes and limitations

- Classical ciphers are historically important but are not secure by modern standards.
- Base64 is an encoding scheme, **not encryption**.
- Playfair decryption returns the prepared letter pairs. It does not automatically remove filler `X` characters or reconstruct omitted spaces.
- Hill Cipher uses a 2×2 key matrix and requires an invertible matrix modulo 26.
- The application processes text locally; it does not send input to a server.

**Do not use this application to protect passwords, personal data, financial information, or other sensitive information.**

## Project structure

```text
CipherLab-Pro/
├── main.py
├── Ciphers-2.py
├── README.md
├── .gitignore
└── tests/
    └── test_ciphers.py
```

## Author

**Aqoub Ismail Sawlah (عقوب إسماعيل صولة)**  
Third-year Engineering Student  
**Al-Razi University — Yemen**

- GitHub: [Add your GitHub profile URL]
- Email: [Add a public contact email if you want to share one]

## Future improvements

- Add screenshots and a short demo GIF.
- Add step-by-step explanations for each cipher.
- Add a dedicated result history viewer.
- Add input validation and clearer algorithm-specific help in the interface.
- Add support for configurable alphabets and additional classical ciphers.

---

*Created as an educational university project. Contributions and learning-focused feedback are welcome.*
