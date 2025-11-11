# Person C - Testing & Performance Analyst

## Role
Focuses on experiment runs and performance measurement.

## Core Responsibilities
- Run algorithm for all required n-values (10, 100, 1000, 10000, 100000, 1000000)
- Measure execution time and iteration count
- Collect success/failure rates over multiple runs
- Create result tables and performance plots
- Draft Results & Discussion section

## Deliverables
- CSV logs with experimental data
- Performance plots and graphs
- Result tables
- 2 pages Results & Discussion section

## Testing Requirements
Test the algorithm for the following n-values:
- n = 10
- n = 100
- n = 1000
- n = 10000
- n = 100000
- n = 1000000

## Metrics to Collect
- Execution time
- Number of iterations until solution
- Success rate over multiple runs
- Average conflicts per iteration
- Maximum n for which solution works in reasonable time

## Output Format
Save results as CSV files in the `results/` directory:
- `n10_results.csv`
- `n100_results.csv`
- `n1000_results.csv`
- `n10000_results.csv`
- `n100000_results.csv`
- `n1000000_results.csv`

Each CSV should include columns:
- run_id, n, iterations, execution_time, success, initial_conflicts, final_conflicts

## Usage
```python
from person_a.min_conflicts import min_conflicts
from person_b.board_utils import is_solution
import time

# Run experiment for n=100
start_time = time.time()
solution = min_conflicts(n=100, max_steps=10000)
execution_time = time.time() - start_time

# Verify solution
if is_solution(solution):
    print(f"Solution found in {execution_time:.2f} seconds")
```

## Integration
- Uses algorithm from `person_a.min_conflicts`
- Uses validation from `person_b.board_utils`
- Provides data for `person_d` visualizations
- Results used in final report by `person_e`

