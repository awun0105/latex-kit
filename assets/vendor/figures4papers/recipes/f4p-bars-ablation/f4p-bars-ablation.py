"""Ablation study as horizontal bars: same blue, opacity grows as components are added.
figures4papers: figure_ImmunoStruct/plot_bars.py, ablation part (CC BY-NC 4.0).

Each row of ABLATIONS is a 0/1 code over COMPONENTS. Replace the numbers with yours.
"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from f4p import PALETTE, LARGE, alpha_ramp, apply_publication_style, finalize_figure, tight_ylim

NAME = Path(__file__).stem
COMPONENTS = ["Encoder", "Pre-training", "Contrastive"]
ABLATIONS = ["100", "110", "101", "111"]          # bottom -> top; last = full model
METRICS = ["AUROC", "AUPRC"]
MEAN = np.array([[0.78, 0.46], [0.81, 0.52], [0.80, 0.50], [0.85, 0.60]])   # example numbers
STD = np.array([[0.008, 0.012], [0.007, 0.010], [0.009, 0.011], [0.005, 0.008]])

labels = [" + ".join(c for c, bit in zip(COMPONENTS, code) if bit == "1") for code in ABLATIONS]
colors = alpha_ramp(PALETTE["blue_secondary"], len(ABLATIONS), 0.25, 1.0)

apply_publication_style(LARGE)
fig, axes = plt.subplots(1, len(METRICS), figsize=(10 * len(METRICS) + 4, 1.3 * len(ABLATIONS) + 2.5))
for j, ax in enumerate(np.atleast_1d(axes)):
    y = np.arange(len(ABLATIONS))
    ax.barh(y, MEAN[:, j], xerr=STD[:, j], color=colors, ecolor="k", capsize=5,
            edgecolor="black", linewidth=1.5)
    ax.set_yticks(y)
    ax.set_yticklabels(labels if j == 0 else [])
    if j:
        ax.tick_params(axis="y", length=0)
    lo, hi = tight_ylim(ax, MEAN[:, j], errors=STD[:, j], margin=1.5)
    ax.set_ylim(-0.6, len(ABLATIONS) - 0.4)
    ax.set_xlim(lo, hi)
    ax.set_xlabel(METRICS[j], fontsize=32)
finalize_figure(fig, NAME)
