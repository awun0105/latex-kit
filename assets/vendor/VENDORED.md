# Bundled third-party assets

Downloaded on 2026-11-08 and copied here so latexkit works offline.

| Folder | Source | Version | License | Kept |
|---|---|---|---|---|
| `opentikz/` | https://github.com/opentikz/opentikz | `main` @ `359befb` | figures: CC0 1.0 (`LICENSE-CONTENT`), code: MIT (`LICENSE-CODE`) | icons, templates, examples, reference, catalog.json, schema, skill, tools (site builder removed) |
| `scienceplots/` | https://github.com/garrettj403/SciencePlots | default branch, 2026-11-08 | MIT (`LICENSE`) | `styles/` (all `.mplstyle` files), README |
| `gradbars/` + `tex/latexkit/gradbars/` | https://github.com/Tape5try/gradbars | v1.2.3 @ `e6440ba` | MIT (`LICENSE`) | all `sty/*.sty` (unchanged) in `tex/latexkit/gradbars/`; README, CHANGELOG, Markdown docs and `docs/examples` here (images and TeX manual removed) |
| `plotneuralnet/` + `tex/latexkit/plotneuralnet/` | https://github.com/HarisIqbal88/PlotNeuralNet | `master` @ `e96bc85` | MIT (`LICENSE`) | layers `Box`, `RightBandedBox`, `Ball` in `tex/latexkit/plotneuralnet/`; `examples/`, `pycore/`, `pyexamples/` here; `figures/` + `catalog.json` = the examples as latexkit assets |
| `figures4papers/` | https://github.com/ChenLiu-1996/figures4papers | `main` @ `b709de1` (2026-10-19) | **CC BY-NC 4.0** (`LICENSE`): attribution required, no commercial use | `upstream/`: every `figure_*/*.py` script, the `scientific-figure-making` skill and README, unchanged (PNG outputs and `assets/` images, ~45 MB, removed); latexkit additions: `f4p.py`, `styles/*.mplstyle`, `recipes/` + `catalog.json` (12 plot assets of type `plot`) |

Not bundled, installed as tools instead (see `latexkit doctor`):

| Tool | Source | Used for |
|---|---|---|
| D2 | https://github.com/d2lang/d2 (v0.9.0 tested) | `diagrams/*.d2` |
| Mermaid CLI | https://github.com/mermaid-js/mermaid-cli | `diagrams/*.mmd` |
| Graphviz | https://graphviz.org | `diagrams/*.dot` |
| draw.io desktop | https://github.com/jgraph/drawio-desktop (Apache 2.0) | `diagrams/*.drawio` (`--export --format pdf --crop`) |
| PGF/TikZ, PGFPlots, tabularray, siunitx | TeX Live / MiKTeX | loaded by `latexkit.sty` |

Changes made for figures4papers (everything outside `upstream/` is new; it adapts upstream
code, so it stays under CC BY-NC 4.0 with credit to Chen Liu):
- `f4p.py` implements the API that `upstream/scientific-figure-making/references/api.md` describes
  (`PALETTE`, `FigureStyle`, `apply_publication_style`, `make_grouped_bar`, `make_trend`,
  `make_heatmap`, `finalize_figure`...) plus helpers taken from the scripts (`make_radar`,
  `gradient_line`, `alpha_ramp`, `legend_panel`, `mark_events`). Needs only matplotlib and numpy:
  the heatmap no longer uses seaborn, `text.usetex` is off, and Helvetica falls back to Arial,
  Liberation Sans or TeX Gyre Heros. `finalize_figure(fig, "name")` writes `figures/name.pdf`.
- `styles/figures4papers*.mplstyle`: the same rcParams for `use_style("figures4papers")`.
- `recipes/<id>/<id>.py`: one script per figure kind, rewritten from the upstream script named in
  `catalog.json` (`origin`), with example numbers in place of the papers' data.
- `tex/latexkit/latexkit-plot.sty`: the palette as `f4p*` colors and the `lkf4p`, `lkf4pbar` pgfplots
  styles.

Update figures4papers: clone again, replace `upstream/` (scripts, skill, README; skip PNGs), then run
`latexkit gallery`, which re-runs every recipe.

Update OpenTikZ: clone the repo again, replace `opentikz/` (drop `.git`, `.github`,
`skills-demos`, `tools/build_site.py`), then run `latexkit gallery` to check every figure still
compiles and regenerate `tex/latexkit/latexkit-opentikz-colors.tex`:

```bash
grep -rhoE "\\\\definecolor\{(ot|brand)[A-Za-z]*\}\{HTML\}\{[0-9A-Fa-f]{6}\}" --include=*.tex \
  assets/vendor/opentikz | sort -u
```

Changes made to PlotNeuralNet:
- `Box.sty`, `RightBandedBox.sty`, `Ball.sty`: the keys stored their values in `\fill`,
  `\caption`, `\name`, `\scale`, `\opacity`... and overwrote those commands for the whole
  document. The macros are renamed with a `\pnn` prefix (`\pnnFill`, `\pnnCaption`...).
  Keys and drawings are unchanged.
- `figures/*/*.tex` (copies of `examples/`): `\usepackage{import}\subimport{...}{init}` replaced by
  `\usepackage{latexkit-nn}`; text after `\end{document}` removed.
- `layers/init.tex` is replaced by `tex/latexkit/latexkit-nn.sty`, which also defines the colors
  (`\ConvColor`, `\PoolColor`...) and the `connection` edge style the examples share.
- `pycore/tikzeng.py`: `to_head()` writes `\usepackage{latexkit-nn}` instead of
  `\usepackage{import}\subimport{<path>/layers/}{init}`.
