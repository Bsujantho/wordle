import unittest
import os
import sys

# Add parent directory to path to allow importing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from word_bank import WordBank
from game import WordleGame

class TestWordBank(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_words_wb.txt"
        with open(self.test_file, "w") as f:
            f.write("APPLE\n")
            f.write("BERRY\n")
            f.write("CHERRY\n") # Invalid length (6)
            f.write("DATE\n")   # Invalid length (4)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_load_words(self):
        wb = WordBank(self.test_file)
        self.assertEqual(len(wb.words), 2)
        self.assertIn("APPLE", wb.words)
        self.assertIn("BERRY", wb.words)
        self.assertNotIn("CHERRY", wb.words)

    def test_contains(self):
        wb = WordBank(self.test_file)
        self.assertTrue(wb.contains("APPLE"))
        self.assertFalse(wb.contains("BANANA"))

class TestWordleGame(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_words_game.txt"
        with open(self.test_file, "w") as f:
            f.write("ABCDE\n")
            f.write("FGHIJ\n")
        self.game = WordleGame(self.test_file)
        self.game.secret_word = "ABCDE" # Fix secret word for testing

    def tearDown(self):
         if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_process_guess_correct(self):
        guess = "ABCDE"
        self.game._process_guess(guess)
        self.assertTrue(self.game.is_won)
        self.assertEqual(self.game.guesses[-1][1], ['GREEN', 'GREEN', 'GREEN', 'GREEN', 'GREEN'])

    def test_process_guess_incorrect(self):
        guess = "FGHIJ"
        self.game._process_guess(guess)
        self.assertFalse(self.game.is_won)
        self.assertEqual(self.game.guesses[-1][1], ['GRAY', 'GRAY', 'GRAY', 'GRAY', 'GRAY'])

    def test_process_guess_partial(self):
        # Secret: ABCDE
        # Guess: AEDCB
        # A (0) -> GREEN (A==A)
        # E (1) -> YELLOW (E in ABCDE at 4)
        # D (2) -> YELLOW
        # C (3) -> YELLOW
        # B (4) -> YELLOW

        guess = "AEDCB"
        self.game._process_guess(guess)
        feedback = self.game.guesses[-1][1]
        self.assertEqual(feedback[0], 'GREEN')
        self.assertEqual(feedback[1], 'YELLOW')
        self.assertEqual(feedback[2], 'YELLOW')
        self.assertEqual(feedback[3], 'YELLOW')
        self.assertEqual(feedback[4], 'YELLOW')

    def test_keyboard_update(self):
        # Secret: ABCDE
        self.game._process_guess("ABFGH")
        # A, B -> GREEN
        # F, G, H -> GRAY

        self.assertEqual(self.game.letter_states['A'], 'GREEN')
        self.assertEqual(self.game.letter_states['B'], 'GREEN')
        self.assertEqual(self.game.letter_states['F'], 'GRAY')
        self.assertEqual(self.game.letter_states['Z'], 'UNKNOWN')

    def test_double_letter_logic(self):
        # Target: HELLO
        self.game.secret_word = "HELLO"
        # Guess: LEVEL
        # L(0) -> YELLOW (matches L(2) or L(3))
        # E(1) -> GREEN (matches E(1))
        # V(2) -> GRAY
        # E(3) -> GRAY (E(1) already matched by E(1))
        # L(4) -> YELLOW

        guess = "LEVEL"
        self.game._process_guess(guess)
        feedback = self.game.guesses[-1][1]

        self.assertEqual(feedback[0], 'YELLOW')
        self.assertEqual(feedback[1], 'GREEN')
        self.assertEqual(feedback[2], 'GRAY')
        self.assertEqual(feedback[3], 'GRAY')
        self.assertEqual(feedback[4], 'YELLOW')

if __name__ == '__main__':
    unittest.main()
