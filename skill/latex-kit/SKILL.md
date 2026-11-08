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
   latexkit new <type> <folder> -t "Title" -a "Author" -l vi|en [-m modules]
   ```
   Types: `notes paper report book slides thesis proposal poster exam cv letter` (`latexkit list`
   describes each; new folders in `templates/` become types too). `-m` takes
   `table,diagram,plot,code,box,math,algo,science`, `all` or `none`; omit it to get the type's
   defaults (cv/letter: none). Only the chosen modules load. Vietnamese compiles with LuaLaTeX.
   Pick the type from the request ("luận văn/đồ án" → thesis, "đề cương" → proposal, "đề thi/bài
   tập" → exam, "thư xin việc" → letter); ask only when two types fit.
2. **Edit** `main.tex` (report/book: `chapters/*.tex`). Use the components below instead of
   raw LaTeX so every document looks the same. Before adding a table, diagram, chart or figure,
   pass the guard below.
3. **Build and verify** — always compile after editing and fix every error before finishing:
   ```bash
   cd <folder> && latexmk            # output: build/main.pdf, log: build/main.log
   ```
   latexmk turns `diagrams/*.mmd|*.dot|*.d2|*.drawio` into PDF automatically. Check the log with
   `grep -E '^[^ ]+:[0-9]+: ' build/main.log`. Look at pages with `pdftoppm -r 60 -png build/main.pdf /tmp/p`.
4. `latexkit doctor` lists missing engines, packages and tools.

## Guard: ask before building a table, diagram, chart or figure

Each request maps to one latexkit component; a wrong guess means redrawing. Before writing one:

1. **List what the request leaves open** among the points in the table below. Answer from the
   request, the surrounding text, the data files in the project and visuals already in the document.
   Skip any point those settle. The request's wording picks the component ("kết quả", "các phương
   pháp" → `lktable`); existing visuals set the look (colors, size, wording). When a visual of the
   same kind already covers the topic, ask whether to edit it or add a new one. Caption, label and
   placement are not open points: write them from the context.
2. **Ask about the rest in one round** — at most 3 questions, each with 2–4 concrete options naming
   the latexkit component, the best fit first and marked recommended (AskUserQuestion when the
   agent has it, otherwise a short numbered list). Ask in the user's language.
3. **Never invent data or emphasis.** Numbers, labels or node names that are missing are asked
   for; when the user says to go ahead without them, mark each placeholder with `\todo{...}`. Add
   only the marks asked for ("tốt nhất" → `\best`, not `\second` or `\lkhl`).
4. **Run `latexkit doctor` before asking** and offer Mermaid, D2, Graphviz or draw.io only when
   the tool is installed; otherwise offer the TikZ equivalent and say which tool is missing.
5. **Go straight to work** when every point is settled, or the user says to decide ("tự chọn",
   "just do it"): pick the recommended option and name the choice in one line of the reply.

| Kind | Points to settle | Answer → component |
|---|---|---|
| Table | purpose; data source (given, `.csv`, to fill in later); emphasis; width; length | results/ablation → `lktable` + `\best \second \up \down`; criteria matrix or long text cells → `lktablex` (`L C R X`); numbers with units or decimal alignment → `lktblr` + `S` columns; bars, sparklines, ranking inside cells → gradbars (`gradtable`, `\gradbar`) or `\lkheat` `\lkbar`; spans pages → `longtable`; notes under the table → `threeparttable` |
| Diagram | what it shows; who edits it later; size and direction | steps with decisions or loops → `tikzpicture[lk]` flowchart; straight sequence → `\lkpipeline` (`*` = vertical); stacked layers → `layer` nodes; services and connections, auto layout → D2 (`.d2`); graph or dependency layout → Graphviz (`.dot`); message order between actors → `sequencediagram` (or Mermaid `sequenceDiagram`); taxonomy → `forest`; dated events → `\lktimeline`; CNN / encoder-decoder blocks → PlotNeuralNet asset (`latexkit asset list nn`) or `\pic{Box=...}`; known ML or system figure → OpenTikZ asset (`latexkit asset list <word>`); user wants to drag boxes by hand → draw.io (`.drawio`) |
| Chart | chart type; data source; look | trend → `axis[lkplot]`; categories → `axis[lkbar]` / `[lkhbar]`; data from code or many points → `plots/*.py` with SciencePlots + `latexkit plot`; match the document fonts → pgfplots |
| Figure / image | existing file or to draw; one or several | file → `\lkfig`; side by side → `\lkfigs`; to draw → the Diagram row |

Example questions for "vẽ sơ đồ hệ thống": *Sơ đồ thể hiện gì?* (luồng xử lý có rẽ nhánh → flowchart
TikZ · các thành phần và kết nối → D2 · các tầng chồng nhau → `layer`) and *Sau này sửa bằng gì?*
(sửa mã trong tài liệu → TikZ/D2 · kéo thả → draw.io).

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
| Type-specific | poster `\block{}{}` in `\column{}`; exam `\question[pts]`, `\part`, `choices`, `solution` (`\printanswers` = answer key); thesis files in `front/` and `chapters/`; cv/letter `\cvheader \cvsection \cventry \cvproject \cvskill \letterheader` (reference.md) |

## Rules

- Colors: use `accent`, `lkblue lkteal lkgreen lkorange lkred lkpurple lkgray` or the OpenTikZ
  palette `otblue otorange otteal otpurple otvermillion otgray` — never raw hex in `.tex` files.
  Diagram files (`.d2`, `.drawio`, `diagrams/mermaid.json`) keep hex colors close to `accent` (`#1F4E79`).
- Do not redefine node styles per figure; extend with `lkcolor=<color>`, `minimum width=...`.
- Do not load geometry after latexkit; use the `margin=` option or load geometry first.
- Wide Mermaid flowcharts shrink; prefer `flowchart TD`, or draw in TikZ.
- Slides: frames with `lkcode`/`lkterminal` need `[fragile]`.
- Venue class (IEEEtran, cvpr, neurips, acmart): `\usepackage[style=plain, margin=none, bib=none, ...]{latexkit}`
  keeps the class layout, headings and bibliography style.
- Send a project elsewhere (Overleaf): `latexkit bundle <folder>` copies the package files in.
