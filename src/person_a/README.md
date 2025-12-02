# Person A: MIN-CONFLICTS Algorithm for N-Queens

## Overview
Implementation of the MIN-CONFLICTS local search algorithm for the N-Queens problem (CP468 Term Project). Based on AIMA 3rd edition, pages 220-221.

## Files
- `min_conflicts.py` - Core algorithm implementation
- `run_tests.py` - Test runner for required n values
- `__init__.py` - Package setup

## How to Run

### Run Tests
```bash
cd src/person_a
python3 run_tests.py
```
Tests n = 10, 100, 1000, 10000

### Demo
```bash
python3 src/person_a/min_conflicts.py
```

## Board Representation
- List of integers: `board[row] = column`
- Example: `[1, 3, 0, 2]` for n=4 means queens at (0,1), (1,3), (2,0), (3,2)

## API Functions

### `min_conflicts(n, max_steps=100000, random_seed=None)`
Solves N-Queens and returns `(board, steps)`.
- Uses **Greedy Initialization** for better starting state.
- Uses **Constant-Time Repair** for O(n) performance.

### `greedy_board(n, rng)`
Generates a greedy initial configuration (minimizes conflicts row by row).

## Usage Example

```python
from src.person_a.min_conflicts import min_conflicts

board, steps = min_conflicts(n=100, random_seed=42)
if board:
    print(f"Solution found in {steps} steps!")
```

## Author
Person A - CP468 Term Project
Reference: AIMA 3rd ed., pp. 220-221

