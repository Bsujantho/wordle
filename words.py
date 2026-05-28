from pathlib import Path

import nltk

OUTPUT_FILE = Path(__file__).with_name("words.txt")


def main() -> None:
    nltk.download("words", quiet=True)
    from nltk.corpus import words

    five_letter_words = sorted(
        {
            word.upper()
            for word in words.words()
            if len(word) == 5 and word.isalpha()
        }
    )

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        for word in five_letter_words:
            file.write(f"{word}\n")

    print(f"Generated {OUTPUT_FILE} with {len(five_letter_words)} words.")


if __name__ == "__main__":
    main()
