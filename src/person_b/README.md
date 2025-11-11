# Person B - Board Representation & Validation Developer

## Role
Handles data structures and solution checking for the N-Queens problem.

## Core Responsibilities
- Implement board representation (array / list)
- Write `is_solution()` function to verify valid configuration
- Add utilities for random restarts and statistics
- Co-write Design Choices section

## Deliverables
- `board_utils.py` - Board representation and utility functions
- Solution validator code (`is_solution()` function)
- 1/2 of Design Choices section

## Board Representation
The board should be represented efficiently to handle large n values.
- Consider using a list/array where index represents column and value represents row
- Example: `[0, 2, 4, 1, 3]` for n=5 means queen in column 0 is in row 0, column 1 in row 2, etc.

## Functions to Implement
- `initialize_board(n)` - Create random initial board configuration
- `is_solution(board)` - Check if current board is a valid solution
- `count_conflicts(board, col, row)` - Count conflicts for a queen at (col, row)
- `get_conflicted_queens(board)` - Return list of columns with conflicts
- `get_min_conflicts_position(board, col)` - Find row with minimum conflicts for a column

## Usage
```python
from person_b.board_utils import initialize_board, is_solution, count_conflicts

# Initialize random board
board = initialize_board(n=8)

# Check if solution
if is_solution(board):
    print("Valid solution!")

# Count conflicts for a position
conflicts = count_conflicts(board, col=0, row=3)
```

## Integration
- Used by `person_a.min_conflicts` for board operations
- Used by `person_c` for testing and validation
- Used by `person_d` for visualization

