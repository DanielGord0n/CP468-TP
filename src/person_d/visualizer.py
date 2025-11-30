"""
Person D - Visualization & Poster Designer
CP468 N-Queens with MIN-CONFLICTS

Functions exposed to the rest of the group:

    visualize_board(board, n)
    plot_performance(data)
    plot_conflicts_over_time(conflict_history)
    create_poster(solution, n)

Assumptions
-----------
- `board` is a length-n iterable where index = column, value = row
  (i.e., board[col] = row of queen in that column).
  If your group used a different representation, only update
  `_board_to_array`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------
# General config
# ---------------------------------------------------------------------

# All figures will be saved here (matches spec: "results/ directory")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def _board_to_array(board: Sequence[int], n: Optional[int] = None) -> np.ndarray:
    """
    Convert 1D board representation to an n x n numpy array with
    1 where a queen is placed, 0 otherwise.

    Assumes board[col] = row.
    """
    if n is None:
        n = len(board)

    arr = np.zeros((n, n), dtype=int)

    for col, row in enumerate(board):
        if 0 <= row < n:
            arr[row, col] = 1
    return arr


def ascii_board(board: Sequence[int], n: Optional[int] = None) -> str:
    """
    Return an ASCII representation of the board for quick debugging.

    Example (n=4):

    . Q . .
    . . . Q
    Q . . .
    . . Q .
    """
    if n is None:
        n = len(board)

    arr = _board_to_array(board, n)
    lines: list[str] = []
    for r in range(n):
        line = []
        for c in range(n):
            line.append("Q" if arr[r, c] == 1 else ".")
        lines.append(" ".join(line))
    return "\n".join(lines)


def board_row_to_col(board_by_row: list[int]) -> list[int]:
    """
    Convert Person A's board format (index = row, value = col)
    into the visualizer's format (index = col, value = row).
    """
    n = len(board_by_row)
    board_by_col = [0] * n
    for row, col in enumerate(board_by_row):
        board_by_col[col] = row
    return board_by_col


# ---------------------------------------------------------------------
# 1. visualize_board
# ---------------------------------------------------------------------

def visualize_board(
    board: Sequence[int],
    n: Optional[int] = None,
    title: Optional[str] = None,
    save: bool = True,
    show: bool = True,
    filename: Optional[str] = None,
) -> Path:
    """
    Display an n-queens board using Matplotlib (for small n, n <= 100).

    Parameters
    ----------
    board : sequence of int
        Board representation where board[col] = row.
    n : int, optional
        Board size. If None, len(board) is used.
    title : str, optional
        Figure title.
    save : bool
        Whether to save the figure into results/ directory.
    show : bool
        Whether to display the figure in a window.
    filename : str, optional
        Custom file name. If None, uses f"board_n{n}.png".
    """
    if n is None:
        n = len(board)

    arr = _board_to_array(board, n)

    fig, ax = plt.subplots(figsize=(6, 6))

    # Draw checkered board background
    bg = np.indices((n, n)).sum(axis=0) % 2
    ax.imshow(bg, cmap="gray", interpolation="nearest")

    # Overlay queens
    queen_rows, queen_cols = np.where(arr == 1)
    ax.scatter(
        queen_cols,
        queen_rows,
        s=200 if n <= 20 else 20,
        marker="X",
    )

    # Grid lines
    ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which="minor", linewidth=0.5)

    # Axis formatting
    step = max(1, n // 10)
    ax.set_xticks(np.arange(0, n, step))
    ax.set_yticks(np.arange(0, n, step))
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(n - 0.5, -0.5)  # flip y-axis so (0,0) is top-left

    if title is None:
        title = f"{n}-Queens Solution"
    ax.set_title(title)

    ax.set_xlabel("Column")
    ax.set_ylabel("Row")

    fig.tight_layout()

    if filename is None:
        filename = f"board_n{n}.png"
    out_path = RESULTS_DIR / filename

    if save:
        fig.savefig(out_path, dpi=300)

    if show:
        plt.show()
    else:
        plt.close(fig)

    return out_path


# ---------------------------------------------------------------------
# 2. plot_performance
# ---------------------------------------------------------------------

def plot_performance(
    data: pd.DataFrame,
    save: bool = True,
    show: bool = True,
    filename: str = "performance.png",
) -> Path:
    """
    Plot performance metrics (runtime vs n, iterations vs n).

    Expected columns in `data` (from Person C):
        - 'n' (problem size)
        - 'runtime' (seconds)
        - 'iterations' (min-conflicts steps)
    """
    required_cols = ["n", "runtime", "iterations"]
    for col in required_cols:
        if col not in data.columns:
            raise ValueError(
                f"plot_performance: expected column '{col}' in DataFrame."
            )

    data = data.sort_values("n")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Runtime vs n
    axes[0].plot(data["n"], data["runtime"], marker="o")
    axes[0].set_xscale("log")
    axes[0].set_xlabel("n (log scale)")
    axes[0].set_ylabel("Runtime (seconds)")
    axes[0].set_title("Runtime vs n")

    # Iterations vs n
    axes[1].plot(data["n"], data["iterations"], marker="o")
    axes[1].set_xscale("log")
    axes[1].set_xlabel("n (log scale)")
    axes[1].set_ylabel("Iterations")
    axes[1].set_title("Iterations vs n")

    fig.suptitle("MIN-CONFLICTS Performance on n-Queens")
    fig.tight_layout()

    out_path = RESULTS_DIR / filename
    if save:
        fig.savefig(out_path, dpi=300)

    if show:
        plt.show()
    else:
        plt.close(fig)

    return out_path


# ---------------------------------------------------------------------
# 3. plot_conflicts_over_time
# ---------------------------------------------------------------------

def plot_conflicts_over_time(
    conflict_history: Iterable[int],
    save: bool = True,
    show: bool = True,
    filename: str = "conflicts_over_time.png",
) -> Path:
    """
    Plot how the number of conflicts decreases over time (per step).

    Parameters
    ----------
    conflict_history : iterable of int
        conflict_history[t] = number of conflicts after step t.
        (Person A can log this inside min_conflicts.)
    """
    conflicts = list(conflict_history)
    steps = list(range(len(conflicts)))

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(steps, conflicts, marker=".")
    ax.set_xlabel("Step")
    ax.set_ylabel("# Conflicts")
    ax.set_title("Conflict Reduction Over Time")
    ax.grid(True, linestyle="--", alpha=0.5)

    fig.tight_layout()

    out_path = RESULTS_DIR / filename
    if save:
        fig.savefig(out_path, dpi=300)

    if show:
        plt.show()
    else:
        plt.close(fig)

    return out_path


# ---------------------------------------------------------------------
# 4. create_poster
# ---------------------------------------------------------------------

def create_poster(
    solution: Sequence[int],
    n: int,
    performance_df: Optional[pd.DataFrame] = None,
    conflict_history: Optional[Iterable[int]] = None,
    filename: Optional[str] = None,
    show: bool = False,
) -> Path:
    """
    Generate a multi-panel "poster" figure for large n (e.g., n >= 1000).

    Panels:
        - mini-board view (compressed)
        - performance curves (if provided)
        - conflicts vs time (if provided)
        - text box summarizing key observations
    """
    if filename is None:
        filename = f"poster_n{n}.png"

    has_perf = performance_df is not None
    has_conf = conflict_history is not None

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    ax_board, ax_perf, ax_conf, ax_text = axes.flatten()

    # --- Panel 1: Board (compressed if n is huge) ---
    arr = _board_to_array(solution, n)
    max_side = 200
    if n > max_side:
        factor = max(1, n // max_side)
        arr_small = arr[::factor, ::factor]
        board_title = f"{n}-Queens Solution (downsampled)"
    else:
        arr_small = arr
        board_title = f"{n}-Queens Solution"

    ax_board.imshow(arr_small, interpolation="nearest")
    ax_board.set_title(board_title)
    ax_board.axis("off")

    # --- Panel 2: Performance ---
    if has_perf:
        data = performance_df.sort_values("n")
        if "n" in data and "runtime" in data:
            ax_perf.plot(data["n"], data["runtime"], marker="o", label="Runtime (s)")
        if "n" in data and "iterations" in data:
            ax_perf.plot(
                data["n"],
                data["iterations"],
                marker="s",
                linestyle="--",
                label="Iterations",
            )
        ax_perf.set_xscale("log")
        ax_perf.set_xlabel("n (log scale)")
        ax_perf.set_ylabel("Value")
        ax_perf.set_title("Performance Summary")
        ax_perf.legend()
        ax_perf.grid(True, linestyle="--", alpha=0.5)
    else:
        ax_perf.axis("off")

    # --- Panel 3: Conflicts over time ---
    if has_conf:
        conflicts = list(conflict_history)
        steps = list(range(len(conflicts)))
        ax_conf.plot(steps, conflicts, marker=".")
        ax_conf.set_xlabel("Step")
        ax_conf.set_ylabel("# Conflicts")
        ax_conf.set_title("Conflict Reduction Over Time")
        ax_conf.grid(True, linestyle="--", alpha=0.5)
    else:
        ax_conf.axis("off")

    # --- Panel 4: Text Box (FINAL VERSION – no placeholders) ---
    text_lines = [
        f"MIN-CONFLICTS on {n}-Queens",
        "",
        "- The visualization shows a valid configuration with exactly one queen",
        "  per column and no attacking pairs.",
        "- The MIN-CONFLICTS algorithm starts from a random board and repeatedly",
        "  moves a queen that is in conflict to the row with the fewest conflicts.",
        "",
    ]

    if has_perf:
        text_lines.extend([
            "- The performance plot demonstrates that runtime grows slowly with n,",
            "  and the algorithm stays efficient even for large problem sizes.",
        ])

    if has_conf:
        text_lines.extend([
            "- The conflict-over-time curve shows how quickly the algorithm drives",
            "  the number of conflicts to zero before reaching a valid solution.",
        ])

    text_lines.extend([
        "",
        "Overall, these results highlight that MIN-CONFLICTS is an effective and",
        "scalable heuristic for solving very large n-Queens problems.",
    ])

    ax_text.axis("off")
    ax_text.text(
        0.01,
        0.99,
        "\n".join(text_lines),
        va="top",
        ha="left",
        wrap=True,
    )

    fig.suptitle(f"CP468 – MIN-CONFLICTS n-Queens Visualization (n = {n})")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    out_path = RESULTS_DIR / filename
    fig.savefig(out_path, dpi=300)

    if show:
        plt.show()
    else:
        plt.close(fig)

    return out_path

# ---------------------------------------------------------------------
# Example usage when running this file directly
# ---------------------------------------------------------------------

from src.person_a.min_conflicts import min_conflicts



def demo_with_person_a(n: int = 8) -> None:
    """
    Demo: call Person A's min_conflicts solver, convert the board,
    and visualize it for a given n.
    """
    print(f"Running MIN-CONFLICTS from Person A for n = {n}...")

    raw_board, steps = min_conflicts(n=n, max_steps=100000, random_seed=42)

    if raw_board is None:
        print(f"No solution found after {steps} steps.")
        return

    # Convert Person A's format (row->col) to this file's format (col->row)
    board_for_vis = board_row_to_col(raw_board)

    print(f"Solution found in {steps} steps.\n")
    print("ASCII BOARD:")
    print(ascii_board(board_for_vis))

    visualize_board(board_for_vis, n=n, show=True)


if __name__ == "__main__":
    # Change n here to try different sizes (<=100 for visualization)
    demo_with_person_a(n=8)

