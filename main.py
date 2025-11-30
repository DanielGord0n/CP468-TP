"""
main.py - Integration script for CP468 N-Queens MIN-CONFLICTS project.
Person E – Documentation & Integration Manager

This script is the main entry point for:
- Running a single MIN-CONFLICTS run for a given n (Person A + B + D)
- Optionally visualizing the board (Person D)
- Running the full experiment pipeline over all required n values (Person C)
"""

import argparse
import time
from typing import Optional

# ---- Person A: MIN-CONFLICTS algorithm ----
from src.person_a.min_conflicts import min_conflicts

# ---- Person B: board validation ----
from src.person_b.board_utils import is_solution

# ---- Person D: visualization ----
from src.person_d.visualizer import (
    visualize_board,
    board_row_to_col,
)

# ---- Person C: full experiment pipeline ----
from src.person_c.run_experiments import main as run_experiments_main


def run_single(
    n: int,
    visualize: bool = False,
    max_steps: int = 100_000,
    seed: Optional[int] = None,
) -> None:
    """
    Run MIN-CONFLICTS once for a given n and optionally visualize the solution.
    """
    print(f"\n=== Single MIN-CONFLICTS run for n = {n} ===")

    start = time.time()
    board, steps = min_conflicts(n=n, max_steps=max_steps, random_seed=seed)
    end = time.time()
    runtime = end - start

    if board is None:
        print(f"✗ No solution found within {steps} steps.")
        print(f"Runtime: {runtime:.4f} seconds")
        return

    # board is in Person A's format: index = row, value = col
    valid = is_solution(board)

    print(f"✓ Solution found in {steps} steps")
    print(f"✓ Valid solution (Person B check): {valid}")
    print(f"Runtime: {runtime:.4f} seconds")

    # For small n, show the board
    if n <= 20:
        print(f"Board (row -> col): {board}")

    if visualize and n <= 100:
        try:
            # Convert row->col to col->row for the visualizer
            board_for_vis = board_row_to_col(board)
            visualize_board(board_for_vis, n=n, show=True, save=True)
        except Exception as e:
            print(f"[WARN] Visualization failed: {e}")


def run_all_experiments() -> None:
    """
    Run the full experiment pipeline defined by Person C.

    This will:
    - Run MIN-CONFLICTS for all required n-values
    - Validate solutions
    - Record detailed metrics into CSV files under results/
    - Print summaries to the console

    All logic is delegated to src/person_c/run_experiments.py.
    """
    print("\n=== Running full experiment pipeline (Person C) ===\n")
    run_experiments_main()
    print("\n=== Experiment pipeline finished ===\n")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CP468 N-Queens with MIN-CONFLICTS – Integration Script (Person E)"
    )

    parser.add_argument(
        "--n",
        type=int,
        default=10,
        help="Board size n for a single run (default: 10).",
    )

    parser.add_argument(
        "--run-all",
        action="store_true",
        help="Run the full experiment pipeline defined by Person C.",
    )

    parser.add_argument(
        "--visualize",
        action="store_true",
        help="Visualize the solution for a single run (recommended only for small n <= 100).",
    )

    parser.add_argument(
        "--max-steps",
        type=int,
        default=100_000,
        help="Maximum number of steps for MIN-CONFLICTS in a single run (default: 100000).",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed for a single MIN-CONFLICTS run.",
    )

    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.run_all:
        run_all_experiments()
    else:
        run_single(
            n=args.n,
            visualize=args.visualize,
            max_steps=args.max_steps,
            seed=args.seed,
        )


if __name__ == "__main__":
    main()
