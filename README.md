# CP468 Term Project: N-Queens with MIN-CONFLICTS Algorithm

## Project Overview
Implementation and analysis of the MIN-CONFLICTS local-search algorithm for solving the N-Queens Constraint Satisfaction Problem (CSP).

**Optimization Update:**
The algorithm has been optimized to solve $N=1,000,000$ in approximately **20 seconds** (on standard hardware), achieving $O(n)$ time complexity.

## Quick Start

### 1. Run Interactive Solver
Solve for any N and optionally visualize the result (for $N \le 100$).
```bash
./run.sh
```
Or run with arguments:
```bash
./run.sh --n 1000
```

### 2. Run Benchmarks
Run the standard benchmark suite ($N=1,000$ to $1,000,000$).
```bash
./run.sh benchmark.py
```

## Project Structure
```
.
├── main.py             # Interactive solver script
├── benchmark.py        # Performance benchmark script
├── run.sh              # Helper script to run with dependencies
├── src/
│   ├── person_a/       # Algorithm Lead (Min-Conflicts logic)
│   ├── person_b/       # Board Validation
│   ├── person_c/       # Experiments (Legacy)
│   ├── person_d/       # Visualization
│   └── person_e/       # Integration
└── results/            # Output directory
```

## Dependencies
The project uses `numpy`, `matplotlib`, and `pandas` for visualization.
These are installed in a local virtual environment (`venv`) to avoid system conflicts.
**Always use `./run.sh`** to ensure these dependencies are loaded correctly.

## Performance Results

| N | Time (approx) | Steps | Status |
|---|---|---|---|
| 1,000 | ~0.02s | ~400 | Success |
| 10,000 | ~0.18s | ~3,000 | Success |
| 100,000 | ~1.8s | ~25,000 | Success |
| **1,000,000** | **~21s** | **~250,000** | **Success** |

## Team Roles

### Person A - Algorithm Lead
- Designs and implements the MIN-CONFLICTS algorithm
- Core algorithm file: `min_conflicts.py`

### Person B - Board Representation & Validation Developer
- Handles data structures and solution checking
- Core files: `board_utils.py`

### Person C - Testing & Performance Analyst
- Runs experiments and performance measurement

### Person D - Visualization & Poster Designer
- Builds graphical outputs and poster for demo
- Core file: `visualizer.py`

### Person E - Documentation & Integration Manager
- Integrates code and finalizes submission

