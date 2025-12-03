"""
visual_test.py

Runs MIN-CONFLICTS on:
  - Small visual tests: n=8 and n=10 (prints board)
  - Then pauses for ENTER
  - Then scale tests: n=100, 1,000, 10,000, 100,000, 1,000,000 (no board printing)

Run from repo root (PowerShell):
  ./venv/Scripts/python.exe visual_test.py

Optional (speeds up validation for huge n by sampling rows if Person B tools exist):
  ./venv/Scripts/python.exe visual_test.py --fast-validate
"""

import os
import sys
import time
import random
from typing import List, Optional, Tuple, Callable

Board = List[int]

# --- Make src imports work if repo uses /src layout ---
REPO_ROOT = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(REPO_ROOT, "src")
if os.path.isdir(SRC_DIR) and SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


def import_solver() -> Callable[..., Tuple[Optional[Board], int]]:
    """Import min_conflicts from either repo root or src/person_a."""
    try:
        from min_conflicts import min_conflicts  # type: ignore
        return min_conflicts
    except Exception:
        pass

    try:
        from person_a.min_conflicts import min_conflicts  # type: ignore
        return min_conflicts
    except Exception as e:
        raise ImportError(
            "Could not import min_conflicts.\n"
            "Expected either:\n"
            "  - min_conflicts.py in repo root, OR\n"
            "  - src/person_a/min_conflicts.py (repo/src on sys.path)\n"
            f"Original error: {e}"
        )


def import_validator_tools():
    """
    Prefer Person B board_utils. If not available, fall back to other is_solution sources.
    Returns:
      is_solution(board)->bool
      build_conflict_tables(board)->tables or None
      queen_conflicts(tables, board, row)->int or None
      get_conflicted_queens(board, tables)->list[int] or None
    """
    try:
        from person_b.board_utils import (  # type: ignore
            is_solution,
            build_conflict_tables,
            queen_conflicts,
            get_conflicted_queens,
        )
        return is_solution, build_conflict_tables, queen_conflicts, get_conflicted_queens
    except Exception:
        pass

    try:
        from board_utils import is_solution  # type: ignore
        return is_solution, None, None, None
    except Exception:
        pass

    try:
        from min_conflicts import is_solution  # type: ignore
        return is_solution, None, None, None
    except Exception:
        pass

    # Last-resort validator (O(n))
    def simple_is_solution(board: Board) -> bool:
        cols = set()
        d1 = set()
        d2 = set()
        for r, c in enumerate(board):
            if c in cols:
                return False
            a = r - c
            b = r + c
            if a in d1 or b in d2:
                return False
            cols.add(c)
            d1.add(a)
            d2.add(b)
        return True

    return simple_is_solution, None, None, None


MIN_CONFLICTS = import_solver()
IS_SOLUTION, BUILD_TABLES, QUEEN_CONFLICTS, GET_CONFLICTED = import_validator_tools()


# ------------------ Visualization (small n only) ------------------
def print_board(board: Board) -> None:
    n = len(board)
    print(f"\nBoard (n={n})  board[row]=col")
    print("    " + " ".join(f"{c:2d}" for c in range(n)))
    for r, c in enumerate(board):
        row = [" ." for _ in range(n)]
        row[c] = " Q"
        print(f"{r:2d}: " + "".join(row))


def print_conflicts_small(board: Board) -> None:
    if BUILD_TABLES is None or QUEEN_CONFLICTS is None:
        return
    t = BUILD_TABLES(board)
    print("\nPer-queen conflicts (should all be 0 on a solution):")
    for r in range(len(board)):
        q = QUEEN_CONFLICTS(t, board, r)
        print(f"  row {r:2d} col {board[r]:2d} -> {q}")
    if GET_CONFLICTED is not None:
        conflicted = GET_CONFLICTED(board, t)
        print(f"Conflicted rows: {conflicted}")


# ------------------ Solver calling / validation ------------------
def call_solver(n: int, max_steps: int, seed: int) -> Tuple[Optional[Board], int]:
    """Try keyword args then fallback to positional."""
    try:
        return MIN_CONFLICTS(n, max_steps=max_steps, random_seed=seed)
    except TypeError:
        return MIN_CONFLICTS(n, max_steps, seed)


def validate(board: Board, fast_validate: bool, seed: int) -> Tuple[bool, str]:
    n = len(board)

    # Fast sampling validation for huge n (only if Person B conflict tools exist)
    if fast_validate and BUILD_TABLES is not None and QUEEN_CONFLICTS is not None and n >= 200_000:
        t = BUILD_TABLES(board)
        rng = random.Random(seed)
        samples = 300
        for _ in range(samples):
            r = rng.randrange(n)
            if QUEEN_CONFLICTS(t, board, r) != 0:
                return False, f"sample conflict at row {r}"
        return True, f"sampled {samples} rows"

    ok = bool(IS_SOLUTION(board))
    return ok, "full is_solution(board)"


def run_test(n: int, max_steps: int, attempts: int, seed0: int, visualize: bool, fast_validate: bool) -> bool:
    print("\n" + "-" * 70)
    print(f"Test: n={n:,}  max_steps={max_steps:,}  attempts={attempts}  seed0={seed0}")
    print("-" * 70)

    for i in range(attempts):
        seed = seed0 + i
        t0 = time.time()
        board, steps = call_solver(n, max_steps=max_steps, seed=seed)
        elapsed = time.time() - t0

        if board is None:
            print(f"  attempt {i+1:2d}: FAIL (no solution) steps={steps:,} time={elapsed:.3f}s seed={seed}")
            continue

        ok, how = validate(board, fast_validate=fast_validate, seed=seed)
        if not ok:
            print(f"  attempt {i+1:2d}: FAIL (invalid)    steps={steps:,} time={elapsed:.3f}s seed={seed} [{how}]")
            continue

        print(f"  attempt {i+1:2d}: PASS              steps={steps:,} time={elapsed:.3f}s seed={seed} [{how}]")

        if visualize:
            print_board(board)
            print_conflicts_small(board)

        return True

    print(f"Result: ✗ FAIL for n={n:,}")
    return False


def main():
    fast_validate = "--fast-validate" in sys.argv

    print("N-Queens Visual + Scale Test Runner")
    print(f"Validator: {getattr(IS_SOLUTION, '__name__', 'is_solution')}")
    if fast_validate:
        print("Mode: --fast-validate enabled (sampling for huge n if tools exist)")

    passed = 0
    total = 0

    # Small visual tests
    small_tests = [
        (8, 100_000, 10),
        (10, 200_000, 20),
    ]

    for n, max_steps, attempts in small_tests:
        total += 1
        if run_test(n, max_steps, attempts, seed0=42, visualize=True, fast_validate=fast_validate):
            passed += 1

    # Pause after n=10 and before n=(100-1M)
    input("\nFinished visual tests (n=8 and n=10). Press ENTER to continue to large-n tests (n>=100)...")

    # Scale tests (no visualization n = 100 to 1,000,000)
    import subprocess

    print("\nRunning benchmark.py (1000 -> 1,000,000)...\n")
    subprocess.run([sys.executable, os.path.join(REPO_ROOT, "benchmark.py")], check=True)

    print("\nBenchmark finished.")
    return

if __name__ == "__main__":
    main()
