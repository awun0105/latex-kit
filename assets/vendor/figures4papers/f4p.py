"""figures4papers house style for latexkit plots.

    from f4p import PALETTE, apply_publication_style, FigureStyle, make_grouped_bar, finalize_figure
    apply_publication_style(FigureStyle(font_size=16))
    fig, ax = plt.subplots(figsize=(8, 4))
    make_grouped_bar(ax, ["A", "B"], [[0.9, 0.8], [0.7, 0.75]], ["Ours", "Baseline"], annotate=True)
    finalize_figure(fig, "comparison")          # -> ../figures/comparison.pdf

Style, palette and helpers follow the "scientific-figure-making" skill and the figure
scripts of figures4papers by Chen Liu (https://github.com/ChenLiu-1996/figures4papers),
licensed CC BY-NC 4.0: free to share and adapt with attribution, not for commercial use.
Only matplotlib and numpy are needed (no seaborn, no LaTeX inside matplotlib).
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib

if not os.environ.get("DISPLAY") and not os.environ.get("MPLBACKEND"):
    matplotlib.use("Agg")  # headless runs (latexkit plot, CI)

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import to_rgba  # noqa: E402

HERE = Path(__file__).resolve().parent
FIGURES = Path(os.environ.get("LATEXKIT_FIGURES") or HERE.parent / "figures")

# ---------------------------------------------------------------- colors
PALETTE = {
    "blue_main": "#0F4D92",       # proposed method / key result
    "blue_secondary": "#3775BA",  # proposed variants, ablation ramps
    "green_1": "#DDF3DE", "green_2": "#AADCA9", "green_3": "#8BCF8B",   # improvements
    "red_1": "#F6CFCB", "red_2": "#E9A6A1", "red_strong": "#B64342",    # baselines, contrasts
    "neutral": "#CFCECE",         # reference / background
    "highlight": "#FFD700",       # one callout only
    "teal": "#42949E", "violet": "#9A4D8E", "magenta": "#EA84DD",
    "gray_1": "#767676", "gray_2": "#4D4D4D", "gray_3": "#272727",
    "yellow_1": "#FFF6CC", "red_soft": "#D88F8A",
}
DEFAULT_COLORS = [PALETTE[k] for k in ("blue_main", "green_3", "red_strong", "teal", "violet", "neutral")]
# Baselines (light → strong) then the proposed method last, as in the Brainteaser / VIGIL figures.
BASELINE_TO_OURS = [PALETTE[k] for k in ("green_1", "green_2", "green_3", "red_1", "red_2", "yellow_1")]
HATCHES = ["", "//", "\\\\", "..", "xx", "--", "++"]

FONT_STACK = ("Helvetica", "Arial", "Liberation Sans", "TeX Gyre Heros", "Nimbus Sans", "DejaVu Sans",
              "sans-serif")
SAVE_FORMATS = ("pdf", "svg", "eps", "png", "jpg", "jpeg", "tif", "tiff")


@dataclass(frozen=True)
class FigureStyle:
    font_size: int = 16          # 24 for large bar panels, 15-16 for compact plots
    axes_linewidth: float = 2.5  # 3 for big bars, 2 for compact
    use_tex: bool = False        # True only when LaTeX is installed and labels need it
    font_family: tuple = FONT_STACK


LARGE = FigureStyle(font_size=24, axes_linewidth=3)
COMPACT = FigureStyle(font_size=15, axes_linewidth=2)


def apply_publication_style(style: FigureStyle | None = None) -> None:
    """Top/right spines off, frameless legends, sans font, vector-friendly export."""
    s = style or FigureStyle()
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": list(s.font_family),
        "font.size": s.font_size,
        "mathtext.fontset": "dejavusans",
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.linewidth": s.axes_linewidth,
        "axes.prop_cycle": matplotlib.cycler(color=DEFAULT_COLORS),
        "xtick.major.width": s.axes_linewidth * 0.8,
        "ytick.major.width": s.axes_linewidth * 0.8,
        "legend.frameon": False,
        "text.usetex": s.use_tex,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,     # TrueType: text stays selectable in the PDF
        "ps.fonttype": 42,
        "savefig.dpi": 300,
        "figure.facecolor": "white",
    })


def create_subplots(nrows: int = 1, ncols: int = 1, figsize=None, **kwargs):
    """(fig, axes) with axes always a flat 1-D array."""
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, squeeze=False, **kwargs)
    return fig, axes.ravel()


def finalize_figure(fig, out_path, formats: Iterable[str] | None = None, dpi: int = 300,
                    close: bool = True, pad: float = 0.05, tight_pad: float | None = 2,
                    **kwargs) -> list[Path]:
    """tight_layout + save. A bare name ("comparison") goes to the project's figures/ folder.

    formats: e.g. ["pdf", "png"]; default: the extension of out_path, else pdf (vector, for LaTeX).
    """
    out = Path(out_path)
    if out.parent == Path("."):
        out = FIGURES / out
    if formats is None:
        formats = [out.suffix[1:]] if out.suffix[1:].lower() in SAVE_FORMATS else ["pdf"]
    formats = [f.lower().lstrip(".") for f in formats]
    bad = [f for f in formats if f not in SAVE_FORMATS]
    if bad:
        raise ValueError(f"unsupported format(s) {bad}; use {', '.join(SAVE_FORMATS)}")
    if out.suffix[1:].lower() in SAVE_FORMATS:
        out = out.with_suffix("")
    if tight_pad is not None:
        fig.tight_layout(pad=tight_pad)
    out.parent.mkdir(parents=True, exist_ok=True)
    written = []
    for ext in formats:
        path = out.parent / f"{out.name}.{ext}"
        fig.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=pad, **kwargs)
        written.append(path)
        print(f"saved {path}")
    if close:
        plt.close(fig)
    return written


# ---------------------------------------------------------------- validation
def _1d(x, name: str) -> np.ndarray:
    a = np.asarray(x, dtype=float)
    if a.ndim != 1:
        raise ValueError(f"{name} must be 1-D, got shape {a.shape}")
    return a


def _2d(x, name: str) -> np.ndarray:
    a = np.asarray(x, dtype=float)
    if a.ndim == 1:
        a = a[None, :]
    if a.ndim != 2:
        raise ValueError(f"{name} must be 2-D, got shape {a.shape}")
    return a


# ---------------------------------------------------------------- small helpers
def alpha_ramp(color: str, n: int, lo: float = 0.2, hi: float = 1.0) -> list[tuple]:
    """Same hue, alpha lo→hi: ablation bars where 'more complete' = more opaque."""
    r, g, b, _ = to_rgba(color)
    return [(r, g, b, a) for a in np.linspace(lo, hi, n)]


def tight_ylim(ax, values, margin: float = 1.0, floor: float | None = None, ceil: float | None = None,
               errors=None) -> tuple[float, float]:
    """Y-limits around the data (min - margin*std, max + margin*std) so differences show."""
    v = np.asarray(values, dtype=float).ravel()
    e = np.zeros_like(v) if errors is None else np.asarray(errors, dtype=float).ravel()
    sd = v.std() if v.size > 1 and v.std() > 0 else max(abs(v.mean()) * 0.05, 1e-9)
    lo, hi = (v - e).min() - margin * sd, (v + e).max() + margin * sd
    if floor is not None:
        lo = max(lo, floor)
    if ceil is not None:
        hi = min(hi, ceil)
    ax.set_ylim(lo, hi)
    return lo, hi


def legend_panel(ax, handles, labels, loc: str = "center", **kwargs):
    """Turn an extra axis into a legend-only panel (keeps data panels clean)."""
    ax.set_axis_off()
    return ax.legend(handles, labels, loc=loc, frameon=False, **kwargs)


def bar_handles(colors: Sequence, labels: Sequence[str], hatches: Sequence[str] | None = None,
                edgecolor: str | None = None):
    """Legend handles for bars without drawing any bars."""
    from matplotlib.patches import Patch
    hatches = hatches or [""] * len(colors)
    return [Patch(facecolor=c, edgecolor=edgecolor or "none", hatch=h, label=l)
            for c, l, h in zip(colors, labels, hatches)]


# ---------------------------------------------------------------- plot helpers
def annotate_bars(ax, bars, fmt: str = "{:.2f}", fontsize: float = 10, padding: float = 3):
    """Write each bar's value above it."""
    for b in bars:
        h = b.get_height()
        ax.annotate(fmt.format(h), (b.get_x() + b.get_width() / 2, h), xytext=(0, padding),
                    textcoords="offset points", ha="center", va="bottom", fontsize=fontsize)


def make_grouped_bar(ax, categories: Sequence[str], series, labels: Sequence[str], ylabel: str = "Value",
                     colors: Sequence | None = None, annotate: bool = False, errors=None,
                     hatches: Sequence[str] | None = None, edgecolor: str = "black",
                     linewidth: float = 1.5, width: float = 0.8, fmt: str = "{:.2f}",
                     annotate_fontsize: float | None = None):
    """Grouped bars: one group per category, one bar per series. Returns the last BarContainer."""
    data = _2d(series, "series")
    if data.shape[1] != len(categories):
        raise ValueError(f"len(categories)={len(categories)} but each series has {data.shape[1]} values")
    if len(labels) != data.shape[0]:
        raise ValueError(f"{data.shape[0]} series but {len(labels)} labels")
    err = None if errors is None else _2d(errors, "errors")
    colors = list(colors or DEFAULT_COLORS)
    n = data.shape[0]
    w = width / n
    x = np.arange(len(categories))
    bars = None
    for i in range(n):
        bars = ax.bar(x - width / 2 + w * (i + 0.5), data[i], w, label=labels[i],
                      color=colors[i % len(colors)], edgecolor=edgecolor, linewidth=linewidth,
                      hatch=(hatches[i % len(hatches)] if hatches else None),
                      yerr=None if err is None else err[i], capsize=4 if err is not None else 0,
                      error_kw={"elinewidth": 1.5, "capthick": 1.5, "ecolor": "black"})
        if annotate:
            annotate_bars(ax, bars, fmt=fmt,
                          fontsize=annotate_fontsize or plt.rcParams["font.size"] * 0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel(ylabel)
    return bars


def make_trend(ax, x, y_series, labels: Sequence[str], colors: Sequence | None = None,
               ylabel: str | None = None, xlabel: str | None = None, show_shadow: bool = True,
               y_std=None, linewidth: float = 2.5, marker: str | None = None, alpha_band: float = 0.18):
    """Several lines over x; with y_std (or show_shadow) an uncertainty band around each."""
    x = _1d(x, "x")
    ys = [_1d(y, f"y_series[{i}]") for i, y in enumerate(y_series)]
    for i, y in enumerate(ys):
        if len(y) != len(x):
            raise ValueError(f"y_series[{i}] has {len(y)} values, x has {len(x)}")
    colors = list(colors or DEFAULT_COLORS)
    stds = None if y_std is None else [_1d(s, "y_std") for s in y_std]
    for i, y in enumerate(ys):
        c = colors[i % len(colors)]
        ax.plot(x, y, color=c, lw=linewidth, label=labels[i], marker=marker)
        if stds is not None:
            ax.fill_between(x, y - stds[i], y + stds[i], color=c, alpha=alpha_band, lw=0)
        elif show_shadow:
            band = 0.03 * (np.ptp(y) or abs(y.mean()) or 1)
            ax.fill_between(x, y - band, y + band, color=c, alpha=alpha_band, lw=0)
    if ylabel:
        ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    return ax


def make_heatmap(ax, matrix, x_labels=None, y_labels=None, cmap: str = "magma", cbar_label: str | None = None,
                 annotate: bool = False, fmt: str = "{:.2f}", vmin=None, vmax=None, linewidth: float = 1,
                 linecolor: str = "white", cbar: bool = True):
    """Heatmap with white cell borders, optional values in cells (no seaborn needed)."""
    m = _2d(matrix, "matrix")
    im = ax.pcolormesh(m, cmap=cmap, vmin=vmin, vmax=vmax, edgecolors=linecolor, linewidth=linewidth)
    ax.set_xlim(0, m.shape[1])
    ax.set_ylim(m.shape[0], 0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    ax.set_xticks(np.arange(m.shape[1]) + 0.5)
    ax.set_yticks(np.arange(m.shape[0]) + 0.5)
    ax.set_xticklabels(x_labels if x_labels is not None else [str(i) for i in range(m.shape[1])])
    ax.set_yticklabels(y_labels if y_labels is not None else [str(i) for i in range(m.shape[0])])
    if annotate:
        lo, hi = im.get_clim()
        for (r, c), v in np.ndenumerate(m):
            dark = (v - lo) / ((hi - lo) or 1) > 0.55
            ax.text(c + 0.5, r + 0.5, fmt.format(v), ha="center", va="center",
                    color="white" if dark else "black", fontsize=plt.rcParams["font.size"] * 0.8)
    cb = None
    if cbar:
        cb = ax.figure.colorbar(im, ax=ax)
        cb.outline.set_visible(False)
        if cbar_label:
            cb.set_label(cbar_label)
    return im, cb


def make_scatter(ax, x, y, label: str | None = None, color: str | None = None, size: float = 50,
                 alpha: float = 0.7, edgecolor: str = "black", linewidth: float = 0.8):
    x, y = _1d(x, "x"), _1d(y, "y")
    if len(x) != len(y):
        raise ValueError(f"x has {len(x)} values, y has {len(y)}")
    return ax.scatter(x, y, s=size, alpha=alpha, label=label, color=color or PALETTE["blue_main"],
                      edgecolors=edgecolor, linewidths=linewidth)


def make_sphere_illustration(ax, light_dir=(-0.5, 0.5, 0.8), resolution: int = 256, alpha: float = 0.3,
                             center=(0.0, 0.0), radius: float = 1.0):
    """Shaded disk that reads as a 3-D sphere (Dispersion figures), for concept panels."""
    xs = np.linspace(-1, 1, resolution)
    x, y = np.meshgrid(xs, xs)
    r2 = x ** 2 + y ** 2
    mask = r2 <= 1.0
    z = np.zeros_like(x)
    z[mask] = np.sqrt(1.0 - r2[mask])
    n = np.sqrt(x ** 2 + y ** 2 + z ** 2) + 1e-6
    light = np.asarray(light_dir, dtype=float)
    light /= np.linalg.norm(light)
    intensity = np.maximum(0.0, (x * light[0] + y * light[1] + z * light[2]) / n)
    shade = np.clip(-0.5 + 2.0 * intensity, 0, 1)
    rgba = np.ones((resolution, resolution, 4))
    rgba[..., :3] = shade[..., None]
    rgba[..., 3] = np.where(mask, alpha, 0.0)
    cx, cy = center
    ax.imshow(rgba, origin="lower", extent=[cx - radius, cx + radius, cy - radius, cy + radius],
              interpolation="bilinear")
    ax.set_aspect("equal")
    return ax


def make_radar(ax, axis_labels: Sequence[str], values, labels: Sequence[str], colors: Sequence | None = None,
               limits=None, ticks=None, fill_alpha: float = 0.05, linewidth: float = 2,
               label_fontsize: float | None = None, tick_fontsize: float | None = None, inner: float = 0.5):
    """Radar chart on a polar axis (VIGIL). values: (n_methods, n_axes).

    Each spoke can have its own scale: limits = [(lo, hi), ...] per axis (default: shared data range),
    ticks = [[...], ...] per axis, printed along the spoke. The ring between 0 and `inner` is left
    empty so small differences stay visible.
    """
    v = _2d(values, "values")
    k = len(axis_labels)
    if v.shape[1] != k:
        raise ValueError(f"{k} axis labels but values have {v.shape[1]} columns")
    colors = list(colors or DEFAULT_COLORS)
    if limits is None:
        lo, hi = np.nanmin(v), np.nanmax(v)
        pad = 0.1 * (hi - lo or 1)
        limits = [(lo - pad, hi + pad)] * k
    lim = np.asarray(limits, dtype=float)

    def norm(val, i):
        a, b = lim[i]
        return inner + (1 - inner) * np.clip((val - a) / ((b - a) or 1), 0, 1)

    ang = np.linspace(0, 2 * np.pi, k, endpoint=False)
    closed = np.append(ang, ang[0])
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 1)
    ax.grid(False)
    ax.spines["polar"].set_visible(False)
    ax.set_yticks([])
    ax.set_xticks(ang)
    ax.set_xticklabels([])
    ax.plot(closed, np.ones_like(closed), color="black", lw=0.8, zorder=4)
    for a in ang:
        ax.plot([a, a], [inner, 1], color="gray", lw=0.5, zorder=4)
    n_ring = max((len(t) for t in ticks), default=0) if ticks else 4
    for j in range(n_ring):
        if ticks:
            ring = [norm(t[min(j, len(t) - 1)], i) for i, t in enumerate(ticks)]
        else:
            ring = [inner + (1 - inner) * j / max(n_ring - 1, 1)] * k
        ax.plot(closed, np.append(ring, ring[0]), color="black", lw=0.5, alpha=0.6, zorder=4)
    for m in range(v.shape[0]):
        r = np.array([norm(val, i) for i, val in enumerate(v[m])])
        rc = np.append(r, r[0])
        c = colors[m % len(colors)]
        ax.plot(closed, rc, color=c, lw=linewidth, label=labels[m], zorder=5)
        ax.fill(closed, rc, color=c, alpha=fill_alpha, zorder=5)
        ax.scatter(ang, r, color=c, s=18, zorder=6, edgecolors="none")
    fs = label_fontsize or plt.rcParams["font.size"] * 0.75
    tfs = tick_fontsize or plt.rcParams["font.size"] * 0.55
    if ticks:
        for i, t in enumerate(ticks):
            for tv in t[1:]:
                ax.text(ang[i], norm(tv, i) + 0.02, f"{tv:g}", fontsize=tfs, ha="center", va="center",
                        rotation=-np.degrees(ang[i]), rotation_mode="anchor", clip_on=False)
    for a, lab in zip(ang, axis_labels):
        ax.text(a, 1.12 + 0.08 * abs(np.sin(a)), lab, fontsize=fs, ha="center", va="center", clip_on=False)
    return ax


def gradient_line(ax, x, y, color: str, alphas=(0.3, 0.9), linewidth: float = 3, marker: str = "o",
                  markersize: float = 9, label: str | None = None):
    """Line whose opacity grows left→right, with solid markers (VIGIL post-training curves)."""
    from matplotlib.collections import LineCollection
    x, y = _1d(x, "x"), _1d(y, "y")
    pts = np.column_stack([x, y])
    seg = np.stack([pts[:-1], pts[1:]], axis=1)
    r, g, b, _ = to_rgba(color)
    cols = [(r, g, b, a) for a in np.linspace(alphas[0], alphas[1], len(seg))]
    ax.add_collection(LineCollection(seg, colors=cols, linewidths=linewidth, capstyle="round"))
    ax.plot(x, y, color=color, lw=0, marker=marker, markersize=markersize, label=label)
    ax.autoscale_view()
    return ax


def mark_events(ax, x, y, events: dict, dy: float = 0.1, fontsize: float | None = None):
    """Arrow annotations above a curve: events = {x_value: "label"}; each '*' in a label lifts it."""
    xs = list(x)
    lo, hi = ax.get_ylim()
    for key, label in events.items():
        if key not in xs:
            continue
        i = xs.index(key)
        lift = (1 + 0.8 * label.count("*")) * dy * (hi - lo)
        ax.annotate(label.replace("*", ""), xy=(i if isinstance(key, str) else key, y[i]),
                    xytext=(i if isinstance(key, str) else key, y[i] + lift), ha="center", va="bottom",
                    fontsize=fontsize or plt.rcParams["font.size"] * 0.7,
                    arrowprops=dict(arrowstyle="-|>", lw=1.3, color="black", shrinkA=0, shrinkB=0,
                                    mutation_scale=15))


if __name__ == "__main__":
    print("PALETTE:")
    for k, v in PALETTE.items():
        print(f"  {k:15} {v}")
