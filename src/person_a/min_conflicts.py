"""
MIN-CONFLICTS implementation for N-Queens (CP468 term project).

This module implements the MIN-CONFLICTS local search algorithm for solving
the N-Queens problem. The algorithm can efficiently handle large board sizes
(up to 1,000,000 queens) by maintaining conflict counts in auxiliary data
structures and updating them incrementally.

Board representation:
    A board is represented as a list of integers of length n, where:
    - Index i = row i
    - Value board[i] = column of the queen in row i
    
    Example: board = [1, 3, 0, 2] for n=4 means:
        Row 0 has a queen in column 1
        Row 1 has a queen in column 3
        Row 2 has a queen in column 0
        Row 3 has a queen in column 2

Author: Person A
Course: CP468 - Artificial Intelligence
"""

import random
from typing import Optional


def is_solution(board: list[int]) -> bool:
    """
    Check if a given board configuration is a valid N-Queens solution.
    
    A valid solution has no two queens attacking each other:
    - No two queens in the same column
    - No two queens on the same major diagonal (row - col constant)
    - No two queens on the same minor diagonal (row + col constant)
    
    Args:
        board: List of integers where board[row] = column of queen in that row.
    
    Returns:
        True if the board is a valid N-Queens solution, False otherwise.
    
    Time complexity: O(n) where n = len(board)
    """
    n = len(board)
    
    # Check for duplicate columns
    columns = set()
    for col in board:
        if col in columns:
            return False
        columns.add(col)
    
    # Check for duplicate major diagonals (row - col)
    major_diagonals = set()
    for row in range(n):
        diag = row - board[row]
        if diag in major_diagonals:
            return False
        major_diagonals.add(diag)
    
    # Check for duplicate minor diagonals (row + col)
    minor_diagonals = set()
    for row in range(n):
        diag = row + board[row]
        if diag in minor_diagonals:
            return False
        minor_diagonals.add(diag)
    
    return True


def greedy_board(n: int, rng: random.Random) -> tuple[list[int], list[int], list[int], list[int]]:
    """
    Generate an initial board using a greedy heuristic.
    
    Places queens row by row, choosing the column with minimum conflicts
    at the time of placement. This provides a much better starting state
    than random assignment.
    
    Returns:
        Tuple of (board, column_counts, diag1_counts, diag2_counts)
    """
    board = [-1] * n
    column_counts = [0] * n
    diag1_counts = [0] * (2 * n - 1)
    diag2_counts = [0] * (2 * n - 1)
    
    # Candidate columns for random tie-breaking
    # We'll reuse this list to avoid allocation
    candidates = []
    
    for row in range(n):
        min_conflicts = float('inf')
        candidates.clear()
        
        # Sample a subset of columns to check for placement
        # For the first row, all cols are 0 conflicts, so just pick random
        if row == 0:
            col = rng.randint(0, n - 1)
            candidates.append(col)
        else:
            # Check a constant number of random columns plus some specific ones
            # to keep initialization O(n) overall (O(1) per row)
            # We check 50 random columns
            n_samples = 50
            for _ in range(n_samples):
                col = rng.randint(0, n - 1)
                
                conflicts = (column_counts[col] + 
                             diag1_counts[row - col + (n - 1)] + 
                             diag2_counts[row + col])
                
                if conflicts < min_conflicts:
                    min_conflicts = conflicts
                    candidates.clear()
                    candidates.append(col)
                elif conflicts == min_conflicts:
                    candidates.append(col)
        
        # Pick one of the best candidates
        col = rng.choice(candidates)
        
        board[row] = col
        column_counts[col] += 1
        diag1_counts[row - col + (n - 1)] += 1
        diag2_counts[row + col] += 1
        
    return board, column_counts, diag1_counts, diag2_counts


def min_conflicts(
    n: int,
    max_steps: int = 100000,
    random_seed: Optional[int] = None
) -> tuple[Optional[list[int]], int]:
    """
    Solve the N-Queens problem using the MIN-CONFLICTS algorithm.
    
    Optimized for O(n) performance on large inputs using:
    1. Greedy initialization
    2. Constant-time repair steps (fixed sample size)
    3. Efficient conflict tracking with inverse indices
    """
    # Initialize random number generator
    rng = random.Random(random_seed)
    
    # 1. Greedy Initialization (O(n))
    board, column_counts, diag1_counts, diag2_counts = greedy_board(n, rng)
    
    # Inverse indices to track which queens are where
    queens_in_col = [[] for _ in range(n)]
    queens_in_diag1 = [[] for _ in range(2 * n - 1)]
    queens_in_diag2 = [[] for _ in range(2 * n - 1)]
    
    # Track empty columns for efficient sampling
    # These are prime targets for moving queens
    empty_columns = set(range(n))
    
    # Populate inverse indices and empty_columns (O(n))
    for r in range(n):
        c = board[r]
        queens_in_col[c].append(r)
        queens_in_diag1[r - c + (n - 1)].append(r)
        queens_in_diag2[r + c].append(r)
        if c in empty_columns:
            empty_columns.remove(c)
    
    # Convert empty_columns to list for random sampling
    empty_columns_list = list(empty_columns)
    
    # Helper to add/remove from empty_columns_list efficiently
    # We use a map to track indices in the list
    empty_col_indices = {col: i for i, col in enumerate(empty_columns_list)}
    
    def add_empty_col(c):
        if c not in empty_col_indices:
            empty_col_indices[c] = len(empty_columns_list)
            empty_columns_list.append(c)
            
    def remove_empty_col(c):
        if c in empty_col_indices:
            idx = empty_col_indices[c]
            last = empty_columns_list[-1]
            
            # Swap with last
            empty_columns_list[idx] = last
            empty_col_indices[last] = idx
            
            empty_columns_list.pop()
            del empty_col_indices[c]

    # Helper to count conflicts for a queen at (row, col)
    def count_conflicts(row: int, col: int) -> int:
        return (column_counts[col] + 
                diag1_counts[row - col + (n - 1)] + 
                diag2_counts[row + col] - 3)

    # 2. Initialize conflicted rows set (O(n))
    conflicted_rows_set = set()
    conflicted_rows_list = []
    
    def add_conflict(r):
        if r not in conflicted_rows_set:
            conflicted_rows_set.add(r)
            conflicted_rows_list.append(r)
            
    def remove_conflict_idx(idx):
        r = conflicted_rows_list[idx]
        conflicted_rows_set.remove(r)
        last = conflicted_rows_list[-1]
        conflicted_rows_list[idx] = last
        conflicted_rows_list.pop()
        return last

    for r in range(n):
        if count_conflicts(r, board[r]) > 0:
            add_conflict(r)
            
    if not conflicted_rows_list:
        return (board, 0)
        
    # 3. Repair Loop (O(max_steps))
    for step in range(max_steps):
        if not conflicted_rows_list:
            return (board, step)
            
        # Pick a random conflicted row
        rand_idx = rng.randint(0, len(conflicted_rows_list) - 1)
        row = conflicted_rows_list[rand_idx]
        
        # Verify it's still conflicted
        if count_conflicts(row, board[row]) == 0:
            remove_conflict_idx(rand_idx)
            continue
            
        old_col = board[row]
        
        # Find best column to move to
        min_conflicts_val = float('inf')
        best_cols = []
        
        # Sample strategy:
        # 1. Always check current column (baseline)
        # 2. Check some empty columns (high priority)
        # 3. Check some random columns (exploration)
        
        candidates = set()
        candidates.add(old_col)
        
        # Sample from empty columns (up to 20)
        if empty_columns_list:
            k = min(20, len(empty_columns_list))
            # random.sample is O(k)
            for c in rng.sample(empty_columns_list, k):
                candidates.add(c)
                
        # Sample from random columns (up to 10)
        for _ in range(10):
            candidates.add(rng.randint(0, n - 1))
            
        for col in candidates:
            c_count = column_counts[col]
            d1_count = diag1_counts[row - col + (n - 1)]
            d2_count = diag2_counts[row + col]
            
            if col == old_col:
                conflicts = (c_count + d1_count + d2_count) - 3
            else:
                conflicts = (c_count + d1_count + d2_count)
            
            if conflicts < min_conflicts_val:
                min_conflicts_val = conflicts
                best_cols = [col]
            elif conflicts == min_conflicts_val:
                best_cols.append(col)
        
        new_col = rng.choice(best_cols)
        
        if new_col != old_col:
            # Move the queen
            
            # 1. Add new conflicts
            for other_r in queens_in_col[new_col]:
                add_conflict(other_r)
            for other_r in queens_in_diag1[row - new_col + (n - 1)]:
                add_conflict(other_r)
            for other_r in queens_in_diag2[row + new_col]:
                add_conflict(other_r)
            
            # 2. Update counts
            column_counts[old_col] -= 1
            diag1_counts[row - old_col + (n - 1)] -= 1
            diag2_counts[row + old_col] -= 1
            
            column_counts[new_col] += 1
            diag1_counts[row - new_col + (n - 1)] += 1
            diag2_counts[row + new_col] += 1
            
            # 3. Update inverse indices
            try:
                queens_in_col[old_col].remove(row)
                queens_in_diag1[row - old_col + (n - 1)].remove(row)
                queens_in_diag2[row + old_col].remove(row)
            except ValueError:
                pass
                
            queens_in_col[new_col].append(row)
            queens_in_diag1[row - new_col + (n - 1)].append(row)
            queens_in_diag2[row + new_col].append(row)
            
            # 4. Update empty columns
            if column_counts[old_col] == 0:
                add_empty_col(old_col)
            if column_counts[new_col] == 1: # Was 0, now 1
                remove_empty_col(new_col)
            
            board[row] = new_col
            
    if is_solution(board):
        return (board, max_steps)
            
    return (None, max_steps)

def main():
    """
    Demonstration of the MIN-CONFLICTS algorithm.
    
    Solves N-Queens for various board sizes and prints results.
    """
    print("MIN-CONFLICTS Algorithm for N-Queens")
    print("=" * 50)
    
    # Test with different board sizes
    test_sizes = [4, 8, 10, 20, 50, 100]
    
    for n in test_sizes:
        print(f"\nSolving {n}-Queens...")
        board, steps = min_conflicts(n, max_steps=100000, random_seed=42)
        
        if board is not None:
            print(f"  ✓ Solution found in {steps} steps")
            print(f"  ✓ Verification: {is_solution(board)}")
            
            # Print board for small n
            if n <= 10:
                print(f"  Board: {board}")
        else:
            print(f"  ✗ No solution found within {steps} steps")
    
    # Demonstrate with a specific example
    print("\n" + "=" * 50)
    print("Example: 8-Queens with detailed output")
    print("=" * 50)
    
    board, steps = min_conflicts(8, max_steps=10000, random_seed=123)
    
    if board is not None:
        print(f"Solution found in {steps} steps")
        print(f"Board configuration: {board}")
        print("\nVisualization:")
        
        for row in range(8):
            line = ""
            for col in range(8):
                if board[row] == col:
                    line += "Q "
                else:
                    line += ". "
            print(line)
        
        print(f"\nIs valid solution? {is_solution(board)}")
    else:
        print(f"No solution found within {steps} steps")


if __name__ == "__main__":
    main()
