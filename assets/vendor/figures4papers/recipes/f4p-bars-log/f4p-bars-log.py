"""Throughput / speed on a log axis, value printed above each bar, legend in two columns.
figures4papers: figure_RNAGenScape/plot_comparison_speed.py (CC BY-NC 4.0).
"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from f4p import PALETTE, FigureStyle, apply_publication_style, finalize_figure

NAME = Path(__file__).stem
RESULTS = [  # (method, mean, std, color) — example numbers
    ("Method A", 0.054, 0.003, "#BABBC6"),
    ("Method B", 0.0083, 0.0001, "#ECC4C4"),
    ("Method C", 0.0124, 0.0002, PALETTE["magenta"]),
    ("Method D", 0.77, 0.004, "#C4A8E8"),
    ("Method E", 0.39, 0.10, "#E8C48A"),
    ("Method F", 0.21, 0.002, "#70CAB4"),
    ("Ours", 0.95, 0.003, PALETTE["blue_main"]),
]

apply_publication_style(FigureStyle(font_size=16, axes_linewidth=2))
names, mean, std, colors = zip(*RESULTS)
mean, std = np.asarray(mean), np.asarray(std)
fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(names))
ax.bar(x, mean, yerr=std, color=colors, label=names, capsize=8,
       error_kw={"elinewidth": 1.5, "capthick": 1.5, "ecolor": "black"})
ax.set_xlim(-1, len(names))
ax.set_xticks([])
ax.set_yscale("log")
lo, hi = ax.get_ylim()
ax.set_ylim(lo, hi * 50)                       # room for the legend above the bars
for i, v in enumerate(mean):
    ax.text(i, v * 1.4, f"{v:.3f}", ha="center", va="bottom", fontsize=13)
ax.set_ylabel("Throughput $\\uparrow$\n(samples / ms)", fontsize=18)
ax.legend(loc="upper left", ncol=2, fontsize=14)
finalize_figure(fig, NAME, tight_pad=1)
