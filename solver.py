from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from feedback import parse_feedback, score_guess, normalize_word


@dataclass(frozen=True)
class GuessRecommendation:
    word: str
    expected_remaining: float
    worst_case_remaining: int
    is_candidate: bool


def parse_clue(clue: str) -> tuple[str, tuple[str, ...]]:
    if ":" in clue:
        guess, feedback = clue.split(":", 1)
    elif "=" in clue:
        guess, feedback = clue.split("=", 1)
    else:
        raise ValueError("clues must use GUESS:FEEDBACK, for example CRANE:BBYBG.")

    return normalize_word(guess, field_name="guess"), parse_feedback(feedback)


def filter_candidates(
    candidates: Iterable[str],
    guess: str,
    feedback: str | Iterable[str],
) -> list[str]:
    normalized_guess = normalize_word(guess, field_name="guess")
    expected_feedback = (
        parse_feedback(feedback) if isinstance(feedback, str) else tuple(feedback)
    )

    return [
        normalize_word(candidate)
        for candidate in candidates
        if score_guess(normalized_guess, candidate) == expected_feedback
    ]


def apply_clues(candidates: Iterable[str], clues: Iterable[str]) -> list[str]:
    remaining_candidates = [normalize_word(candidate) for candidate in candidates]
    for clue in clues:
        guess, feedback = parse_clue(clue)
        remaining_candidates = filter_candidates(remaining_candidates, guess, feedback)
    return remaining_candidates


def recommend_guesses(
    candidates: Iterable[str],
    allowed_guesses: Iterable[str] | None = None,
    *,
    limit: int = 10,
) -> list[GuessRecommendation]:
    candidate_words = sorted({normalize_word(candidate) for candidate in candidates})
    if not candidate_words:
        return []

    allowed_words = (
        sorted({normalize_word(guess) for guess in allowed_guesses})
        if allowed_guesses is not None
        else candidate_words
    )
    candidate_set = set(candidate_words)
    recommendations = []

    for guess in allowed_words:
        partitions = Counter(score_guess(guess, answer) for answer in candidate_words)
        expected_remaining = sum(size * size for size in partitions.values()) / len(
            candidate_words
        )
        recommendations.append(
            GuessRecommendation(
                word=guess,
                expected_remaining=expected_remaining,
                worst_case_remaining=max(partitions.values()),
                is_candidate=guess in candidate_set,
            )
        )

    recommendations.sort(
        key=lambda item: (
            item.expected_remaining,
            item.worst_case_remaining,
            not item.is_candidate,
            item.word,
        )
    )
    return recommendations[:limit]
