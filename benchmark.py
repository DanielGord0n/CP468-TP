
import time
import random
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.person_a.min_conflicts import min_conflicts

def run_benchmark(n, max_steps=100000):
    print(f"Benchmarking n={n}...")
    start = time.time()
    board, steps = min_conflicts(n, max_steps=max_steps, random_seed=42)
    end = time.time()
    print(f"  Time: {end - start:.4f}s")
    print(f"  Steps: {steps}")
    if board:
        print("  Result: Success")
    else:
        print("  Result: Failed")

if __name__ == "__main__":
    sizes = [1000, 10000, 100000, 1000000]
    for n in sizes:
        run_benchmark(n, max_steps=n*5)
