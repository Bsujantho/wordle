import argparse

from feedback import feedback_to_pattern
from game import WordleGame
from solver import filter_candidates, parse_clue, recommend_guesses
from word_bank import DEFAULT_WORD_FILE, WordBank


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Play Wordle or use the solver helper.")
    parser.add_argument("mode", nargs="?", choices=("play", "solve"), default="play")
    parser.add_argument(
        "--word-file",
        default=None,
        help=f"Path to a newline-delimited word list. Default: {DEFAULT_WORD_FILE.name}",
    )
    parser.add_argument(
        "--max-guesses",
        type=int,
        default=6,
        help="Number of guesses for play mode. Default: 6",
    )
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors.")
    parser.add_argument("--secret-word", default=None, help=argparse.SUPPRESS)
    parser.add_argument(
        "--clue",
        action="append",
        default=[],
        metavar="GUESS:FEEDBACK",
        help="Solver clue, such as CRANE:BBYBG. Repeat for multiple clues.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of solver recommendations to show. Default: 10",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Keep prompting for guesses and feedback in solver mode.",
    )
    return parser


def run_play(args: argparse.Namespace) -> int:
    print("==============================")
    print("   Welcome to Python Wordle   ")
    print("==============================")
    print(f"Guess the 5-letter word in {args.max_guesses} tries.")

    try:
        game = WordleGame(
            args.word_file,
            max_guesses=args.max_guesses,
            secret_word=args.secret_word,
            use_color=not args.no_color,
        )
    except (OSError, ValueError) as error:
        print(f"Could not start game: {error}")
        return 1

    game.play()
    print("\nThanks for playing!")
    return 0


def show_solver_state(candidates: list[str], allowed_guesses: list[str], limit: int) -> None:
    recommendations = recommend_guesses(candidates, allowed_guesses, limit=limit)
    shown_candidates = ", ".join(candidates[:20])
    if len(candidates) > 20:
        shown_candidates += ", ..."

    print(f"Candidates remaining: {len(candidates)}")
    print(f"Candidates: {shown_candidates}")
    print("Recommended guesses:")
    for recommendation in recommendations:
        candidate_note = "candidate" if recommendation.is_candidate else "probe"
        print(
            f"  {recommendation.word} "
            f"(expected {recommendation.expected_remaining:.1f}, "
            f"worst {recommendation.worst_case_remaining}, {candidate_note})"
        )


def run_interactive_solver(candidates: list[str], allowed_guesses: list[str], limit: int) -> None:
    while len(candidates) > 1:
        best_guess = recommend_guesses(candidates, allowed_guesses, limit=1)[0].word
        guess = input(f"Guess used [{best_guess}] or q to quit: ").strip()
        if guess.lower() in {"q", "quit", "exit"}:
            return
        if not guess:
            guess = best_guess

        feedback = input("Feedback (G=green, Y=yellow, B=gray): ").strip()
        try:
            candidates = filter_candidates(candidates, guess, feedback)
        except ValueError as error:
            print(f"Invalid clue: {error}")
            continue

        if not candidates:
            print("No candidates match that feedback.")
            return
        show_solver_state(candidates, allowed_guesses, limit)

    print(f"Answer should be: {candidates[0]}")


def run_solver(args: argparse.Namespace) -> int:
    try:
        word_bank = WordBank(args.word_file)
        candidates = word_bank.words
    except (OSError, ValueError) as error:
        print(f"Could not start solver: {error}")
        return 1

    for clue in args.clue:
        try:
            guess, feedback = parse_clue(clue)
            candidates = filter_candidates(candidates, guess, feedback)
        except ValueError as error:
            print(f"Invalid clue {clue!r}: {error}")
            return 2
        print(f"{guess} {feedback_to_pattern(feedback)} -> {len(candidates)} candidate(s)")

    if not candidates:
        print("No candidate words match those clues.")
        return 1

    show_solver_state(candidates, word_bank.words, args.limit)
    if args.interactive:
        run_interactive_solver(candidates, word_bank.words, args.limit)
    return 0


def main():
    args = build_parser().parse_args()
    if args.mode == "solve":
        return run_solver(args)

    return run_play(args)


if __name__ == "__main__":
    raise SystemExit(main())
