"""Same methods across many categories: a grid of small bar panels plus a legend panel.
figures4papers: figure_Brainteaser/plot_correctness_by_category.py (CC BY-NC 4.0).
"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from f4p import BASELINE_TO_OURS, PALETTE, LARGE, apply_publication_style, bar_handles, finalize_figure, legend_panel

NAME = Path(__file__).stem
METHODS = ["Model 1.5B", "Model 14B", "Model 70B", "Chat model", "Reasoning model", "Ours"]
COLORS = BASELINE_TO_OURS[:len(METHODS) - 1] + [PALETTE["blue_secondary"]]
RESULT = {   # category -> one value per method (example numbers)
    "Algebra": [0.20, 0.54, 0.57, 0.66, 0.75, 0.82],
    "Geometry": [0.13, 0.42, 0.38, 0.29, 0.38, 0.67],
    "Number theory": [0.44, 0.56, 0.53, 0.68, 0.82, 0.85],
    "Combinatorics": [0.25, 0.42, 0.42, 0.63, 0.67, 0.75],
    "Logic": [0.03, 0.41, 0.45, 0.52, 0.62, 0.76],
}
NCOLS = 3

apply_publication_style(LARGE)
cells = len(RESULT) + 1
nrows = int(np.ceil(cells / NCOLS))
fig, axes = plt.subplots(nrows, NCOLS, figsize=(9 * NCOLS, 6 * nrows))
axes = axes.ravel()
for ax, (cat, vals) in zip(axes, RESULT.items()):
    ax.bar(np.arange(len(METHODS)), vals, color=COLORS, edgecolor="black", linewidth=1.2)
    ax.set_title(cat, fontsize=32, pad=20)
    ax.set_ylabel("Accuracy", fontsize=28)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
legend_panel(axes[len(RESULT)], bar_handles(COLORS, METHODS, edgecolor="black"), METHODS, fontsize=26)
for ax in axes[len(RESULT) + 1:]:
    ax.set_axis_off()
finalize_figure(fig, NAME)
