"""
Person B - run_tests.py

- run Person A's solver
- validate using Person B's is_solution
"""

import os
import sys
import time

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from person_a.min_conflicts import min_conflicts
from person_b.board_utils import is_solution


def run_test(n, max_steps=100000, seed=42):
    print(f"\nTest: n={n}")
    start = time.time()

    board, steps = min_conflicts(n, max_steps=max_steps, random_seed=seed)

    elapsed = time.time() - start

    if board is None:
        print(f"FAIL: no solution (steps={steps}, time={elapsed:.3f}s)")
        return False

    if not is_solution(board):
        print(f"FAIL: returned board is not a solution (steps={steps}, time={elapsed:.3f}s)")
        return False

    print(f"PASS: solved in {steps} steps (time={elapsed:.3f}s)")
    return True


def main():
    print("Person B is_solved tests - Using Person A's min_conflicts solver")

    tests = [10, 100, 1000, 10000]
    passed = 0

    for n in tests:
        if run_test(n):
            passed += 1

    print(f"\nSummary: {passed}/{len(tests)} tests passed.")
    if passed != len(tests):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
