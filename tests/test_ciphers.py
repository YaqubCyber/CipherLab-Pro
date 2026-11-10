import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ciphers", ROOT / "Ciphers-2.py")
ciphers = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ciphers)


class CipherTests(unittest.TestCase):
    def assert_round_trip(self, algorithm, plaintext, key):
        encrypted = algorithm(plaintext, key, decrypt=False)
        decrypted = algorithm(encrypted, key, decrypt=True)
        self.assertEqual(decrypted, plaintext)

    def test_caesar_round_trip_and_punctuation(self):
        self.assert_round_trip(ciphers.caesar_cipher, "Hello, World! 123", 3)

    def test_additive_round_trip(self):
        self.assert_round_trip(ciphers.additive_cipher, "Attack at Dawn", 11)

    def test_multiplicative_round_trip(self):
        self.assert_round_trip(ciphers.multiplicative_cipher, "Meet me at 9", 5)

    def test_multiplicative_rejects_non_coprime_key(self):
        with self.assertRaises(ValueError):
            ciphers.multiplicative_cipher("HELLO", 2)

    def test_affine_round_trip(self):
        self.assert_round_trip(ciphers.affine_cipher, "Affine Cipher!", "5,8")

    def test_affine_rejects_invalid_a(self):
        with self.assertRaises(ValueError):
            ciphers.affine_cipher("HELLO", "2,8")

    def test_vigenere_round_trip(self):
        self.assert_round_trip(ciphers.vigenere_cipher, "Attack at Dawn!", "LEMON")

    def test_autokey_vigenere_round_trip(self):
        self.assert_round_trip(ciphers.autokey_vigenere_cipher, "ATTACKATDAWN", "QUEEN")

    def test_playfair_round_trip_to_prepared_text(self):
        plaintext = "HIDE THE GOLD"
        encrypted = ciphers.playfair_cipher(plaintext, "MONARCHY")
        decrypted = ciphers.playfair_cipher(encrypted, "MONARCHY", decrypt=True)
        self.assertEqual(decrypted, "".join(ciphers.prepare_playfair_text(plaintext)))

    def test_hill_round_trip_with_padding(self):
        plaintext = "HELP"
        encrypted = ciphers.hill_cipher(plaintext, "3,3,2,5")
        self.assertEqual(ciphers.hill_cipher(encrypted, "3,3,2,5", decrypt=True), plaintext)

    def test_hill_rejects_non_invertible_matrix(self):
        with self.assertRaises(ValueError):
            ciphers.hill_cipher("HELP", "2,4,2,4")

    def test_keyless_transposition_is_reversible_on_cleaned_text(self):
        encrypted = ciphers.transposition_cipher("Hello, World!", "")
        self.assertEqual(encrypted, "DLROWOLLEH")
        self.assertEqual(ciphers.transposition_cipher(encrypted, "", decrypt=True), "HELLOWORLD")

    def test_registry_contains_nine_algorithms(self):
        self.assertEqual(len(ciphers.ALGORITHMS), 9)


if __name__ == "__main__":
    unittest.main()
