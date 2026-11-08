---
name: latex-kit
description: Create and edit LaTeX notes, papers, reports, books and beamer slides with the latexkit package and CLI — shared tables with gradbars data bars, TikZ flowcharts/pipelines/architectures, OpenTikZ and PlotNeuralNet figure assets, Mermaid/D2/Graphviz/draw.io diagrams, pgfplots and SciencePlots charts, code blocks, note boxes, theorems and algorithms, in Vietnamese or English. Use when the user wants a new LaTeX document or template, or asks to add a table, diagram, flowchart, chart, code listing or figure to a latexkit project (main.tex with \usepackage{latexkit}).
---

# latex-kit

latexkit = one LaTeX package (`\usepackage{latexkit}`) shared by every document type,
plus a CLI (`latexkit`) that creates projects and builds their diagrams, plots and figures.
Kit location: `{{KIT}}` (CLI: `{{KIT}}/latexkit.py`, also on PATH as `latexkit` after `latexkit install`).

## Workflow

1. **New document** — never hand-write a preamble; generate it:
   ```bash
   latexkit new <notes|paper|report|book|slides> <folder> -t "Title" -a "Author" -l vi|en -m all
   ```
   `-m` takes modules: `table,diagram,plot,code,box,math,algo,science` or `all`
   (default: table,diagram,plot,code,box,math). Vietnamese always compiles with LuaLaTeX.
2. **Edit** `main.tex` (report/book: `chapters/*.tex`). Use the components below instead of
   raw LaTeX so every document looks the same.
3. **Build and verify** — always compile after editing and fix every error before finishing:
   ```bash
   cd <folder> && latexmk            # output: build/main.pdf, log: build/main.log
   ```
   latexmk turns `diagrams/*.mmd|*.dot|*.d2|*.drawio` into PDF automatically. Check the log with
   `grep -E '^[^ ]+:[0-9]+: ' build/main.log`. Look at pages with `pdftoppm -r 60 -png build/main.pdf /tmp/p`.
4. `latexkit doctor` lists missing engines, packages and tools.

## Components (full list with examples: reference.md)

| Need | Write |
|---|---|
| Result table | `\begin{lktable}[H]{Caption}{tab:x}{l ccc} head \\ \midrule rows \end{lktable}` — rules added for you |
| Full-width table | `lktablex` with `L C R X` columns; tabularray: `lktblr` |
| Data bars / sparklines in cells | gradbars: `\gradbar[max=100]{72.4}` `\gradspark{3,5,2}` `\gradheat` `\gradstack`, report table `gradtable` |
| Marks in cells | `\best{}` `\second{}` `\cmark` `\xmark` `\pmark` `\up` `\down` `\lkhl` (row) `\lkheat{0.7}` `\lkbar{0.7}` |
| Quick pipeline | `\lkpipeline{A, B, C}` (left→right), `\lkpipeline*{...}` (top→down) |
| Timeline | `\lktimeline{2020/NeRF, 2023/3DGS}` |
| Flowchart / architecture | `\begin{tikzpicture}[lk]` + nodes `process terminal decision io datastore note layer=10cm tag`, edges `flow dashflow biflow loop`, labels `elabel`, frame `\lkgroup{(a)(b)}{Label}`, recolor `lkcolor=lkteal` |
| Tree | `forest` environment |
| Sequence diagram | `sequencediagram` (pgf-umlsd) |
| Diagram file | write `diagrams/name.mmd` (Mermaid) / `.d2` (D2) / `.dot` (Graphviz) / `.drawio` (draw.io), then `\lkdiagram{diagrams/name}` |
| Library figure | `latexkit asset list <word>` → `latexkit asset add <id>` → `\lktikzfig{figures/<id>}`; edit the `\def` parameters at the top of the copied file (its `.meta.json` lists them) |
| CNN / encoder-decoder (3D blocks) | `latexkit asset list nn` (U-Net, VGG16, FCN...) or `\pic{Box={...}}` / `RightBandedBox` / `Ball` (PlotNeuralNet, see reference.md) |
| Image | `\lkfig[0.8]{file}{Caption}{fig:x}`; side by side `\lkfigs{Caption}{fig:x}{a/Left, b/Right}` |
| pgfplots chart | `\begin{axis}[lkplot, ...]` or `[lkbar, symbolic x coords={...}]` |
| Python chart | edit `plots/make_plots.py` (`use_style("science","ieee")`, `save(fig,"name")`), run `latexkit plot`, include `figures/name.pdf` |
| Code | `\begin{lkcode}[Python]{Title}...\end{lkcode}`, `\lkcodefile[Python]{code/x.py}`, `lkterminal` |
| Boxes | `keyidea info tip warning question examplebox summary`, optional `[Title]` |
| Math | `theorem lemma definition example remark proof`, `\R \E \argmin \norm{} \abs{} \vect{} \mat{} \T` |
| Algorithm | `algorithm` + `algorithmic` (`\Require \State \For \While \Comment`) |
| References | `\cref{...}` (localized names), `\citep{}`/`\citet{}`, bibliography: `\lkbibliography` |

## Rules

- Colors: use `accent`, `lkblue lkteal lkgreen lkorange lkred lkpurple lkgray` or the OpenTikZ
  palette `otblue otorange otteal otpurple otvermillion otgray` — never raw hex in the body.
- Do not redefine node styles per figure; extend with `lkcolor=<color>`, `minimum width=...`.
- Do not load geometry after latexkit; use the `margin=` option or load geometry first.
- Wide Mermaid flowcharts shrink; prefer `flowchart TD`, or draw in TikZ.
- Slides: frames with `lkcode`/`lkterminal` need `[fragile]`.
- Venue class (IEEEtran, cvpr, neurips, acmart): `\usepackage[style=plain, margin=none, bib=none, ...]{latexkit}`
  keeps the class layout, headings and bibliography style.
- Send a project elsewhere (Overleaf): `latexkit bundle <folder>` copies the package files in.
