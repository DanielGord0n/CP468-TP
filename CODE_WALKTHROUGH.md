# Codebase Walkthrough & Explanation

This document breaks down exactly how the code works, file by file. Use this to explain the project during interviews.

## 1. The Core Algorithm (`src/person_a/min_conflicts.py`)
This is the most important file. It contains the logic that solves the problem.

### Key Function: `min_conflicts(n, max_steps)`
This is the main loop.
1.  **Initialization**: It calls `greedy_board(n)` instead of placing queens randomly.
    *   *Why?* Random placement creates ~500,000 conflicts for N=1M. Greedy placement creates only ~50. This makes the solver 1000x faster.
2.  **Conflict Tracking**: It sets up "Inverse Indices" (maps/sets) to track where every queen is.
    *   `queens_in_col`: Which row is the queen in for column X?
    *   `queens_in_diag1`: Which queens are on diagonal / ?
    *   `queens_in_diag2`: Which queens are on diagonal \ ?
    *   *Why?* This allows us to calculate conflicts in $O(1)$ (instant) time instead of counting them one by one.
3.  **The Loop**:
    *   It picks a random queen that is currently attacking someone (`conflicted_rows`).
    *   It tries to move it to a better spot.
    *   **Optimization**: It prioritizes checking "Empty Columns" (columns that no one is attacking). Moving a queen there usually fixes the problem immediately.

## 2. The Validator (`src/person_b/board_utils.py`)
This file checks if the answer is actually correct.

### Key Function: `is_solution(board)`
*   It iterates through the board and checks if any two queens share a row or diagonal.
*   If it finds even *one* pair of attacking queens, it returns `False`.
*   We use this at the end to prove our solution is valid.

## 3. The Visualizer (`src/person_d/visualizer.py`)
This file draws the board.

### Key Logic
*   **Small Boards (N < 100)**: It uses `matplotlib` to draw a chessboard with 'X' markers for queens.
*   **Large Boards**: It skips drawing because an image with 1 million pixels is too big.
*   **Dependency Handling**: It has `try/except` blocks so the code doesn't crash if you don't have `matplotlib` installed.

## 4. The Runner (`main.py`)
This is the "User Interface".
*   It handles the command line arguments (like `--n 1000`).
*   It runs the solver, times it, checks the solution, and prints the result nicely.

## 5. The Benchmark (`benchmark.py`)
This is the "Performance Tester".
*   It runs the solver for $N = 1,000, 10,000, 100,000, 1,000,000$.
*   It prints a table showing the time and steps for each.
