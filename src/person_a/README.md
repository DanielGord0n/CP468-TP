# Person A: MIN-CONFLICTS Algorithm for N-Queens

## Overview
This module implements the MIN-CONFLICTS local search algorithm for solving the N-Queens problem as part of the CP468 (Artificial Intelligence) term project.

## File
- `min_conflicts.py` - Complete implementation of the MIN-CONFLICTS algorithm

## Algorithm
MIN-CONFLICTS is a local search algorithm that:
1. Starts with a random configuration (one queen per row)
2. Iteratively repairs conflicts by moving queens to positions with minimum conflicts
3. Terminates when a solution is found or max steps is reached

The algorithm is particularly efficient for large N-Queens instances (can handle up to 1,000,000 queens) due to:
- O(1) conflict updates using auxiliary data structures
- Efficient tracking of column and diagonal occupancy
- Random tie-breaking for avoiding local minima

## Board Representation
A board is represented as a list of integers:
- Index i = row i
- Value board[i] = column of queen in row i

Example: `[1, 3, 0, 2]` for n=4 means queens at (0,1), (1,3), (2,0), (3,2)

## Public API

### `is_solution(board: list[int]) -> bool`
Checks if a board configuration is a valid N-Queens solution.

**Parameters:**
- `board`: List of integers representing queen positions

**Returns:**
- `True` if valid solution (no queens attack each other), `False` otherwise

**Time Complexity:** O(n)

### `min_conflicts(n: int, max_steps: int = 100000, random_seed: int | None = None) -> tuple[list[int] | None, int]`
Solves the N-Queens problem using MIN-CONFLICTS.

**Parameters:**
- `n`: Board size (number of queens)
- `max_steps`: Maximum iterations before giving up (default: 100,000)
- `random_seed`: Optional seed for reproducible results

**Returns:**
- Tuple `(board, steps_taken)` where:
  - `board`: Valid solution if found, otherwise `None`
  - `steps_taken`: Number of iterations used

**Time Complexity:** O(max_steps) with O(1) per step

### `random_board(n: int, rng: random.Random) -> list[int]`
Helper function to generate a random initial board.

**Parameters:**
- `n`: Board size
- `rng`: Random number generator instance

**Returns:**
- List of n integers with random queen positions

## Usage Example

```python
from src.person_a.min_conflicts import min_conflicts, is_solution

# Solve 100-Queens
board, steps = min_conflicts(100, max_steps=100000, random_seed=42)

if board is not None:
    print(f"Solution found in {steps} steps")
    print(f"Valid: {is_solution(board)}")
    print(f"Board: {board}")
else:
    print(f"No solution found within {steps} steps")
```

## Testing
Run the module directly to see demonstrations:
```bash
python3 src/person_a/min_conflicts.py
```

This will:
- Solve N-Queens for various board sizes (4, 8, 10, 20, 50, 100)
- Display number of steps taken
- Show board visualization for small n
- Verify solutions using `is_solution()`

## Performance Notes
- Typically finds solutions very quickly (often < 100 steps even for large n)
- Occasionally gets stuck in local minima (rare with good random initialization)
- Scales well to very large problems (tested up to n=1,000,000 in literature)
- Not guaranteed to find a solution within max_steps, but empirically very reliable

## Implementation Details
The algorithm uses three auxiliary data structures for efficient conflict counting:
- `column_counts[c]`: Number of queens in column c
- `diag1_counts[d]`: Number of queens on major diagonal (row - col = d)
- `diag2_counts[d]`: Number of queens on minor diagonal (row + col = d)

These allow O(1) conflict computation and updates when moving a queen.

## Integration with Other Modules
This implementation is self-contained and provides its own:
- Board representation and generation
- Solution validation (`is_solution()`)
- Complete MIN-CONFLICTS solver

Other team members can import and use these functions directly without dependencies.

## References
- Russell & Norvig, AIMA 3rd ed., pages 220-221
- Algorithm covered in CP468 class lectures

## Author
Person A - CP468 Term Project

