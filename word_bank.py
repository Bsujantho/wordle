import random

class WordBank:
    def __init__(self, word_file_path: str):
        self.words = self._load_words(word_file_path)
        self.valid_words = set(self.words)

    def _load_words(self, file_path: str) -> list[str]:
        word_list = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    word = line.strip().upper()
                    # Basic validation to ensure file integrity
                    if len(word) == 5 and word.isalpha():
                        word_list.append(word)

            if not word_list:
                raise ValueError("Word file is empty or contains no valid 5-letter words.")

            return word_list
        except FileNotFoundError:
            raise FileNotFoundError(f"The word file was not found at {file_path}")

    def get_random_word(self) -> str:
        return random.choice(self.words)

    def contains(self, word: str) -> bool:
        return word in self.valid_words
