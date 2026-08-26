import os
import sys
import tempfile
import unittest
from io import StringIO

# Import functions from your solution file (assumed to be named vigenere_cipher.py)
try:
    from vigenere_cipher import (
        adjusted_key,
        decrypt_vigenere,
        encrypt_vigenere,
        main,
        menu,
    )
except ImportError:
    print("Error: Could not import 'vigenere_cipher.py'.")
    print("Please make sure this autograder script is in the same directory as your solution file.")
    sys.exit(1)


class TestPart1AdjustedKey(unittest.TestCase):
    """5 Test Cases for Part 1: adjusted_key(text, key)"""

    def test_case_1_basic_repeated_key(self):
        text = "ilovepythonprogramming"
        key = "abc"
        expected = "abcabcabcabcabcabcabca"
        self.assertEqual(adjusted_key(text, key), expected)

    def test_case_2_with_spaces_and_punctuation(self):
        text = "pittsburgh pa"
        key = "yes"
        expected = "yesyesyesy es"
        self.assertEqual(adjusted_key(text, key), expected)

    def test_case_3_single_letter_key(self):
        text = "hello world!"
        key = "a"
        expected = "aaaaa aaaaa!"
        self.assertEqual(adjusted_key(text, key), expected)

    def test_case_4_key_longer_than_text(self):
        text = "hi"
        key = "python"
        expected = "py"
        self.assertEqual(adjusted_key(text, key), expected)

    def test_case_5_numbers_and_special_chars_ignored(self):
        text = "cs 0011 lab #7!"
        key = "cat"
        expected = "ca 0011 tca #7!"
        self.assertEqual(adjusted_key(text, key), expected)


class TestPart1And2Encryption(unittest.TestCase):
    """5 Test Cases for Part 1 & 2: File-based Encryption"""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_encrypt_test(self, input_content, key, expected_output):
        in_path = os.path.join(self.temp_dir.name, "input.txt")
        out_path = os.path.join(self.temp_dir.name, "output.txt")

        with open(in_path, "w") as f:
            f.write(input_content)

        # Simulate user inputs: input_file, key, output_file
        user_inputs = f"{in_path}\n{key}\n{out_path}\n"
        sys.stdin = StringIO(user_inputs)

        encrypt_vigenere()

        self.assertTrue(os.path.exists(out_path))
        with open(out_path, "r") as f:
            result = f.read()

        self.assertEqual(result, expected_output)

    def test_case_1_standard_encryption(self):
        self.run_encrypt_test("pittsburgh pa", "yes", "nmlrwtsvyf ts")

    def test_case_2_encryption_with_python_key(self):
        self.run_encrypt_test(
            "computer programming", "python", "rmfwigtp iyctgyftwav"
        )

    def test_case_3_encryption_with_zero_shift_key_a(self):
        self.run_encrypt_test("hello world", "a", "hello world")

    def test_case_4_uppercase_conversion(self):
        self.run_encrypt_test("PITTSBURGH PA", "YES", "nmlrwtsvyf ts")

    def test_case_5_preserve_numbers_and_symbols(self):
        self.run_encrypt_test("pittsburgh, 15260!", "key", "zmrdwzever, 15260!")


class TestPart2Decryption(unittest.TestCase):
    """5 Test Cases for Part 2: File-based Decryption"""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_decrypt_test(self, input_content, key, expected_output):
        in_path = os.path.join(self.temp_dir.name, "input.txt")
        out_path = os.path.join(self.temp_dir.name, "output.txt")

        with open(in_path, "w") as f:
            f.write(input_content)

        # Simulate user inputs: input_file, key, output_file
        user_inputs = f"{in_path}\n{key}\n{out_path}\n"
        sys.stdin = StringIO(user_inputs)

        decrypt_vigenere()

        self.assertTrue(os.path.exists(out_path))
        with open(out_path, "r") as f:
            result = f.read()

        self.assertEqual(result, expected_output)

    def test_case_1_standard_decryption(self):
        self.run_decrypt_test("nmlrwtsvyf ts", "yes", "pittsburgh pa")

    def test_case_2_decryption_with_python_key(self):
        self.run_decrypt_test(
            "rmfwigtp iyctgyftwav", "python", "computer programming"
        )

    def test_case_3_decryption_with_zero_shift_key_a(self):
        self.run_decrypt_test("hello world", "a", "hello world")

    def test_case_4_uppercase_key_decryption(self):
        self.run_decrypt_test("nmlrwtsvyf ts", "YES", "pittsburgh pa")

    def test_case_5_preserve_numbers_and_symbols_decryption(self):
        self.run_decrypt_test("zmrdwzever, 15260!", "key", "pittsburgh, 15260!")


class TestPart3MenuAndMain(unittest.TestCase):
    """5 Test Cases for Part 3: Menu & Main Loop Execution"""

    def test_case_1_menu_valid_option_1(self):
        sys.stdin = StringIO("1\n")
        result = menu()
        self.assertEqual(result, "1")

    def test_case_2_menu_valid_option_2(self):
        sys.stdin = StringIO("2\n")
        result = menu()
        self.assertEqual(result, "2")

    def test_case_3_menu_valid_option_9(self):
        sys.stdin = StringIO("9\n")
        result = menu()
        self.assertEqual(result, "9")

    def test_case_4_menu_invalid_then_valid(self):
        sys.stdin = StringIO("5\n0\n1\n")
        captured_output = StringIO()
        sys.stdout = captured_output

        result = menu()

        sys.stdout = sys.__stdout__
        self.assertEqual(result, "1")
        self.assertIn("Invalid option. Try again.", captured_output.getvalue())

    def test_case_5_main_loop_exit_on_9(self):
        sys.stdin = StringIO("9\n")
        captured_output = StringIO()
        sys.stdout = captured_output

        main()

        sys.stdout = sys.__stdout__
        self.assertIn("Quitting program. Bye!", captured_output.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)