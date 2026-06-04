import argparse
import random
from state import State, GOAL_STATE
from search import astar, HEURISTICS
from advisor import advise
from display import print_solution


def random_puzzle(moves: int = 30, seed: int | None = None) -> State:
    rng = random.Random(seed)
    state = State(GOAL_STATE)
    for _ in range(moves):
        successors = state.successors()
        _, state = rng.choice(successors)
    return state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI 8-Puzzle Solver (A*)")
    parser.add_argument(
        "--heuristic",
        choices=list(HEURISTICS.keys()),
        default="manhattan",
        help="Heuristic function for A* (default: manhattan)",
    )
    parser.add_argument(
        "--board",
        nargs=9,
        type=int,
        metavar="N",
        help="Custom board: 9 integers (0=blank), e.g. --board 1 2 3 4 0 5 7 8 6",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for puzzle generation (default: 42)",
    )
    parser.add_argument(
        "--moves",
        type=int,
        default=25,
        help="Number of random shuffling moves (default: 25)",
    )
    parser.add_argument(
        "--no-advisor",
        action="store_true",
        help="Suppress advisor commentary",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.0,
        help="Seconds to pause between steps (default: 0)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.board:
        board = tuple(args.board)
        if sorted(board) != list(range(9)):
            raise SystemExit("--board must contain exactly the digits 0–8 each once.")
        initial = State(board)
    else:
        initial = random_puzzle(moves=args.moves, seed=args.seed)

    advisor_fn = None if args.no_advisor else advise

    path, nodes, elapsed = astar(initial, heuristic_name=args.heuristic)

    print_solution(
        initial,
        path,
        nodes_explored=nodes,
        elapsed=elapsed,
        advisor_fn=advisor_fn,
        step_delay=args.delay,
    )


if __name__ == "__main__":
    main()
