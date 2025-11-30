import time
import pandas as pd
from person_a.min_conflicts import min_conflicts

def measure_n(n, attempts=3):
    """Runs MIN-CONFLICTS a few times and returns avg runtime + iterations."""
    runtimes = []
    iterations = []

    for seed in range(attempts):
        start = time.time()
        board, steps = min_conflicts(n=n, max_steps=200000, random_seed=seed)
        end = time.time()

        runtimes.append(end - start)
        iterations.append(steps)

    return sum(runtimes)/attempts, sum(iterations)/attempts


def main():
    test_sizes = [10, 50, 100, 200, 500, 1000]

    rows = []

    for n in test_sizes:
        print(f"Running MIN-CONFLICTS for n = {n}...")
        avg_time, avg_iters = measure_n(n)

        rows.append({
            "n": n,
            "runtime": avg_time,
            "iterations": avg_iters
        })

    df = pd.DataFrame(rows)
    df.to_csv("results/performance_results.csv", index=False)

    print("\nSaved performance_results.csv to results/")
    print(df)


if __name__ == "__main__":
    main()
