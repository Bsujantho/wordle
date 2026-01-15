import nltk
from nltk.corpus import words
import os

def generate_word_list(output_file='words_generated.txt'):
    print("Downloading word list...")
    nltk.download('words', quiet=True)

    five_letter_words = sorted(list(set(
        [word.upper() for word in words.words() if len(word) == 5]
    )))

    with open(output_file, 'w') as f:
        for word in five_letter_words:
            f.write(f"{word}\n")

    print(f"Generated a file with {len(five_letter_words)} words at {output_file}.")

if __name__ == "__main__":
    generate_word_list()
