from collections import Counter
from collections.abc import Iterable

WORD_LENGTH = 5

GREEN = "GREEN"
YELLOW = "YELLOW"
GRAY = "GRAY"

FEEDBACK_VALUES = (GREEN, YELLOW, GRAY)
FEEDBACK_TO_SYMBOL = {
    GREEN: "G",
    YELLOW: "Y",
    GRAY: "B",
}

_SINGLE_MARK_ALIASES = {
    "G": GREEN,
    "Y": YELLOW,
    "B": GRAY,
    "X": GRAY,
    "-": GRAY,
    "0": GRAY,
}

_WORD_MARK_ALIASES = {
    "GREEN": GREEN,
    "YELLOW": YELLOW,
    "GRAY": GRAY,
    "GREY": GRAY,
}


def normalize_word(word: str, *, field_name: str = "word") -> str:
    normalized = word.strip().upper()
    if len(normalized) != WORD_LENGTH:
        raise ValueError(f"{field_name} must be exactly {WORD_LENGTH} letters.")
    if not normalized.isalpha():
        raise ValueError(f"{field_name} must contain only letters.")
    return normalized


def score_guess(guess: str, secret_word: str) -> tuple[str, ...]:
    guess = normalize_word(guess, field_name="guess")
    secret_word = normalize_word(secret_word, field_name="secret word")
    feedback = [GRAY] * WORD_LENGTH
    remaining_letters = Counter(secret_word)

    for index, letter in enumerate(guess):
        if letter == secret_word[index]:
            feedback[index] = GREEN
            remaining_letters[letter] -= 1

    for index, letter in enumerate(guess):
        if feedback[index] == GREEN:
            continue
        if remaining_letters[letter] > 0:
            feedback[index] = YELLOW
            remaining_letters[letter] -= 1

    return tuple(feedback)


def parse_feedback(pattern: str) -> tuple[str, ...]:
    raw_pattern = pattern.strip().upper()
    compact_pattern = raw_pattern.replace(" ", "").replace(",", "")

    if (
        len(compact_pattern) == WORD_LENGTH
        and all(mark in _SINGLE_MARK_ALIASES for mark in compact_pattern)
    ):
        return tuple(_SINGLE_MARK_ALIASES[mark] for mark in compact_pattern)

    tokens = raw_pattern.replace(",", " ").split()
    if len(tokens) != WORD_LENGTH:
        raise ValueError(
            "feedback must be five marks, such as GYBBG or GREEN YELLOW GRAY GRAY GREEN."
        )

    try:
        return tuple(_WORD_MARK_ALIASES[token] for token in tokens)
    except KeyError as error:
        raise ValueError(
            "feedback marks must be G, Y, B, X, GREEN, YELLOW, GRAY, or GREY."
        ) from error


def feedback_to_pattern(feedback: Iterable[str]) -> str:
    values = tuple(feedback)
    if len(values) != WORD_LENGTH:
        raise ValueError(f"feedback must contain {WORD_LENGTH} marks.")

    try:
        return "".join(FEEDBACK_TO_SYMBOL[value] for value in values)
    except KeyError as error:
        raise ValueError(f"unknown feedback mark: {error.args[0]}") from error
