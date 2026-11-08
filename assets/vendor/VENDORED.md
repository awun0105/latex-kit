# Bundled third-party assets

Downloaded on 2026-11-08 and copied here so latexkit works offline.

| Folder | Source | Version | License | Kept |
|---|---|---|---|---|
| `opentikz/` | https://github.com/opentikz/opentikz | `main` @ `359befb` | figures: CC0 1.0 (`LICENSE-CONTENT`), code: MIT (`LICENSE-CODE`) | icons, templates, examples, reference, catalog.json, schema, skill, tools (site builder removed) |
| `scienceplots/` | https://github.com/garrettj403/SciencePlots | default branch, 2026-11-08 | MIT (`LICENSE`) | `styles/` (all `.mplstyle` files), README |
| `gradbars/` + `tex/latexkit/gradbars/` | https://github.com/Tape5try/gradbars | v1.2.3 @ `e6440ba` | MIT (`LICENSE`) | all `sty/*.sty` (unchanged) in `tex/latexkit/gradbars/`; README, CHANGELOG, Markdown docs and `docs/examples` here (images and TeX manual removed) |
| `plotneuralnet/` + `tex/latexkit/plotneuralnet/` | https://github.com/HarisIqbal88/PlotNeuralNet | `master` @ `e96bc85` | MIT (`LICENSE`) | layers `Box`, `RightBandedBox`, `Ball` in `tex/latexkit/plotneuralnet/`; `examples/`, `pycore/`, `pyexamples/` here; `figures/` + `catalog.json` = the examples as latexkit assets |

Not bundled, installed as tools instead (see `latexkit doctor`):

| Tool | Source | Used for |
|---|---|---|
| D2 | https://github.com/d2lang/d2 (v0.9.0 tested) | `diagrams/*.d2` |
| Mermaid CLI | https://github.com/mermaid-js/mermaid-cli | `diagrams/*.mmd` |
| Graphviz | https://graphviz.org | `diagrams/*.dot` |
| draw.io desktop | https://github.com/jgraph/drawio-desktop (Apache 2.0) | `diagrams/*.drawio` (`--export --format pdf --crop`) |
| PGF/TikZ, PGFPlots, tabularray, siunitx | TeX Live / MiKTeX | loaded by `latexkit.sty` |

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
