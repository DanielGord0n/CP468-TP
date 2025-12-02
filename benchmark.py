"""
benchmark.py - Performance Benchmark for N-Queens Solver

Runs the solver for N = 1,000, 10,000, 100,000, and 1,000,000.
Outputs a performance table.
"""

import time
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.person_a.min_conflicts import min_conflicts

def run_benchmark(n, max_steps):
    start = time.time()
    board, steps = min_conflicts(n, max_steps=max_steps, random_seed=42)
    end = time.time()
    runtime = end - start
    
    status = "Success" if board else "Failed"
    return runtime, steps, status

def main():
    sizes = [1_000, 10_000, 100_000, 1_000_000]
    
    print("\nRunning Benchmarks...")
    print("=" * 60)
    print(f"{'N':<12} | {'Time (s)':<12} | {'Steps':<12} | {'Status':<10}")
    print("-" * 60)
    
    for n in sizes:
        # Use 5*n steps as a safe upper bound for O(n) algorithm
        max_steps = n * 10
        if max_steps < 100_000: max_steps = 100_000
        
        runtime, steps, status = run_benchmark(n, max_steps)
        
        print(f"{n:<12,} | {runtime:<12.4f} | {steps:<12,} | {status:<10}")
        
    print("=" * 60)
    print("Benchmark Complete.\n")

if __name__ == "__main__":
    main()
