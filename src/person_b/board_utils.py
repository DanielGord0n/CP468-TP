"""
Board Representation & Validation Utilities (N-Queens).

This module will be designed to cleanly integrate with Person A's current code structure.

Representation also matches Person A:
    board[row] = col    (Only one queen per row)

Therefore:
    "conflicting queens" are being returned as ROW indicies.
    "min-conflicts position" chooses a COLUMN index.


Author: Person B (Sam Oreskovic)
Course: CP468 - Artificial Intelligence
"""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Optional, List, Tuple

Board = List[int]

@dataclass
class ConflictTables:
    """
    Counts of the queens in each column and diagonal for O(1) conflict inputs.
    """
    n: int
    col_counts: List[int]   # n
    diag1_counts: List[int] # 2n - 1, idx = row - col + (n - 1)
    diag2_counts: List[int] # 2n - 1, idx = row + col

def initialize_board(n: int, rng: Optional[random.Random] = None) -> Board:
    """
    Make an initial board (randomized) with one queen per row.
    board[row] = random col
    """
    if rng is None:
        rng = random.Random()
    return [rng.randrange(n) for _ in range(n)]

def build_conflict_tables(board: Board) -> ConflictTables:
    """
    Build the counts for column and diagonal from a given board.
    """
    n = len(board)
    shift = (n - 1)
    col_counts = [0] * n
    diag1_counts = [0] * (2 * n - 1)
    diag2_counts = [0] * (2 * n - 1)

    for row, col in enumerate(board):
        col_counts[col] += 1
        diag1_counts[row - col + shift] += 1
        diag2_counts[row + col] += 1
    
    return ConflictTables(n = n, col_counts = col_counts, diag1_counts = diag1_counts, diag2_counts = diag2_counts)

def is_solution(board: Board) -> bool:
    """
    Check if the solution for N-Queens is valid in O(n).

    True if, and only if:
        - all columns are unique
        - all (row-col) diagonals are unique
        - all (row+col) diagonals are unique
    """
    n = len(board)
    cols = set()
    diag1 = set()
    diag2 = set()

    for row, col in enumerate(board):
        if col in cols:
            return False
        cols.add(col)

        d1 = row - col
        d2 = row + col
        if d1 in diag1 or d2 in diag2:
            return False
        diag1.add(d1)
        diag2.add(d2)
    
    return True

def conflicts_for_position(t: ConflictTables, row: int, col: int, current_col: Optional[int] = None) -> int:
    """
    Count the number of conflicts if the queen at (row, current_col) is moved to (row, col).
    
    current_col:
        - provides the queen's current column if the move being evaluated is an existing queen
        - used for no move evaluation, as it counts -=1 for itself
    """
    n = t.n
    shift = n - 1

    if current_col is not None and col == current_col:
        return (t.col_counts[col] - 1) + (t.diag1_counts[row - col + shift] - 1) + (t.diag2_counts[row + col] - 1)
    
    return t.col_counts[col] + t.diag1_counts[row - col + shift] + t.diag2_counts[row + col]

def queen_conflicts(t: ConflictTables, board: Board, row: int) -> int:
    """
    Counts the number of conflicts for the queen currently at (row, board[row]).
    """
    return conflicts_for_position(t, row, board[row], current_col = board[row])

def get_conflicted_queens(board: Board, t: ConflictTables) -> List[int]:
    """
    Returns as list of ROW indicies that currently have conflicting queens.
    """
    conflict = []
    for row in range(t.n):
        if queen_conflicts(t, board, row) > 0:
            conflict.append(row)
    return conflict

def apply_move(board: Board, t: ConflictTables, row: int, new_col: int) -> None:
    """
    Move the queen at (row, board[row]) to (row, new_col) and update conflict tables in O(1).
    """
    n = t.n
    shift = n - 1
    old_col = board[row]
    if new_col == old_col:
        return
    
    # remove old position
    t.col_counts[old_col] -= 1
    t.diag1_counts[row - old_col + shift] -= 1
    t.diag2_counts[row + old_col] -= 1

    # add new position
    t.col_counts[new_col] += 1
    t.diag1_counts[row - new_col + shift] += 1
    t.diag2_counts[row + new_col] += 1

    board[row] = new_col

def get_min_conflicts_position(board: Board, t: ConflictTables, row: int, rng: random.Random, sample_size: int = 50) -> int:
    """
    Find a column for the given row with the least conflicts.
    
    For small n: full search (exact min).
    For large n: random sampling (approx min needed for n=100000/1000000 to be efficient).
    
    Returns the chosen column index.
    """
    n = t.n
    current_col = board[row]

    # Full search for small n
    if n <= 5000:
        best = []
        best_val = 10 ** 18
        for col in range(n):
            cc = conflicts_for_position(t, row, col, current_col = current_col)
            if cc < best_val:
                best_val = cc
                best = [col]
            elif cc == best_val:
                best.append(col)
        return rng.choice(best)
    
    # Random sampling for large n
    # Make sure to keep track of/include current_col so "no move" is possible if 
    # the queen is already optimally placed.
    k = min(sample_size, n)
    possible_col = {current_col}
    while len(possible_col) < k:
        possible_col.add(rng.randrange(n))
    
    best = []
    best_val = 10 ** 18
    for col in possible_col:
        cc = conflicts_for_position(t, row, col, current_col = current_col)
        if cc < best_val:
            best_val = cc
            best = [col]
        elif cc == best_val:
            best.append(col)
    return rng.choice(best)

def solve_with_restarts(n: int, solver_fn, max_steps: int, attempts: int = 10, seed0: int = 42) -> Tuple[Optional[Board], int, int]:
    """
    Utility for random restarts + some basic stats.
    
    solver_fn signature should be:
        solver_fn(n, max_steps = <int>, random_seed = <int>) -> (board|None, steps)
    
    Returns: Best board or None, steps, and attempts
    """
    best_board = None
    best_steps = 10 ** 18
    best_attempt = -1

    for i in range(attempts):
        seed = seed0 + i
        board, steps = solver_fn(n, max_steps = max_steps, random_seed = seed)
        if board is not None:
            # keep fastest/most efficient solution
            if steps < best_steps:
                best_board, best_steps, best_attempt = board, steps, i + 1
    
    if best_board is None:
        return None, max_steps, -1
    return best_board, best_steps, best_attempt

