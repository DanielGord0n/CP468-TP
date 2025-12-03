"""
main.py - N-Queens Solver (Min-Conflicts)

This script solves the N-Queens problem using an optimized Min-Conflicts algorithm.
It supports both command-line arguments and interactive mode.

Usage:
    python3 main.py              # Interactive mode
    python3 main.py --n 1000     # Solve for N=1000
"""

import argparse
import os
import sys
import time
import random
import subprocess
from typing import Optional, List, Tuple

# Import core logic (project structure)
from src.person_a.min_conflicts import min_conflicts
from src.person_b.board_utils import is_solution

# Optional: Person B conflict helpers (for per-queen conflict print in demo)
try:
    from src.person_b.board_utils import build_conflict_tables, queen_conflicts, get_conflicted_queens
except Exception:
    build_conflict_tables = None
    queen_conflicts = None
    get_conflicted_queens = None

# Visualization (Person D)
from src.person_d.visualizer import (
    visualize_board,
    board_row_to_col,
)

Board = List[int]
REPO_ROOT = os.path.abspath(os.path.dirname(__file__))


def safe_input(prompt: str) -> str:
    """
    Input that won't explode in non-interactive runners (read-only output panels).
    """
    try:
        return input(prompt)
    except EOFError:
        print("\n(no interactive input available — continuing)")
        return ""
    except KeyboardInterrupt:
        print("\n(interrupted at prompt — continuing)")
        return ""


# ------------------ ASCII visualization for small N (demo mode) ------------------
def print_ascii_board(board: Board) -> None:
    n = len(board)
    print(f"\nBoard (n={n})  board[row]=col")
    print("    " + " ".join(f"{c:2d}" for c in range(n)))
    for r, c in enumerate(board):
        row = [" ." for _ in range(n)]
        row[c] = " Q"
        print(f"{r:2d}: " + "".join(row))


def print_per_queen_conflicts(board: Board) -> None:
    if build_conflict_tables is None or queen_conflicts is None:
        return

    t = build_conflict_tables(board)
    print("\nPer-queen conflicts (should all be 0 on a solution):")
    for r in range(len(board)):
        q = queen_conflicts(t, board, r)
        print(f"  row {r:2d} col {board[r]:2d} -> {q}")

    if get_conflicted_queens is not None:
        conflicted = get_conflicted_queens(board, t)
        print(f"Conflicted rows: {conflicted}")


# ------------------ Core solve helpers ------------------
def solve_once(n: int, max_steps: int, seed: Optional[int]) -> Tuple[Optional[Board], int, float]:
    start = time.time()
    board, steps = min_conflicts(n=n, max_steps=max_steps, random_seed=seed)
    runtime = time.time() - start
    return board, steps, runtime


def run_solver(
    n: int,
    visualize: bool = False,
    max_steps: int = 10_000_000,
    seed: Optional[int] = None,
) -> None:
    """
    Run the solver for a given n and print results.
    """
    print(f"\nSolving {n}-Queens...")
    print("-" * 30)

    board, steps, runtime = solve_once(n, max_steps=max_steps, seed=seed)

    if board is None:
        print(f"[FAIL] No solution within {steps} steps.")
        print(f"  Time: {runtime:.4f}s")
        return

    valid = is_solution(board)
    status_text = "Valid" if valid else "Invalid"
    status = "[OK]" if valid else "[FAIL]"

    print(f"{status} Solution found!")
    print(f"  Steps: {steps:,}")
    print(f"  Time:  {runtime:.4f}s")
    print(f"  Check: {status_text}")

    # Graphical visualization using Person D tools
    if visualize:
        if n > 100:
            print("\n[INFO] Visualization skipped (N > 100 is too large to plot).")
        else:
            print("\nGenerating visualization...")
            try:
                # Convert row->col to col->row for the visualizer
                board_for_vis = board_row_to_col(board)
                visualize_board(board_for_vis, n=n, show=True, save=True)
            except Exception as e:
                print(f"[WARN] Visualization failed: {e}")


# ------------------ DEMO mode (visual tests + benchmark) ------------------
def run_demo(max_steps: int, seed: Optional[int], fast_validate: bool) -> None:
    """
    Inlines the visual_test behavior:
      - small ASCII visual tests (8, 10)
      - pause
      - run benchmark.py (1000 -> 1,000,000)

    fast_validate is currently a placeholder here (benchmark handles its own logic).
    """
    print("=== DEMO MODE: Visual Tests + Benchmark ===")
    print("Small N will be printed as a board. Large N will not be visualized.\n")

    seed0 = 42 if seed is None else seed

    small_tests = [
        (8, 100_000, 10),
        (10, 200_000, 20),
    ]

    for (n, steps_limit, attempts) in small_tests:
        print("\n" + "-" * 70)
        print(f"Test: n={n}  max_steps={steps_limit:,}  attempts={attempts}  seed0={seed0}")
        print("-" * 70)

        passed = False
        for i in range(attempts):
            this_seed = seed0 + i
            board, steps, runtime = solve_once(n, max_steps=steps_limit, seed=this_seed)

            if board is None:
                print(f"  attempt {i+1:2d}: FAIL  steps={steps:,}  time={runtime:.3f}s  seed={this_seed}")
                continue

            ok = is_solution(board)
            if not ok:
                print(f"  attempt {i+1:2d}: FAIL (invalid) steps={steps:,} time={runtime:.3f}s seed={this_seed}")
                continue

            print(f"  attempt {i+1:2d}: PASS  steps={steps:,}  time={runtime:.3f}s  seed={this_seed} [is_solution]")
            print_ascii_board(board)
            print_per_queen_conflicts(board)
            passed = True
            break

        if not passed:
            print(f"Result: FAIL for n={n}")

    safe_input("\nFinished visual tests (n=8 and n=10). Press ENTER to run benchmark (1000 -> 1,000,000)...")

    bench_path = os.path.join(REPO_ROOT, "benchmark.py")
    if not os.path.exists(bench_path):
        print(f"\n[FAIL] benchmark.py not found at: {bench_path}")
        return

    print("\nRunning benchmark.py (1000 -> 1,000,000)...\n")

    try:
        # -u ensures output prints live
        subprocess.run([sys.executable, "-u", bench_path], check=True)
    except KeyboardInterrupt:
        print("\nBenchmark interrupted by user (Ctrl+C). Exiting cleanly.")
        return
    except subprocess.CalledProcessError as e:
        print(f"\nBenchmark failed (exit code {e.returncode}). Exiting cleanly.")
        return

    print("\nBenchmark finished.")


# ------------------ Interactive input ------------------
def get_user_input() -> int:
    """
    Prompt user for N.
    Special input:
      - 'demo' runs demo mode (returns -1 sentinel)
      - 'q' quits (raises KeyboardInterrupt to exit loop)
    """
    while True:
        val = safe_input("\nEnter number of queens (N) or type 'demo' (or 'q' to quit): ").strip().lower()
        if not val:
            continue
        if val == "demo":
            return -1
        if val == "q":
            raise KeyboardInterrupt

        try:
            n = int(val)
            if n < 4:
                print("N must be at least 4.")
                continue
            return n
        except ValueError:
            print("Invalid input. Please enter an integer or 'demo'.")


def main() -> None:
    parser = argparse.ArgumentParser(description="N-Queens Solver")
    parser.add_argument("--n", type=int, help="Number of queens")
    parser.add_argument("--visualize", action="store_true", help="Visualize solution (for N <= 100)")
    parser.add_argument("--max-steps", type=int, default=10_000_000, help="Max steps")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--demo", action="store_true", help="Run demo: n=8,10 ASCII + benchmark (1000->1,000,000)")
    parser.add_argument("--fast-validate", action="store_true", help="(Optional) Hint for fast validation (if supported)")

    args = parser.parse_args()

    # Demo mode
    if args.demo:
        run_demo(max_steps=args.max_steps, seed=args.seed, fast_validate=args.fast_validate)
        return

    # Command line mode
    if args.n is not None:
        run_solver(args.n, args.visualize, args.max_steps, args.seed)
        return

    # Interactive mode
    print("=== N-Queens Solver ===")
    try:
        while True:
            n = get_user_input()

            if n == -1:
                # Run demo suite from interactive mode
                run_demo(max_steps=args.max_steps, seed=args.seed, fast_validate=args.fast_validate)
                again = safe_input("\nBack to interactive solver? (y/N): ").strip().lower()
                if again != "y":
                    break
                continue

            vis = False
            if n <= 100:
                v_input = safe_input("Visualize solution? (y/N): ").strip().lower()
                if v_input == "y":
                    vis = True

            run_solver(n, visualize=vis, max_steps=args.max_steps, seed=args.seed)

            again = safe_input("\nSolve another? (y/N): ").strip().lower()
            if again != "y":
                break
    except KeyboardInterrupt:
        print("\nExiting.")


if __name__ == "__main__":
    main()