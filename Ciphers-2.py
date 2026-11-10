"""
Ciphers-2.py
------------
Cipher algorithms used by the Cryptography GUI project.

Supported algorithms:
1. Caesar Cipher
2. Additive Cipher
3. Multiplicative Cipher
4. Affine Cipher
5. Vigenere Cipher
6. Auto-Key Vigenere Cipher
7. Playfair Cipher
8. Hill Cipher (2x2)
9. Keyless Transposition Cipher

All alphabetic calculations use A=0 ... Z=25 and modulo 26.
"""

import math
import string
from typing import Callable, Dict, List, Tuple


ALPHABET = string.ascii_uppercase


def clean(text: str) -> str:
    """Return only English letters in uppercase form."""
    return "".join(ch for ch in text.upper() if ch in ALPHABET)


def caesar_cipher(text: str, key, decrypt: bool = False) -> str:
    """Caesar cipher: shift letters by a numeric key."""
    shift = int(key)
    if decrypt:
        shift = -shift

    result = ""

    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch

    return result


def additive_cipher(text: str, key, decrypt: bool = False) -> str:
    """Additive cipher; mathematically equivalent to Caesar shifting."""
    return caesar_cipher(text, key, decrypt)


def multiplicative_cipher(text: str, key, decrypt: bool = False) -> str:
    """Multiplicative cipher using modular multiplication."""
    key = int(key)

    if math.gcd(key, 26) != 1:
        raise ValueError(
            "Multiplicative key must be relatively prime to 26."
        )

    if decrypt:
        key = pow(key, -1, 26)

    result = ""

    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = ord("A") if ch.isupper() else ord("a")
            x = ord(ch) - base
            result += chr((key * x) % 26 + base)
        else:
            result += ch

    return result


def affine_cipher(text: str, key: str, decrypt: bool = False) -> str:
    """Affine cipher: C = (a*x + b) mod 26."""
    parts = key.replace(" ", "").split(",")

    if len(parts) != 2:
        raise ValueError(
            "Affine key must be in the form a,b. Example: 5,8"
        )

    a = int(parts[0])
    b = int(parts[1])

    if math.gcd(a, 26) != 1:
        raise ValueError(
            "Affine value 'a' must be relatively prime to 26."
        )

    if decrypt:
        inv_a = pow(a, -1, 26)
        a, b = inv_a, (-inv_a * b) % 26

    result = ""

    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = ord("A") if ch.isupper() else ord("a")
            x = ord(ch) - base
            result += chr((a * x + b) % 26 + base)
        else:
            result += ch

    return result


def vigenere_cipher(text: str, key: str, decrypt: bool = False) -> str:
    """Standard Vigenere cipher with a repeating keyword."""
    key = clean(key)

    if not key:
        raise ValueError("Vigenere key must contain English letters.")

    result = ""
    index = 0

    for ch in text:
        if ch.isalpha() and ch.isascii():
            shift = ord(key[index % len(key)]) - ord("A")

            if decrypt:
                shift = -shift

            base = ord("A") if ch.isupper() else ord("a")
            result += chr((ord(ch) - base + shift) % 26 + base)
            index += 1
        else:
            result += ch

    return result


def autokey_vigenere_cipher(
    text: str, key: str, decrypt: bool = False
) -> str:
    """
    Auto-Key Vigenere.

    The supplied keyword starts the key stream. During encryption,
    plaintext letters extend the key stream. During decryption,
    recovered plaintext letters extend it.
    """
    key = clean(key)

    if not key:
        raise ValueError(
            "Auto-Key Vigenere key must contain English letters."
        )

    result = ""
    key_stream = [ord(ch) - ord("A") for ch in key]
    index = 0

    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = ord("A") if ch.isupper() else ord("a")

            if index >= len(key_stream):
                raise ValueError("Auto-Key stream error.")

            shift = key_stream[index]
            x = ord(ch) - base

            if decrypt:
                p = (x - shift) % 26
                result += chr(p + base)
                key_stream.append(p)
            else:
                p = x
                c = (p + shift) % 26
                result += chr(c + base)
                key_stream.append(p)

            index += 1
        else:
            result += ch

    return result


def create_playfair_matrix(key: str) -> List[List[str]]:
    """Create a 5x5 Playfair matrix, combining I/J."""
    key = clean(key).replace("J", "I")

    if not key:
        raise ValueError("Playfair key cannot be empty.")

    letters: List[str] = []

    for ch in key + ALPHABET:
        if ch == "J":
            ch = "I"

        if ch not in letters:
            letters.append(ch)

    return [letters[i:i + 5] for i in range(0, 25, 5)]


def find_position(
    matrix: List[List[str]], ch: str
) -> Tuple[int, int]:
    """Find row and column of a Playfair character."""
    if ch == "J":
        ch = "I"

    for row in range(5):
        for col in range(5):
            if matrix[row][col] == ch:
                return row, col

    raise ValueError("Character not found in Playfair matrix.")


def prepare_playfair_text(text: str) -> List[str]:
    """Prepare plaintext as Playfair digraphs."""
    text = clean(text).replace("J", "I")

    if not text:
        return []

    pairs: List[str] = []
    i = 0

    while i < len(text):
        first = text[i]

        if i + 1 >= len(text):
            pairs.append(first + "X")
            i += 1
        elif text[i] == text[i + 1]:
            pairs.append(first + "X")
            i += 1
        else:
            pairs.append(first + text[i + 1])
            i += 2

    return pairs


def playfair_cipher(
    text: str, key: str, decrypt: bool = False
) -> str:
    """Playfair cipher using the standard 5x5 rules."""
    matrix = create_playfair_matrix(key)

    if decrypt:
        clean_text = clean(text).replace("J", "I")

        if len(clean_text) % 2 != 0:
            raise ValueError(
                "Playfair ciphertext must have an even number of letters."
            )

        pairs = [
            clean_text[i:i + 2]
            for i in range(0, len(clean_text), 2)
        ]
    else:
        pairs = prepare_playfair_text(text)

    direction = -1 if decrypt else 1
    result = ""

    for first, second in pairs:
        row1, col1 = find_position(matrix, first)
        row2, col2 = find_position(matrix, second)

        if row1 == row2:
            result += matrix[row1][(col1 + direction) % 5]
            result += matrix[row2][(col2 + direction) % 5]

        elif col1 == col2:
            result += matrix[(row1 + direction) % 5][col1]
            result += matrix[(row2 + direction) % 5][col2]

        else:
            result += matrix[row1][col2]
            result += matrix[row2][col1]

    return result


def parse_hill_key(key: str) -> Tuple[int, int, int, int]:
    """Parse a 2x2 Hill key: a,b,c,d."""
    parts = key.replace(";", ",").split(",")
    values = [int(part.strip()) for part in parts if part.strip()]

    if len(values) != 4:
        raise ValueError(
            "Hill key must contain 4 numbers. Example: 3,3,2,5"
        )

    return values[0], values[1], values[2], values[3]


def hill_cipher(
    text: str, key: str, decrypt: bool = False
) -> str:
    """Hill cipher using a 2x2 key matrix."""
    a, b, c, d = parse_hill_key(key)

    determinant = (a * d - b * c) % 26

    if math.gcd(determinant, 26) != 1:
        raise ValueError(
            "Hill matrix has no inverse modulo 26."
        )

    text = clean(text)

    if not text:
        return ""

    if len(text) % 2 != 0:
        text += "X"

    if decrypt:
        inv_det = pow(determinant, -1, 26)
        a, b, c, d = (
            (d * inv_det) % 26,
            (-b * inv_det) % 26,
            (-c * inv_det) % 26,
            (a * inv_det) % 26,
        )

    result = ""

    for i in range(0, len(text), 2):
        x1 = ord(text[i]) - ord("A")
        x2 = ord(text[i + 1]) - ord("A")

        y1 = (a * x1 + b * x2) % 26
        y2 = (c * x1 + d * x2) % 26

        result += chr(y1 + ord("A"))
        result += chr(y2 + ord("A"))

    return result


def transposition_cipher(
    text: str, key=None, decrypt: bool = False
) -> str:
    """
    Keyless transposition used by this project.

    It reverses the cleaned letter sequence. Since reversing is its
    own inverse, the same operation is used for encryption/decryption.
    """
    cleaned = clean(text)

    if not cleaned:
        return ""

    return cleaned[::-1]


# Central registry used by the GUI.
ALGORITHMS: Dict[str, Callable] = {
    "Caesar Cipher": caesar_cipher,
    "Additive Cipher": additive_cipher,
    "Multiplicative Cipher": multiplicative_cipher,
    "Affine Cipher": affine_cipher,
    "Vigenere Cipher": vigenere_cipher,
    "Auto-Key Vigenere Cipher": autokey_vigenere_cipher,
    "Playfair Cipher": playfair_cipher,
    "Hill Cipher": hill_cipher,
    "Keyless Transposition Cipher": transposition_cipher,
}


KEY_HINTS = {
    "Caesar Cipher": "Numeric key, e.g. 3",
    "Additive Cipher": "Numeric key, e.g. 3",
    "Multiplicative Cipher": "Key relatively prime to 26, e.g. 5",
    "Affine Cipher": "Two values a,b, e.g. 5,8",
    "Vigenere Cipher": "English keyword, e.g. PASCAL",
    "Auto-Key Vigenere Cipher": "Initial keyword, e.g. QUEEN",
    "Playfair Cipher": "English keyword, e.g. MONARCHY",
    "Hill Cipher": "Four numbers a,b,c,d, e.g. 3,3,2,5",
    "Keyless Transposition Cipher": "No key required",
}
