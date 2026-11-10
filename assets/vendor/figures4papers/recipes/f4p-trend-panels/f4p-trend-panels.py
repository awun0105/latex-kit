"""Training and validation curves with uncertainty bands, plus a legend-only panel.
figures4papers: scientific-figure-making tutorial 2 (CC BY-NC 4.0).
"""
from pathlib import Path

import numpy as np

from f4p import PALETTE, FigureStyle, apply_publication_style, create_subplots, finalize_figure, legend_panel, make_trend

NAME = Path(__file__).stem
steps = np.linspace(0, 10, 50)   # example curves: replace with your logs (mean and std per step)
CURVES = {
    "Training": {"Ours": 0.5 + 0.4 * (1 - np.exp(-steps / 3)), "Baseline": 0.45 + 0.35 * (1 - np.exp(-steps / 4))},
    "Validation": {"Ours": 0.48 + 0.36 * (1 - np.exp(-steps / 3)), "Baseline": 0.44 + 0.30 * (1 - np.exp(-steps / 4))},
}
STD = 0.02
COLORS = [PALETTE["blue_main"], PALETTE["red_strong"]]

apply_publication_style(FigureStyle(font_size=15, axes_linewidth=2))
fig, axes = create_subplots(1, len(CURVES) + 1, figsize=(5 * (len(CURVES) + 1), 4))
for ax, (title, lines) in zip(axes, CURVES.items()):
    make_trend(ax, steps, list(lines.values()), list(lines), colors=COLORS,
               y_std=[np.full_like(steps, STD)] * len(lines), xlabel="Epoch", ylabel="Accuracy")
    ax.set_title(title)
handles, labels = axes[0].get_legend_handles_labels()
legend_panel(axes[-1], handles, labels)
finalize_figure(fig, NAME)
