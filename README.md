# CP468 Term Project: N-Queens with MIN-CONFLICTS Algorithm

## Project Overview
Implementation and analysis of the MIN-CONFLICTS local-search algorithm for solving the N-Queens Constraint Satisfaction Problem (CSP).

## Project Goal
- Implement the MIN-CONFLICTS algorithm for the N-Queens problem
- Test performance for n = 10, 100, 1000, 10000, 100000, 1000000
- Document results, analysis, and visual output
- Generate poster with graphical representations for large n

## Project Structure
```
src/
├── person_a/           # Algorithm Lead - MIN-CONFLICTS implementation
├── person_b/           # Board Representation & Validation Developer
├── person_c/           # Testing & Performance Analyst
├── person_d/           # Visualization & Poster Designer
└── person_e/           # Documentation & Integration Manager
results/                # Experimental results (CSV files, plots, tables)
docs/                   # Documentation files
```

## Team Roles

### Person A - Algorithm Lead
- Designs and implements the MIN-CONFLICTS algorithm
- Core algorithm file: `min_conflicts.py`
- Deliverables: Algorithm implementation + 1-page Algorithm Design write-up

### Person B - Board Representation & Validation Developer
- Handles data structures and solution checking
- Core files: `board_utils.py`, solution validator
- Deliverables: Board representation code + solution validator + 1/2 of Design Choices section

### Person C - Testing & Performance Analyst
- Runs experiments and performance measurement
- Deliverables: CSV logs + plots + tables + 2 pages Results & Discussion

### Person D - Visualization & Poster Designer
- Builds graphical outputs and poster for demo
- Core file: `visualizer.py`
- Deliverables: Visualizer code + poster + figures + Visualization & Interpretation section

### Person E - Documentation & Integration Manager
- Integrates code and finalizes submission
- Deliverables: README.md + final PDF report + complete code bundle

## Dependencies
See `requirements.txt` for Python package requirements.

## Testing
Implementations should be tested with increasingly larger values of `n`. Solutions must be found for:
- n = 10
- n = 100
- n = 1000
- n = 10000
- n = 100000
- n = 1000000

## Submission Requirements
- One `.zip` file (code)
- One `.pdf` file (design document) containing:
  1. Cover sheet (Names/Student IDs, Course Number/Name, Date)
  2. Discussion of design choices (e.g., data structures)
  3. Clear instructions for installation, compilation, and execution
  4. Results of test runs for specified n-values
  5. Poster with graphical representations of solution for large n

## Resources
- MIN-CONFLICTS algorithm described in AIMA 3rd ed., pages 220-221
- Algorithm covered in class lectures

