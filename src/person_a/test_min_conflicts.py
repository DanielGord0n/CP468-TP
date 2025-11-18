"""
Simple tests for the MIN-CONFLICTS implementation.

This file provides basic tests to verify the correctness and performance
of the MIN-CONFLICTS algorithm for N-Queens.

Run with: python3 src/person_a/test_min_conflicts.py
"""

import time
from min_conflicts import min_conflicts, is_solution, random_board
import random


def test_is_solution():
    """Test the is_solution function with known configurations."""
    print("Testing is_solution()...")
    
    # Valid 4-Queens solution
    valid_4 = [1, 3, 0, 2]
    assert is_solution(valid_4), "Failed: valid 4-Queens marked as invalid"
    
    # Invalid 4-Queens (two queens in same column)
    invalid_4_col = [0, 0, 2, 3]
    assert not is_solution(invalid_4_col), "Failed: invalid config marked as valid"
    
    # Invalid 4-Queens (two queens on same diagonal)
    invalid_4_diag = [0, 1, 2, 3]
    assert not is_solution(invalid_4_diag), "Failed: diagonal conflict not detected"
    
    # Valid 8-Queens solution
    valid_8 = [0, 4, 7, 5, 2, 6, 1, 3]
    assert is_solution(valid_8), "Failed: valid 8-Queens marked as invalid"
    
    print("  ✓ All is_solution() tests passed\n")


def test_random_board():
    """Test random board generation."""
    print("Testing random_board()...")
    
    rng = random.Random(42)
    n = 20
    board = random_board(n, rng)
    
    assert len(board) == n, "Board length incorrect"
    assert all(0 <= col < n for col in board), "Board contains invalid column values"
    
    print(f"  ✓ Generated valid {n}-Queens random board\n")


def test_small_n():
    """Test MIN-CONFLICTS on small board sizes."""
    print("Testing MIN-CONFLICTS on small boards...")
    
    test_cases = [4, 8, 10]
    
    for n in test_cases:
        board, steps = min_conflicts(n, max_steps=10000, random_seed=42)
        
        if board is not None:
            assert len(board) == n, f"Board size incorrect for n={n}"
            assert is_solution(board), f"Invalid solution returned for n={n}"
            print(f"  ✓ {n}-Queens: solution found in {steps} steps")
        else:
            print(f"  ⚠ {n}-Queens: no solution in {steps} steps (rare but OK)")
    
    print()


def test_large_n():
    """Test MIN-CONFLICTS on larger board sizes."""
    print("Testing MIN-CONFLICTS on large boards...")
    
    test_cases = [100, 500, 1000]
    
    for n in test_cases:
        start_time = time.time()
        board, steps = min_conflicts(n, max_steps=50000, random_seed=42)
        elapsed = time.time() - start_time
        
        if board is not None:
            assert len(board) == n, f"Board size incorrect for n={n}"
            assert is_solution(board), f"Invalid solution returned for n={n}"
            print(f"  ✓ {n}-Queens: solution found in {steps} steps ({elapsed:.3f}s)")
        else:
            print(f"  ⚠ {n}-Queens: no solution in {steps} steps ({elapsed:.3f}s)")
    
    print()


def test_reproducibility():
    """Test that the same seed produces the same results."""
    print("Testing reproducibility with random_seed...")
    
    n = 50
    seed = 123
    
    board1, steps1 = min_conflicts(n, max_steps=10000, random_seed=seed)
    board2, steps2 = min_conflicts(n, max_steps=10000, random_seed=seed)
    
    assert board1 == board2, "Same seed produced different boards"
    assert steps1 == steps2, "Same seed produced different step counts"
    
    print(f"  ✓ Reproducibility confirmed (n={n}, seed={seed})\n")


def test_performance():
    """Benchmark performance on various board sizes."""
    print("Performance Benchmark")
    print("-" * 60)
    
    test_sizes = [10, 50, 100, 500, 1000, 5000]
    
    for n in test_sizes:
        trials = 3 if n <= 1000 else 1
        total_time = 0
        total_steps = 0
        successes = 0
        
        for trial in range(trials):
            start_time = time.time()
            board, steps = min_conflicts(n, max_steps=50000, random_seed=42 + trial)
            elapsed = time.time() - start_time
            
            if board is not None:
                total_time += elapsed
                total_steps += steps
                successes += 1
        
        if successes > 0:
            avg_time = total_time / successes
            avg_steps = total_steps / successes
            print(f"  n={n:5d}: {avg_steps:6.0f} steps, {avg_time:.3f}s avg ({successes}/{trials} success)")
        else:
            print(f"  n={n:5d}: No solutions found in any trial")
    
    print()


def main():
    """Run all tests."""
    print("=" * 60)
    print("MIN-CONFLICTS Algorithm Test Suite")
    print("=" * 60)
    print()
    
    test_is_solution()
    test_random_board()
    test_small_n()
    test_large_n()
    test_reproducibility()
    test_performance()
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
