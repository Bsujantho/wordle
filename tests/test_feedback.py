import unittest

from feedback import GRAY, GREEN, YELLOW, feedback_to_pattern, parse_feedback, score_guess


class FeedbackTests(unittest.TestCase):
    def test_score_guess_handles_repeated_letters_in_secret(self):
        self.assertEqual(
            score_guess("ALLEY", "APPLE"),
            (GREEN, YELLOW, GRAY, YELLOW, GRAY),
        )

    def test_score_guess_limits_duplicate_yellows(self):
        self.assertEqual(
            score_guess("LLAMA", "BANAL"),
            (YELLOW, GRAY, YELLOW, GRAY, YELLOW),
        )

    def test_parse_feedback_accepts_short_and_long_forms(self):
        expected = (GREEN, YELLOW, GRAY, GRAY, GREEN)

        self.assertEqual(parse_feedback("GYBBG"), expected)
        self.assertEqual(parse_feedback("green yellow gray grey green"), expected)

    def test_feedback_to_pattern(self):
        self.assertEqual(feedback_to_pattern((GREEN, YELLOW, GRAY, GRAY, GREEN)), "GYBBG")


if __name__ == "__main__":
    unittest.main()
