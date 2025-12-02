"""
main.py - N-Queens Solver (Min-Conflicts)

This script solves the N-Queens problem using an optimized Min-Conflicts algorithm.
It supports both command-line arguments and interactive mode.

Usage:
    python3 main.py              # Interactive mode
    python3 main.py --n 1000     # Solve for N=1000
"""

import argparse
import time
import sys
from typing import Optional

# Import core logic
from src.person_a.min_conflicts import min_conflicts
from src.person_b.board_utils import is_solution
from src.person_d.visualizer import (
    visualize_board,
    board_row_to_col,
)

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

    start = time.time()
    board, steps = min_conflicts(n=n, max_steps=max_steps, random_seed=seed)
    end = time.time()
    runtime = end - start

    if board is None:
        print(f"✗ Failed to find solution within {steps} steps.")
        print(f"  Time: {runtime:.4f}s")
        return

    # Validate solution
    valid = is_solution(board)
    status_icon = "✓" if valid else "✗"
    status_text = "Valid" if valid else "Invalid"

    print(f"{status_icon} Solution found!")
    print(f"  Steps: {steps:,}")
    print(f"  Time:  {runtime:.4f}s")
    print(f"  Check: {status_text}")

    # Visualization
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

def get_user_input() -> int:
    """Prompt user for N."""
    while True:
        try:
            val = input("\nEnter number of queens (N): ").strip()
            if not val:
                continue
            n = int(val)
            if n < 4:
                print("N must be at least 4.")
                continue
            return n
        except ValueError:
            print("Invalid input. Please enter an integer.")

def main() -> None:
    parser = argparse.ArgumentParser(description="N-Queens Solver")
    parser.add_argument("--n", type=int, help="Number of queens")
    parser.add_argument("--visualize", action="store_true", help="Visualize solution (for N <= 100)")
    parser.add_argument("--max-steps", type=int, default=10_000_000, help="Max steps")
    parser.add_argument("--seed", type=int, help="Random seed")
    
    args = parser.parse_args()

    if args.n is not None:
        # Command line mode
        run_solver(args.n, args.visualize, args.max_steps, args.seed)
    else:
        # Interactive mode
        print("=== N-Queens Solver ===")
        try:
            while True:
                n = get_user_input()
                
                # Ask for visualization if N is small
                vis = False
                if n <= 100:
                    v_input = input("Visualize solution? (y/N): ").strip().lower()
                    if v_input == 'y':
                        vis = True
                
                run_solver(n, visualize=vis, max_steps=args.max_steps, seed=args.seed)
                
                again = input("\nSolve another? (y/N): ").strip().lower()
                if again != 'y':
                    break
        except KeyboardInterrupt:
            print("\nExiting.")

if __name__ == "__main__":
    main()
