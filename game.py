from collections import Counter
from word_bank import WordBank
import string

class WordleGame:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    GRAY = '\033[90m'
    RESET = '\033[0m'
    CLEAR_SCREEN = '\033[2J\033[H'

    def __init__(self, word_file_path="words_generated.txt", max_guesses: int =6):
        self.word_bank = WordBank(word_file_path)
        self.secret_word = self.word_bank.get_random_word()
        self.max_guesses = max_guesses
        self.guesses_left = max_guesses
        self.guesses = []
        self.is_won = False
        self.letter_states = {letter: 'UNKNOWN' for letter in string.ascii_uppercase}

    def _get_user_guess(self) -> str:
        while True:
            guess = input("Enter your guess: ").strip().upper()
            if len(guess) != 5:
                print("Invalid guess. Please enter a 5-letter word.")
            elif not guess.isalpha():
                print("Invalid guess. Please use only letters.")
            elif not self.word_bank.contains(guess):
                print("Not in word list.")
            else:
                return guess

    def _update_letter_states(self, guess: str, feedback: list[str]):
        for letter, status in zip(guess, feedback):
            current_status = self.letter_states[letter]
            if status == 'GREEN':
                self.letter_states[letter] = 'GREEN'
            elif status == 'YELLOW':
                if current_status != 'GREEN':
                    self.letter_states[letter] = 'YELLOW'
            elif status == 'GRAY':
                if current_status == 'UNKNOWN':
                     self.letter_states[letter] = 'GRAY'

    def _process_guess(self, guess: str):
        feedback = [''] * 5
        secret_word_counts = Counter(self.secret_word)

        # First pass for GREEN
        for i, letter in enumerate(guess):
            if letter == self.secret_word[i]:
                feedback[i] = 'GREEN'
                secret_word_counts[letter] -= 1

        # Second pass for YELLOW/GRAY
        for i, letter in enumerate(guess):
            if feedback[i] == '': # Not already marked as GREEN
                if secret_word_counts[letter] > 0:
                    feedback[i] = 'YELLOW'
                    secret_word_counts[letter] -= 1
                else:
                    feedback[i] = 'GRAY'
        
        self.guesses.append((guess, feedback))
        self._update_letter_states(guess, feedback)
        self.guesses_left -= 1
        if guess == self.secret_word:
            self.is_won = True
            
    def _display_board(self):
        print(self.CLEAR_SCREEN)
        print("Python Wordle")
        print("="*20)
        for guess, feedback in self.guesses:
            colored_guess = ""
            for i, letter in enumerate(guess):
                if feedback[i] == 'GREEN':
                    colored_guess += f"{self.GREEN}{letter}{self.RESET} "
                elif feedback[i] == 'YELLOW':
                    colored_guess += f"{self.YELLOW}{letter}{self.RESET} "
                else:
                    colored_guess += f"{self.GRAY}{letter}{self.RESET} "
            print(colored_guess.strip())

        for _ in range(self.guesses_left):
            print("_ _ _ _ _")

        print("\n" + self._format_keyboard())
        print(f"\nGuesses remaining: {self.guesses_left}")
        print("="*20 + "\n")

    def _format_keyboard(self) -> str:
        # QWERTY layout
        rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        formatted_rows = []
        for row in rows:
            formatted_row = ""
            for letter in row:
                status = self.letter_states[letter]
                if status == 'GREEN':
                    formatted_row += f"{self.GREEN}{letter}{self.RESET} "
                elif status == 'YELLOW':
                    formatted_row += f"{self.YELLOW}{letter}{self.RESET} "
                elif status == 'GRAY':
                    formatted_row += f"{self.GRAY}{letter}{self.RESET} "
                else:
                    formatted_row += f"{letter} "
            formatted_rows.append(formatted_row.strip())
        return "\n".join(formatted_rows)

    def play(self):
        while self.guesses_left > 0 and not self.is_won:
            self._display_board()
            user_guess = self._get_user_guess()
            self._process_guess(user_guess)

        self._display_board()
        if self.is_won:
            print(f"{self.GREEN}Congratulations! You guessed the word: {self.secret_word}{self.RESET}")
        else:
            print(f"Sorry, you ran out of guesses. The word was: {self.secret_word}")
