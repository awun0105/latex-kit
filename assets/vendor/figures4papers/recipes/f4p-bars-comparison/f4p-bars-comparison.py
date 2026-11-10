"""Method comparison over several metrics: one panel per metric, error bars, no x ticks,
legend in its own panel. figures4papers: figure_ImmunoStruct/plot_bars.py (CC BY-NC 4.0).

Replace DATA with your results, then: latexkit plot  ->  figures/<this file name>.pdf
"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from f4p import PALETTE, LARGE, apply_publication_style, bar_handles, finalize_figure, legend_panel, tight_ylim

NAME = Path(__file__).stem
DATA = {  # example numbers: replace them
    "methods": ["Baseline A", "Baseline B", "Baseline C", "Baseline D", "Ours"],
    "colors": [PALETTE["neutral"], PALETTE["green_2"], PALETTE["green_3"], PALETTE["red_2"], PALETTE["blue_main"]],
    "metrics": ["AUROC", "AUPRC", "F1"],
    "mean": np.array([[0.71, 0.38, 0.33],
                      [0.74, 0.45, 0.36],
                      [0.77, 0.52, 0.40],
                      [0.79, 0.55, 0.43],
                      [0.84, 0.63, 0.49]]),
    "std": np.array([[0.010, 0.020, 0.015],
                     [0.012, 0.018, 0.012],
                     [0.008, 0.015, 0.010],
                     [0.010, 0.014, 0.011],
                     [0.006, 0.010, 0.008]]),
}

apply_publication_style(LARGE)
n_metric = len(DATA["metrics"])
fig, axes = plt.subplots(1, n_metric + 1, figsize=(7 * (n_metric + 1), 6))
x = np.arange(len(DATA["methods"]))
for j, ax in enumerate(axes[:-1]):
    ax.bar(x, DATA["mean"][:, j], yerr=DATA["std"][:, j], capsize=5, color=DATA["colors"],
           edgecolor="black", linewidth=1.5)
    ax.set_xticks([])
    tight_ylim(ax, DATA["mean"][:, j], errors=DATA["std"][:, j], margin=1.0, floor=0)
    ax.set_ylabel(DATA["metrics"][j], fontsize=32)
legend_panel(axes[-1], bar_handles(DATA["colors"], DATA["methods"], edgecolor="black"), DATA["methods"])
finalize_figure(fig, NAME)
