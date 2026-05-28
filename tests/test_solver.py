import unittest

from solver import filter_candidates, parse_clue, recommend_guesses


class SolverTests(unittest.TestCase):
    def test_filter_candidates_matches_feedback(self):
        candidates = ["APPLE", "CRANE", "BRICK"]

        self.assertEqual(filter_candidates(candidates, "ALLEY", "GYBYB"), ["APPLE"])

    def test_parse_clue_accepts_colon_and_equals(self):
        self.assertEqual(parse_clue("crane:bbbbb"), parse_clue("CRANE=BBBBB"))

    def test_recommend_guesses_prefers_candidate_when_scores_tie(self):
        recommendations = recommend_guesses(["APPLE"], ["CRANE", "APPLE"], limit=2)

        self.assertEqual(recommendations[0].word, "APPLE")
        self.assertTrue(recommendations[0].is_candidate)
        self.assertEqual(recommendations[0].expected_remaining, 1.0)


if __name__ == "__main__":
    unittest.main()
