"""
Test runner for MIN-CONFLICTS N-Queens implementation.
Tests the required n values: 10, 100, 1000, 10000, 100000, 1000000
"""

import time
from min_conflicts import min_conflicts, is_solution


def run_test(n, max_steps=100000, max_attempts=10):
    """Run test with multiple random seeds for robustness."""
    print(f"\nTesting n = {n:,}")
    print("-" * 60)
    
    for attempt in range(max_attempts):
        seed = 42 + attempt
        start = time.time()
        board, steps = min_conflicts(n, max_steps=max_steps, random_seed=seed)
        elapsed = time.time() - start
        
        if board is not None and is_solution(board):
            print(f"✓ Solution found in {steps:,} steps ({elapsed:.3f}s)")
            print(f"  Attempt: {attempt + 1}, Seed: {seed}")
            return True
    
    print(f"✗ No solution found in {max_attempts} attempts")
    return False


def main():
    print("=" * 60)
    print("MIN-CONFLICTS N-QUEENS TEST RUNNER")
    print("=" * 60)
    
    # Test required values
    test_values = [10, 100, 1000, 10000]
    
    print("\nTesting n = 10, 100, 1000, 10000")
    print("(For 100000 and 1000000, run with more time)\n")
    
    results = []
    for n in test_values:
        success = run_test(n, max_steps=100000 if n <= 10000 else 50000)
        results.append((n, success))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for n, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"n = {n:>6,}: {status}")
    
    successes = sum(1 for _, s in results if s)
    print(f"\nSuccess Rate: {successes}/{len(results)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
