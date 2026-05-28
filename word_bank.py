from pathlib import Path
import random

from feedback import normalize_word

DEFAULT_WORD_FILE = Path(__file__).with_name("words.txt")


class WordBank:
    def __init__(self, word_file_path: str | Path | None = None, rng=None):
        self.word_file_path = Path(word_file_path) if word_file_path else DEFAULT_WORD_FILE
        self.rng = rng or random
        self.words = self._load_words(self.word_file_path)
        self._word_set = set(self.words)

    def _load_words(self, file_path: Path) -> list[str]:
        word_list = []
        seen_words = set()

        if not file_path.exists():
            raise FileNotFoundError(f"Word file was not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                raw_word = line.strip()
                if not raw_word or raw_word.startswith("#"):
                    continue

                try:
                    word = normalize_word(raw_word, field_name=f"word on line {line_number}")
                except ValueError as error:
                    raise ValueError(f"{file_path}: {error}") from error

                if word not in seen_words:
                    word_list.append(word)
                    seen_words.add(word)

        if not word_list:
            raise ValueError(f"Word file has no usable words: {file_path}")

        return word_list

    def get_random_word(self) -> str:
        return self.rng.choice(self.words)

    def contains(self, word: str) -> bool:
        try:
            return normalize_word(word) in self._word_set
        except ValueError:
            return False

    def __contains__(self, word: str) -> bool:
        return self.contains(word)
