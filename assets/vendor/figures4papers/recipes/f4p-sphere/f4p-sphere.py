"""Concept panels: points on a shaded sphere, spread out vs. collapsed (embedding geometry).
figures4papers: figure_Dispersion/plot_idea.py (CC BY-NC 4.0).
"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from f4p import FigureStyle, apply_publication_style, finalize_figure, make_sphere_illustration

NAME = Path(__file__).stem
PANELS = [  # (title, angular spread of the points, point color)
    ("Spread out", 2 * np.pi, "#CDE5F8"),
    ("Collapsed", np.pi / 4, "#6A98CB"),
    ("Dispersed again", 2 * np.pi, "#6A98CB"),
]
N_POINTS = 16
rng = np.random.default_rng(1)


def points_in_disk(n, spread):
    r = np.sqrt(rng.uniform(0, 0.95, n))
    t = rng.uniform(np.pi / 2 - spread / 2, np.pi / 2 + spread / 2, n)
    return np.stack([r * np.cos(t), r * np.sin(t)], axis=1)


apply_publication_style(FigureStyle(font_size=22))
fig, axes = plt.subplots(1, len(PANELS), figsize=(6 * len(PANELS), 6))
for ax, (title, spread, color) in zip(axes, PANELS):
    make_sphere_illustration(ax, light_dir=(-0.5, 0.5, 0.8))
    pts = points_in_disk(N_POINTS, spread)
    for p in pts:
        ax.plot([p[0], 0], [p[1], 0], ls="--", color="black", lw=1, alpha=0.8)
    ax.scatter(pts[:, 0], pts[:, 1], s=80, facecolor=color, edgecolor="black", alpha=0.9, zorder=3)
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.4, 1.4)
    ax.set_axis_off()
    ax.set_title(title)
finalize_figure(fig, NAME)
