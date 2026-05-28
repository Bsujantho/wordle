from pathlib import Path
import tempfile
import unittest

from word_bank import WordBank


class WordBankTests(unittest.TestCase):
    def test_loads_uppercase_unique_words_and_skips_comments(self):
        with tempfile.TemporaryDirectory() as directory:
            word_file = Path(directory) / "words.txt"
            word_file.write_text("apple\n# comment\napple\ncrane\n\n", encoding="utf-8")

            word_bank = WordBank(word_file)

        self.assertEqual(word_bank.words, ["APPLE", "CRANE"])
        self.assertTrue(word_bank.contains("apple"))
        self.assertFalse(word_bank.contains("apples"))

    def test_invalid_words_fail_fast(self):
        with tempfile.TemporaryDirectory() as directory:
            word_file = Path(directory) / "words.txt"
            word_file.write_text("apple\nTOOLONG\n", encoding="utf-8")

            with self.assertRaises(ValueError):
                WordBank(word_file)

    def test_missing_word_file_fails_fast(self):
        with self.assertRaises(FileNotFoundError):
            WordBank("does-not-exist.txt")


if __name__ == "__main__":
    unittest.main()
