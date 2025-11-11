# Person A - Algorithm Lead

## Role
Designs and implements the MIN-CONFLICTS algorithm for the N-Queens problem.

## Core Responsibilities
- Implement initialization (random board)
- Write main loop (min-conflicts selection)
- Implement conflict-count function
- Optimize runtime for large n
- Comment code and document logic

## Deliverables
- `min_conflicts.py` - Core MIN-CONFLICTS algorithm implementation
- 1-page Algorithm Design write-up

## Algorithm Overview
The MIN-CONFLICTS algorithm:
1. Starts with a random assignment of queens (one per column)
2. Selects a conflicted variable (column with a queen in conflict)
3. Moves the queen to the position in that column with minimum conflicts
4. Repeats until a solution is found or max iterations reached

## Usage
```python
from person_a.min_conflicts import min_conflicts

# Solve n-queens problem
solution = min_conflicts(n=8, max_steps=1000)
```

## Integration
- Uses board representation from `person_b.board_utils`
- Uses solution validator from `person_b.board_utils.is_solution()`
- Should be optimized to handle large n values (up to 1,000,000)

## References
- AIMA 3rd ed., pages 220-221
- Algorithm covered in class lectures

