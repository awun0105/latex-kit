"""Radar chart: one spoke per (model, benchmark), each benchmark with its own scale and
tick values along the spoke. figures4papers: figure_VIGIL/plot_comparison_radar.py (CC BY-NC 4.0).
"""
from pathlib import Path

import matplotlib.pyplot as plt

from f4p import PALETTE, LARGE, apply_publication_style, finalize_figure, make_radar

NAME = Path(__file__).stem
METHODS = ["Baseline A", "Baseline B", "Ours"]
COLORS = [PALETTE["red_soft"], PALETTE["green_3"], PALETTE["blue_main"]]
SCALES = {"Bench-1": [75, 80, 85, 91], "Bench-2": [30, 40, 50, 61], "Bench-3": [40, 55, 70, 85]}
RESULTS = {   # "model\nbenchmark" -> one value per method (example numbers)
    "Model-S\nBench-1": [82.8, 84.2, 86.9], "Model-M\nBench-1": [85.5, 86.8, 89.4],
    "Model-L\nBench-1": [84.5, 87.4, 89.8], "Model-S\nBench-2": [48.0, 48.8, 49.5],
    "Model-M\nBench-2": [57.9, 58.8, 60.1], "Model-L\nBench-2": [54.1, 55.4, 56.6],
    "Model-S\nBench-3": [71.2, 72.0, 72.5], "Model-M\nBench-3": [79.5, 80.1, 81.3],
    "Model-L\nBench-3": [77.2, 77.8, 78.5],
}

bench = [k.split("\n")[-1] for k in RESULTS]
ticks = [SCALES[b] for b in bench]
limits = [(min(t), max(t)) for t in ticks]
values = list(zip(*RESULTS.values()))          # (n_methods, n_spokes)

apply_publication_style(LARGE)
fig = plt.figure(figsize=(11, 10))
ax = fig.add_subplot(111, projection="polar")
make_radar(ax, list(RESULTS), values, METHODS, colors=COLORS, limits=limits, ticks=ticks,
           label_fontsize=15, tick_fontsize=12)
ax.legend(loc="upper right", bbox_to_anchor=(1.35, 0.08), fontsize=16)
finalize_figure(fig, NAME)
