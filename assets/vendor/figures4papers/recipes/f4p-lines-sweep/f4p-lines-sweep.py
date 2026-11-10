"""Hyper-parameter sweep: one small panel per metric, thick lines with round markers.
figures4papers: figure_RNAGenScape/plot_sweep.py (CC BY-NC 4.0).
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from f4p import PALETTE, COMPACT, apply_publication_style, finalize_figure

NAME = Path(__file__).stem
X_LABEL = "Optimization step"
X = [1, 5, 10, 20, 40]
PANELS = {   # metric -> {setting: values} (example numbers)
    "Median change": {"increase": [0.29, 0.50, 0.57, 0.56, 0.55], "decrease": [-0.90, -1.28, -1.31, -1.28, -1.29]},
    "Success rate (%) $\\uparrow$": {"increase": [67.6, 77.3, 79.9, 79.4, 79.6], "decrease": [75.9, 84.7, 84.9, 84.7, 85.1]},
}
COLORS = {"increase": PALETTE["magenta"], "decrease": PALETTE["blue_main"]}

apply_publication_style(COMPACT)
fig, axes = plt.subplots(1, len(PANELS), figsize=(4.5 * len(PANELS), 4))
for i, (ax, (metric, lines)) in enumerate(zip(axes, PANELS.items())):
    for setting, ys in lines.items():
        ax.plot(X, ys, "-o", lw=3, ms=8, alpha=0.8, color=COLORS[setting], label=setting)
    ax.set_xticks(X)
    ax.set_xlabel(X_LABEL)
    ax.set_ylabel(metric)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
axes[-1].legend(loc="lower right")
finalize_figure(fig, NAME, tight_pad=1)
