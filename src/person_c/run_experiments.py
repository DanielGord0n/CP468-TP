"""
Person C - Testing & Performance Analyst
CP468 Term Project - MIN-CONFLICTS N-Queens

Runs MIN-CONFLICTS (Person A) across multiple N values,
records execution metrics, validates using Person B,
and saves results into CSV files inside the results/ folder.

Metrics collected:
- Execution time
- Number of iterations until solution
- Success rate over multiple runs
- Average conflicts per iteration (where feasible)
- Largest N that solves reliably in "reasonable" time
"""

import os
import sys
import csv
import time

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from person_a.min_conflicts import min_conflicts
from person_b.board_utils import (
    is_solution,
    build_conflict_tables,
    queen_conflicts,
)

N_VALUES = [10, 100, 1000, 10000, 100000, 1000000]
BASE_RUNS_PER_N = 5
REASONABLE_TIME_THRESHOLD = 5.0


def runs_for_n(n: int) -> int:
    """Choose number of runs depending on board size."""
    if n < 10_000:
        return BASE_RUNS_PER_N
    if n < 100_000:
        return 3
    return 1


def max_steps_for_n(n: int) -> int:
    """Scale max_steps to prevent massive runtimes."""
    if n <= 1000:
        return 100_000
    if n <= 10_000:
        return 20_000
    if n <= 100_000:
        return 1000
    return 10


def fmt(value, decimals: int = 6):
    """Format values for CSV without scientific notation."""
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.{decimals}f}"
    return value


def fast_conflict_sum(board):
    """Compute total conflicting queen pairs in O(n)."""
    if board is None:
        return None
    t = build_conflict_tables(board)
    total = 0
    for row in range(len(board)):
        total += queen_conflicts(t, board, row)
    return total // 2


def should_compute_conflicts(n: int) -> bool:
    """Avoid conflict computation for huge N."""
    return n <= 100_000


def run_single_experiment(n: int) -> dict:
    """Run MIN-CONFLICTS once and gather metrics."""
    if should_compute_conflicts(n):
        init_board, _ = min_conflicts(n, max_steps=1)
        initial_conflicts = fast_conflict_sum(init_board)
    else:
        initial_conflicts = None

    max_steps = max_steps_for_n(n)

    start = time.time()
    board, steps = min_conflicts(n, max_steps=max_steps)
    exec_time = time.time() - start

    if should_compute_conflicts(n):
        final_conflicts = fast_conflict_sum(board)
    else:
        final_conflicts = None

    conflict_delta = (
        initial_conflicts - final_conflicts
        if (initial_conflicts is not None and final_conflicts is not None)
        else None
    )

    success = 1 if (board is not None and is_solution(board)) else 0

    time_per_iter = exec_time / steps if steps and steps > 0 else None
    avg_conflicts_per_iter = (
        (final_conflicts / steps)
        if (steps and steps > 0 and final_conflicts is not None)
        else None
    )

    return {
        "iterations": steps,
        "execution_time": exec_time,
        "success": success,
        "initial_conflicts": initial_conflicts,
        "final_conflicts": final_conflicts,
        "conflict_delta": conflict_delta,
        "time_per_iter": time_per_iter,
        "avg_conflicts_per_iter": avg_conflicts_per_iter,
    }


def main():
    """Run experiments and write results to CSV."""
    os.makedirs("results", exist_ok=True)
    print("Running MIN-CONFLICTS experiments...\n")

    largest_reasonable_n = None

    for n in N_VALUES:
        runs = runs_for_n(n)
        filename = f"results/n{n}_results.csv"

        print(f"Running tests for n = {n}...")
        print(f"  Using max_steps = {max_steps_for_n(n)}")
        print(f"  Number of runs = {runs}")
        print(f"  Saving results to {filename}")

        total_success = 0
        total_time = 0.0
        total_steps = 0
        total_avg_conflicts = 0.0
        conflict_samples = 0

        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "run_id", "n", "iterations", "execution_time", "success",
                "initial_conflicts", "final_conflicts", "conflict_delta",
                "avg_conflicts_per_iteration", "time_per_iteration"
            ])

            for run_id in range(1, runs + 1):
                result = run_single_experiment(n)

                writer.writerow([
                    run_id, n,
                    fmt(result["iterations"]),
                    fmt(result["execution_time"]),
                    fmt(result["success"]),
                    fmt(result["initial_conflicts"]),
                    fmt(result["final_conflicts"]),
                    fmt(result["conflict_delta"]),
                    fmt(result["avg_conflicts_per_iter"]),
                    fmt(result["time_per_iter"]),
                ])

                print(
                    f"  Run {run_id}/{runs} -> "
                    f"steps={result['iterations']}, "
                    f"time={result['execution_time']:.4f}s, "
                    f"success={result['success']}"
                )

                total_success += result["success"]
                total_time += result["execution_time"]
                total_steps += result["iterations"]

                if result["avg_conflicts_per_iter"] is not None:
                    total_avg_conflicts += result["avg_conflicts_per_iter"]
                    conflict_samples += 1

        avg_time = total_time / runs
        avg_steps = total_steps / runs
        avg_conflicts = (
            total_avg_conflicts / conflict_samples if conflict_samples > 0 else None
        )

        print(f"\n=== Summary for n = {n} ===")
        print(f"Success rate: {total_success}/{runs}")
        print(f"Average time: {avg_time:.4f}s")
        print(f"Average iterations: {avg_steps:.1f}")
        print(f"Average conflicts/iteration: {avg_conflicts}")
        print("============================\n")

        if avg_time < REASONABLE_TIME_THRESHOLD and total_success == runs:
            largest_reasonable_n = n

    print("\nAll experiments completed!")
    print(
        f"Largest N solved reliably in <{REASONABLE_TIME_THRESHOLD}s: "
        f"{largest_reasonable_n if largest_reasonable_n is not None else 'None'}"
    )


if __name__ == "__main__":
    main()
