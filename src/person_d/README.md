# Person D - Visualization & Poster Designer

## Role
Builds graphical outputs and the poster for demo.

## Core Responsibilities
- Write visualizer for small n (ASCII or Matplotlib board)
- Generate conflict heatmaps or runtime graphs from Person C's data
- Design demo/poster showing algorithm behavior
- Write Visualization & Interpretation paragraph

## Deliverables
- `visualizer.py` - Visualization code
- Poster with graphical representations
- Figures and graphs
- Short Visualization & Interpretation report section

## Visualization Requirements
- Visualize board for small n (n ≤ 100) using Matplotlib
- Generate performance graphs (runtime vs n, iterations vs n)
- Create conflict heatmaps showing algorithm progress
- Design poster showing algorithm behavior for large n
- ASCII visualization option for quick debugging

## Functions to Implement
- `visualize_board(board, n)` - Display n-queens board
- `plot_performance(data)` - Plot performance metrics
- `plot_conflicts_over_time(conflict_history)` - Show conflict reduction
- `create_poster(solution, n)` - Generate poster for large n solution

## Usage
```python
from src.person_d.visualizer import visualize_board, plot_performance
from src.person_a.min_conflicts import min_conflicts

# Solve and visualize
solution, steps = min_conflicts(n=8, max_steps=1000)
if solution:
    visualize_board(solution, n=8)

# Plot performance data from CSV
import pandas as pd
data = pd.read_csv('results/n100_results.csv')
plot_performance(data)
```

## Output Locations
- Save figures in `results/` directory
- Poster should be saved as high-resolution image/PDF
- Include visualizations in final report

## Integration
- Uses solution data from `person_a.min_conflicts`
- Uses performance data from `person_c` experiments
- Visualizations included in final report by `person_e`
- Poster used for demo/presentation

## Poster Requirements
- Show solution for large n (e.g., n = 1000 or larger)
- Demonstrate algorithm behavior
- Include performance metrics
- Professional, clear, and visually appealing

