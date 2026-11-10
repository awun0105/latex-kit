"""Training curves that fade in left to right, dashed reference line, legend in two columns.
figures4papers: figure_VIGIL/plot_posttraining.py (CC BY-NC 4.0).
"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from f4p import PALETTE, LARGE, apply_publication_style, finalize_figure, gradient_line

NAME = Path(__file__).stem
STEPS = [0, 200, 400, 600, 800]
METHODS = {  # method -> (color, values) — example numbers
    "Baseline A": (PALETTE["red_soft"], [22.0, 25.5, 28.2, 29.5, 30.2]),
    "Baseline B": (PALETTE["green_3"], [22.0, 33.5, 38.2, 39.8, 40.5]),
    "Ours": (PALETTE["blue_main"], [22.0, 52.5, 56.8, 57.9, 58.5]),
}
REFERENCE = ("Before training", 22.0)

apply_publication_style(LARGE)
fig, ax = plt.subplots(figsize=(9, 8))
x = np.arange(len(STEPS))
ax.axhline(REFERENCE[1], color="black", alpha=0.3, lw=4, ls="--")
for name, (color, ys) in METHODS.items():
    gradient_line(ax, x, ys, color)
handles = [Line2D([0], [0], color="black", ls="--", lw=4, alpha=0.3, label=REFERENCE[0])]
handles += [Line2D([0], [0], color=c, lw=3, marker="o", ms=10, label=n) for n, (c, _) in METHODS.items()]
ax.legend(handles=handles, fontsize=20, loc="lower right", ncols=2)
ax.set_xticks(x)
ax.set_xticklabels([str(s) for s in STEPS])
ax.set_xlabel("Training steps", fontsize=28, labelpad=12)
ax.set_ylabel("Accuracy (%) $\\uparrow$", fontsize=28, labelpad=12)
ax.set_ylim(0, 65)
ax.tick_params(labelsize=20, length=8, width=1.5)
finalize_figure(fig, NAME)
