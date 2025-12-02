"""
Person A - MIN-CONFLICTS Algorithm Implementation

This package provides a complete implementation of the MIN-CONFLICTS
algorithm for solving the N-Queens problem.

Main exports:
    - min_conflicts: Main algorithm function
    - is_solution: Solution validator
    - greedy_board: Greedy board generator

Usage:
    from person_a import min_conflicts, is_solution
    
    board, steps = min_conflicts(100, random_seed=42)
    if board and is_solution(board):
        print(f"Valid solution found in {steps} steps!")
"""

from .min_conflicts import min_conflicts, is_solution, greedy_board

__all__ = ['min_conflicts', 'is_solution', 'greedy_board']
