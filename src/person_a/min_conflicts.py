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


def random_board(n: int, rng: random.Random) -> list[int]:
    """
    Generate a random initial board configuration.
    
    Places one queen in each row at a random column.
    
    Args:
        n: The size of the board (number of queens).
        rng: Random number generator instance for reproducibility.
    
    Returns:
        A list of n integers representing random queen positions.
    """
    return [rng.randint(0, n - 1) for _ in range(n)]


def min_conflicts(
    n: int,
    max_steps: int = 100000,
    random_seed: Optional[int] = None
) -> tuple[Optional[list[int]], int]:
    """
    Solve the N-Queens problem using the MIN-CONFLICTS algorithm.
    
    This algorithm starts with a random configuration and iteratively moves
    queens that are in conflict to positions with minimum conflicts, until
    a solution is found or the maximum number of steps is reached.
    
    Args:
        n: Board size (number of queens to place).
        max_steps: Maximum number of repair steps before giving up.
        random_seed: Optional seed for the random number generator.
    
    Returns:
        A tuple (board, steps_taken) where:
        - board: A valid N-Queens solution if found, otherwise None.
        - steps_taken: Number of steps/iterations used.
    
    Algorithm:
        1. Start with a random board (one queen per row).
        2. Maintain conflict counts for columns and diagonals.
        3. At each step:
           - If no conflicts exist, return the solution.
           - Otherwise, pick a conflicted row.
           - Try moving that queen to the column with minimum conflicts.
           - Update the board and conflict counts.
        4. Return None if max_steps is exceeded.
    
    Time complexity: O(max_steps) with O(1) conflict updates per step.
    """
    # Initialize random number generator
    rng = random.Random(random_seed)
    
    # Generate initial random board
    board = random_board(n, rng)
    
    # Initialize conflict tracking data structures
    # column_counts[c] = number of queens in column c
    column_counts = [0] * n
    
    # diag1_counts[d] = number of queens on major diagonal d (row - col)
    # Diagonal indices range from -(n-1) to (n-1), so we shift by (n-1)
    diag1_counts = [0] * (2 * n - 1)
    
    # diag2_counts[d] = number of queens on minor diagonal d (row + col)
    # Diagonal indices range from 0 to 2*(n-1)
    diag2_counts = [0] * (2 * n - 1)
    
    # Populate initial conflict counts
    for row in range(n):
        col = board[row]
        column_counts[col] += 1
        diag1_counts[row - col + (n - 1)] += 1
        diag2_counts[row + col] += 1
    
    # Helper function to count conflicts for a queen at (row, col)
    def count_conflicts(row: int, col: int) -> int:
        """
        Count how many other queens conflict with a queen at (row, col).
        
        A conflict occurs when another queen shares the same column,
        major diagonal, or minor diagonal.
        """
        conflicts = 0
        
        # Conflicts in the same column (subtract 1 to exclude self)
        conflicts += column_counts[col] - 1
        
        # Conflicts on the same major diagonal (subtract 1 to exclude self)
        conflicts += diag1_counts[row - col + (n - 1)] - 1
        
        # Conflicts on the same minor diagonal (subtract 1 to exclude self)
        conflicts += diag2_counts[row + col] - 1
        
        return conflicts
    
    # Helper function to get all rows currently in conflict
    def get_conflicted_rows() -> list[int]:
        """Return a list of all rows where the queen is in conflict."""
        conflicted = []
        for row in range(n):
            if count_conflicts(row, board[row]) > 0:
                conflicted.append(row)
        return conflicted
    
    # Main MIN-CONFLICTS loop
    for step in range(max_steps):
        # Check if current board is a solution
        conflicted_rows = get_conflicted_rows()
        
        if not conflicted_rows:
            # No conflicts - we have a solution!
            return (board, step)
        
        # Choose a random conflicted row
        row = rng.choice(conflicted_rows)
        old_col = board[row]
        
        # Find the column with minimum conflicts for this row
        min_conflicts_value = float('inf')
        best_cols = []
        
        for col in range(n):
            # Temporarily remove the queen from its current position
            if col == old_col:
                # If considering the current position, conflicts are already counted
                conflicts = count_conflicts(row, col)
            else:
                # Temporarily move the queen to compute conflicts
                # Remove from old position
                column_counts[old_col] -= 1
                diag1_counts[row - old_col + (n - 1)] -= 1
                diag2_counts[row + old_col] -= 1
                
                # Add to new position
                column_counts[col] += 1
                diag1_counts[row - col + (n - 1)] += 1
                diag2_counts[row + col] += 1
                
                # Count conflicts at new position
                conflicts = count_conflicts(row, col)
                
                # Restore old position
                column_counts[col] -= 1
                diag1_counts[row - col + (n - 1)] -= 1
                diag2_counts[row + col] -= 1
                
                column_counts[old_col] += 1
                diag1_counts[row - old_col + (n - 1)] += 1
                diag2_counts[row + old_col] += 1
            
            # Track columns with minimum conflicts
            if conflicts < min_conflicts_value:
                min_conflicts_value = conflicts
                best_cols = [col]
            elif conflicts == min_conflicts_value:
                best_cols.append(col)
        
        # Choose randomly among columns with minimum conflicts
        new_col = rng.choice(best_cols)
        
        # Move the queen to the new column
        if new_col != old_col:
            # Remove from old position
            column_counts[old_col] -= 1
            diag1_counts[row - old_col + (n - 1)] -= 1
            diag2_counts[row + old_col] -= 1
            
            # Add to new position
            column_counts[new_col] += 1
            diag1_counts[row - new_col + (n - 1)] += 1
            diag2_counts[row + new_col] += 1
            
            # Update board
            board[row] = new_col
    
    # Max steps exceeded without finding a solution
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
