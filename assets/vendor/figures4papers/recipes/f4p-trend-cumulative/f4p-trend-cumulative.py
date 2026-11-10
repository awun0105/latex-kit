"""Cumulative counts over time as filled areas with event arrows, two stacked panels
(second one hatched for print). figures4papers: figure_ophthal_review/plot_trend.py (CC BY-NC 4.0).
"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from f4p import COMPACT, apply_publication_style, finalize_figure, mark_events

NAME = Path(__file__).stem
START = (2022, 11)                     # first month (year, month)
SERIES = {                             # name -> count per month (example numbers)
    "Method papers (text)": [0, 0, 1, 0, 2, 1, 1, 3, 2, 2, 4, 3, 3, 5, 4, 6, 5, 7, 6, 8],
    "Application papers (text)": [0, 1, 4, 2, 3, 6, 4, 5, 7, 6, 9, 8, 7, 10, 9, 11, 10, 12, 11, 13],
    "Method papers (multimodal)": [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 2, 1, 1, 2, 2, 1, 3, 2, 3],
    "Application papers (multimodal)": [0, 0, 1, 0, 1, 0, 2, 1, 1, 2, 3, 2, 2, 3, 3, 4, 3, 4, 5, 4],
}
EVENTS_TOP = {"2022-11": "Model v1", "2023-03": "Model v2*", "2023-12": "Model v3", "2024-04": "Model v4"}
EVENTS_BOTTOM = {"2023-02": "VLM v1", "2023-09": "VLM v2*", "2024-02": "VLM v3"}
COLORS = ["#9BC8FA", "#FFA8A6", "#13457E", "#850C0A"]   # light fills, dark lines

n = len(next(iter(SERIES.values())))
months = [f"{START[0] + (START[1] - 1 + i) // 12}-{(START[1] - 1 + i) % 12 + 1:02d}" for i in range(n)]
names = list(SERIES)
cum = {k: np.cumsum(v) for k, v in SERIES.items()}

apply_publication_style(COMPACT)
fig, axes = plt.subplots(2, 1, figsize=(14, 8))
for row, ax in enumerate(axes):
    a, b = names[2 * row], names[2 * row + 1]
    hatch = {} if row == 0 else {"edgecolor": "black"}
    ax.fill_between(months, 0, cum[b], color=COLORS[1], label=b, hatch=None if row == 0 else "\\\\\\", **hatch)
    ax.fill_between(months, 0, cum[a], color=COLORS[0], label=a, hatch=None if row == 0 else "///", **hatch)
    ax.plot(months, cum[a], lw=3, c=COLORS[2])
    ax.plot(months, cum[b], lw=3, c=COLORS[3])
    ax.set_ylim(0, max(cum[a].max(), cum[b].max()) * 1.35)
    ax.set_xticks(months[::6])
    ax.set_ylabel("Cumulative\npublications")
    ax.legend(loc="upper left")
    mark_events(ax, months, cum[b], EVENTS_TOP if row == 0 else EVENTS_BOTTOM)
finalize_figure(fig, NAME)
