from feedback import GREEN, YELLOW, normalize_word, score_guess
from word_bank import WordBank


class WordleGame:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    GRAY = '\033[90m'
    RESET = '\033[0m'

    def __init__(
        self,
        word_file_path: str | None = None,
        max_guesses: int = 6,
        secret_word: str | None = None,
        word_bank: WordBank | None = None,
        use_color: bool = True,
    ):
        if max_guesses < 1:
            raise ValueError("max_guesses must be at least 1.")

        self.word_bank = word_bank or WordBank(word_file_path)
        self.secret_word = (
            normalize_word(secret_word, field_name="secret word")
            if secret_word
            else self.word_bank.get_random_word()
        )
        self.max_guesses = max_guesses
        self.guesses_left = max_guesses
        self.guesses = []
        self.is_won = False
        self.is_lost = False
        self.use_color = use_color

    def _get_user_guess(self) -> str:
        while True:
            guess = input("Enter your guess: ")
            try:
                return normalize_word(guess, field_name="guess")
            except ValueError as error:
                print(f"Invalid guess. {error}")

    def _process_guess(self, guess: str):
        normalized_guess = normalize_word(guess, field_name="guess")
        feedback = score_guess(normalized_guess, self.secret_word)

        self.guesses.append((normalized_guess, feedback))
        self.guesses_left -= 1
        if normalized_guess == self.secret_word:
            self.is_won = True
        elif self.guesses_left == 0:
            self.is_lost = True

        return feedback

    def _format_letter(self, letter: str, feedback: str) -> str:
        if not self.use_color:
            return letter
        if feedback == GREEN:
            return f"{self.GREEN}{letter}{self.RESET}"
        if feedback == YELLOW:
            return f"{self.YELLOW}{letter}{self.RESET}"
        return f"{self.GRAY}{letter}{self.RESET}"
            
    def _display_board(self):

        print("\n" + "="*20)
        for guess, feedback in self.guesses:
            colored_guess = ""
            for i, letter in enumerate(guess):
                colored_guess += f"{self._format_letter(letter, feedback[i])} "
            print(colored_guess.strip())

        for _ in range(self.guesses_left):
            print("_ _ _ _ _")
        print(f"Guesses remaining: {self.guesses_left}")
        print("="*20 + "\n")

    def play(self):

        while self.guesses_left > 0 and not self.is_won:
            self._display_board()
            user_guess = self._get_user_guess()
            self._process_guess(user_guess)

        self._display_board()
        if self.is_won:
            message = f"Congratulations! You guessed the word: {self.secret_word}"
            if self.use_color:
                message = f"{self.GREEN}{message}{self.RESET}"
            print(message)
        else:
            print(f"Sorry, you ran out of guesses. The word was: {self.secret_word}")

