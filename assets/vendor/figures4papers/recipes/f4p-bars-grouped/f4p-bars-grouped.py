"""Grouped bars with black edges, hatching (readable in grayscale) and values on top.
figures4papers: scientific-figure-making tutorial 1, figure_CellSpliceNet (CC BY-NC 4.0).
"""
from pathlib import Path

import matplotlib.pyplot as plt

from f4p import PALETTE, FigureStyle, apply_publication_style, finalize_figure, make_grouped_bar

NAME = Path(__file__).stem
CATEGORIES = ["Dataset A", "Dataset B", "Dataset C", "Dataset D"]
SERIES = [[0.78, 0.80, 0.82, 0.79],     # example numbers: one row per method
          [0.85, 0.82, 0.88, 0.84],
          [0.92, 0.88, 0.91, 0.90]]
LABELS = ["Baseline X", "Baseline Y", "Ours"]
COLORS = [PALETTE["red_1"], PALETTE["green_2"], PALETTE["blue_main"]]

apply_publication_style(FigureStyle(font_size=18, axes_linewidth=2.5))
fig, ax = plt.subplots(figsize=(12, 4.8))
make_grouped_bar(ax, CATEGORIES, SERIES, LABELS, ylabel="Accuracy", colors=COLORS,
                 hatches=["//", "..", ""], annotate=True, fmt="{:.2f}")
ax.set_ylim(0.7, 1.0)
ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.18))
finalize_figure(fig, NAME)
