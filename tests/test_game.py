import unittest

from feedback import GREEN
from game import WordleGame


class FakeWordBank:
    def __init__(self, words):
        self.words = words

    def get_random_word(self):
        return self.words[0]


class WordleGameTests(unittest.TestCase):
    def test_process_guess_updates_win_state(self):
        game = WordleGame(
            max_guesses=2,
            secret_word="APPLE",
            word_bank=FakeWordBank(["APPLE"]),
            use_color=False,
        )

        feedback = game._process_guess("apple")

        self.assertEqual(feedback, (GREEN, GREEN, GREEN, GREEN, GREEN))
        self.assertTrue(game.is_won)
        self.assertFalse(game.is_lost)
        self.assertEqual(game.guesses_left, 1)
        self.assertEqual(game.guesses[0][0], "APPLE")

    def test_process_guess_updates_loss_state(self):
        game = WordleGame(
            max_guesses=1,
            secret_word="APPLE",
            word_bank=FakeWordBank(["APPLE"]),
            use_color=False,
        )

        game._process_guess("CRANE")

        self.assertFalse(game.is_won)
        self.assertTrue(game.is_lost)
        self.assertEqual(game.guesses_left, 0)

    def test_requires_positive_guess_count(self):
        with self.assertRaises(ValueError):
            WordleGame(max_guesses=0, word_bank=FakeWordBank(["APPLE"]))


if __name__ == "__main__":
    unittest.main()
