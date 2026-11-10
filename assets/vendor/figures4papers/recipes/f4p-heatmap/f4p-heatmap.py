"""Count matrix as an annotated heatmap with totals in the labels (no seaborn needed).
figures4papers: figure_ophthal_review/plot_composition.py (CC BY-NC 4.0).
"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from f4p import FigureStyle, apply_publication_style, finalize_figure, make_heatmap

NAME = Path(__file__).stem
COLUMNS = ["Benchmark\nevaluation", "Expert\nevaluation", "Retrospective\nvalidation",
           "Prospective\npilot", "Clinical\ntrial"]
ROWS = {   # row -> one count per column (example numbers)
    "Screening / diagnosis": [10, 7, 10, 3, 0],
    "Report generation": [2, 3, 3, 0, 0],
    "Treatment planning": [2, 3, 3, 2, 0],
    "Patient Q&A": [5, 13, 1, 1, 0],
    "Patient education": [1, 6, 0, 0, 0],
    "Exam taking": [19, 5, 0, 0, 0],
}

m = np.array(list(ROWS.values()))
ylabels = [f"{r}\n($n={m[i].sum()}$)" for i, r in enumerate(ROWS)]
xlabels = [f"{c}\n($n={m[:, j].sum()}$)" for j, c in enumerate(COLUMNS)]

apply_publication_style(FigureStyle(font_size=16, axes_linewidth=2))
fig, ax = plt.subplots(figsize=(13, 8.5))
_, cb = make_heatmap(ax, m, xlabels, ylabels, cmap="Reds", annotate=True, fmt="{:.0f}", vmin=0, vmax=20)
cb.set_ticks([0, 5, 10, 15, 20])
finalize_figure(fig, NAME)
