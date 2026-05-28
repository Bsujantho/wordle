# Python Wordle

A small terminal Wordle clone with a built-in solver helper. The game ships with a tracked `words.txt`, so it works immediately after cloning and does not depend on a generated local word file.

## Play

```bash
python main.py
```

You get six guesses to find the five-letter secret word. Guesses are scored with standard Wordle colors:

- `G` / green: correct letter in the correct spot
- `Y` / yellow: correct letter in another spot
- `B` / gray: letter is not used in the answer

Useful play options:

```bash
python main.py --max-guesses 8
python main.py --word-file path/to/words.txt
python main.py --no-color
```

## Solver Mode

Use solver mode when you are playing a Wordle puzzle elsewhere and want suggested guesses.

```bash
python main.py solve
python main.py solve --clue CRANE:BBBBY --limit 5
python main.py solve --clue CRANE:BBBBY --clue PILOT:BYBBB
python main.py solve --interactive
```

Clues use `GUESS:FEEDBACK`. Feedback can be compact (`GYBBG`) or written out (`GREEN YELLOW GRAY GRAY GREEN`). `B`, `X`, `GRAY`, and `GREY` all mean a gray tile.

Recommendations are ranked by the expected number of possible answers left after the guess. Solver output labels guesses as:

- `candidate`: still a possible answer
- `probe`: useful for information, but not currently a possible answer

## Tests

Run the test suite with the standard library:

```bash
python -m unittest discover -s tests
```

The tests cover repeated-letter scoring, game win/loss state, word-bank validation, and solver candidate filtering.

## Word List

The app uses the tracked `words.txt` by default. To regenerate it from NLTK's word corpus:

```bash
pip install -r requirements.txt
python words.py
```

`requirements.txt` is only needed for regenerating the word list; playing the game and running tests use the Python standard library.

## Project Layout

- `main.py`: command-line entry point for play and solver modes
- `game.py`: interactive game loop and board display
- `feedback.py`: shared Wordle scoring and feedback parsing
- `solver.py`: candidate filtering and guess recommendations
- `word_bank.py`: word-list loading and validation
- `words.py`: optional NLTK-based word-list generator
- `tests/`: unit tests
