"""Small helper for paper figures with matplotlib.

    from latexkit_plot import use_style, save
    use_style("science", "ieee")     # any SciencePlots style names
    ...
    save(fig, "psnr")                # writes ../figures/psnr.pdf

The SciencePlots style files (MIT license, github.com/garrettj403/SciencePlots)
live next to this file in styles/, so SciencePlots itself does not need to be
installed. The figures4papers style is there too: use_style("figures4papers"),
or the helpers in f4p.py. List them with: python latexkit_plot.py
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
STYLES = HERE / "styles"
FIGURES = HERE.parent / "figures"

matplotlib.rcParams["pdf.fonttype"] = 42  # embed TrueType: text stays selectable in the PDF


def styles() -> dict[str, Path]:
    return {p.stem: p for p in STYLES.rglob("*.mplstyle")}


def use_style(*names: str) -> None:
    """Apply SciencePlots styles by name, in order (later ones override)."""
    found = styles()
    paths = []
    for n in names:
        if n in found:
            paths.append(str(found[n]))
        elif n in plt.style.available:
            paths.append(n)
        else:
            raise ValueError(f"unknown style {n!r}; available: {', '.join(sorted(found))}")
    plt.style.use(paths)


def save(fig, name: str, folder: Path | str | None = None, formats=("pdf",)) -> list[Path]:
    """Save a figure as figures/<name>.pdf (vector), tightly cropped."""
    out = Path(folder) if folder else FIGURES
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for ext in formats:
        path = out / f"{name}.{ext}"
        fig.savefig(path, bbox_inches="tight", pad_inches=0.02)
        written.append(path)
        print(f"saved {path}")
    return written


if __name__ == "__main__":
    print("SciencePlots styles:", ", ".join(sorted(styles())))
