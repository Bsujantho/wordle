from game import WordleGame
import os
import words

def main():
    """
    The main entry point for the Wordle game application.
    """
    print("==============================")
    print("   Welcome to Python Wordle   ")
    print("==============================")
    print("Guess the 5-letter word in 6 tries.")

    word_file = "words_generated.txt"

    if not os.path.exists(word_file):
        print(f"Word file '{word_file}' not found. Generating it now...")
        try:
            words.generate_word_list(word_file)
        except Exception as e:
            print(f"Failed to generate word list: {e}")
            return

    try:
        game = WordleGame(word_file)
        game.play()
    except Exception as e:
        print(f"\nAn error occurred while running the game: {e}")

    print("\nThanks for playing!")

if __name__ == "__main__":
    main()
