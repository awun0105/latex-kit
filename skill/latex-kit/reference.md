# latexkit reference

Every snippet below compiles inside a document that loads `\usepackage[...]{latexkit}` with the
named module. `gallery/gallery.pdf` in the kit shows each one rendered next to its code.

## Package options

```latex
\usepackage[lang=vi, table, diagram, plot, code, box, math, algo, science]{latexkit}
```

| Option | Values | Effect |
|---|---|---|
| `lang` | `vi` (default), `en` | babel language, box titles, `\cref` names, theorem names |
| modules | `table diagram plot code box math algo science`, `all`, `none` | default on: table, diagram, code, box, math |
| `accent` | HTML hex, default `1F4E79` | main color (`accent`) |
| `style` | `modern` (default), `plain` | colored sans-serif headings or class defaults |
| `float` | `auto` (default), `here` | `here` = every figure/table placed `[H]` |
| `parskip` | flag | blank line between paragraphs |
| `margin` | length (default `2.5cm`), `none` | `none` keeps the class layout |
| `bib`, `bibfile` | `natbib` (default), `biblatex`, `none`; file name `references` | `\lkbibliography` prints it |
| `minted` | flag | Pygments highlighting (needs `-shell-escape`; `latexkit new --minted` sets it up) |

Load `geometry` before latexkit (or use `margin=`) to change the page layout.

## table

```latex
\begin{lktable}[H]{Main results}{tab:main}{l ccc}
  Method & PSNR\up & SSIM\up & LPIPS\down \\ \midrule
  Baseline   & 25.10          & 0.810          & 0.240 \\
  Prior      & \second{27.40} & \second{0.860} & \second{0.190} \\
  \lkhl Ours & \best{29.20}   & \best{0.890}   & \best{0.150} \\
\end{lktable}

\begin{lktablex}[H]{Options}{tab:opt}{l C C C}   % full width; L C R X share free space
  Criterion & A & B & C \\ \midrule
  Quality & \lkheat{0.6} & \lkheat{0.9} & \lkheat{0.4} \\   % cell shaded by value in [0,1]
  Speed   & \lkbar{0.8}  & \lkbar{0.5}  & \lkbar{0.9}  \\   % inline data bar
  LiDAR   & \cmark & \pmark & \xmark \\
\end{lktablex}

\begin{lktblr}{colspec={l S[table-format=2.1] S[table-format=1.3]}}   % tabularray + siunitx
  {Method} & {PSNR} & {SSIM} \\
  Ours & 28.8 & 0.893 \\
\end{lktblr}
```
### gradbars (data graphics in text and cells; docs: `assets/vendor/gradbars/docs/api.md`)
```latex
\gradbar[max=100, width=25mm, precision=1]{72.4}   \gradspark{3,5,2,8,6}
\gradheat[min=0, max=1]{0.7}   \gradstack{30,50,20}
\begin{gradtable}[width=\linewidth, header align=c]
  \gradcolumn{method}{Method}
  \gradcolumn[type=bar, mark=both, options={max=100, precision=1}]{score}{Score}
  \gradcolumn[type=number, mark=best, options={better=lower}]{time}{Time / ms}
  \gradrow{Baseline, 72.4, 18.2}
  \gradrow{Ours, 92.7, 11.5}          % NA = missing value
\end{gradtable}
```
`\UseTblrLibrary{gradbars}` is already called: gradbars columns work in `lktblr` too.

Also loaded: `booktabs tabularx tabularray gradbars multirow makecell longtable threeparttable`.
`\lkstripes` before a tabular gives zebra rows. `P{3cm}` = centered fixed-width column.

## diagram

Node styles (inside `\begin{tikzpicture}[lk]`): `process` (alias `box`), `terminal`, `decision`,
`io`, `datastore`, `note`, `layer=<width>`, `tag`. Edge styles: `flow` (alias `arrow`),
`dashflow`, `biflow`, `loop`. Edge label: `elabel`. Recolor any node: `lkcolor=lkteal`.

```latex
\begin{tikzpicture}[lk]
  \node[terminal]                (s)  {Start};
  \node[io,        right=of s]   (i)  {Read};
  \node[decision,  right=of i]   (d)  {Valid?};
  \node[process,   right=of d]   (p)  {Process};
  \node[datastore, below=of p]   (db) {Store};
  \draw[flow] (s) -- (i);  \draw[flow] (i) -- (d);
  \draw[flow] (d) -- node[elabel, above] {Yes} (p);
  \draw[flow] (p) -- (db);
  \draw[loop] (d.south) |- ++(0,-0.9) -| node[elabel, pos=0.25] {No} (i.south);
  \lkgroup{(d)(p)}{Core}                         % dashed frame with a label
\end{tikzpicture}

\begin{tikzpicture}[lk]                          % layered architecture
  \node[layer=10cm]                                 (a) {Application};
  \node[layer=10cm, below=3mm of a]                 (b) {Model};
  \node[layer=10cm, below=3mm of b, lkcolor=lkteal] (c) {Data};
\end{tikzpicture}

\lkpipeline{Data, Reconstruction, Simulation}      % nodes (p1) (p2) (p3)
\lkpipeline*[node distance=5mm]{Step 1, Step 2}   % vertical
\lktimeline{2020/NeRF, 2023/3DGS, 2024/{Street Gaussians}}

\begin{forest}
  for tree={draw=accent, fill=accent!8, rounded corners=2pt, font=\sffamily\small, l sep=6mm}
  [3D [Explicit [Mesh] [Gaussians]] [Implicit [NeRF] [SDF]]]
\end{forest}

\begin{sequencediagram}
  \newthread{c}{Client} \newinst[2]{s}{Server}
  \begin{call}{c}{request()}{s}{response}\end{call}
\end{sequencediagram}
```
Libraries loaded: arrows.meta positioning calc fit backgrounds matrix chains shapes.* decorations.*
mindmap trees shadows patterns quotes angles 3d svg.path. Layers: background, edges, main, foreground.

### Diagram files (Mermaid, D2, Graphviz, draw.io)

Write `diagrams/<name>.mmd`, `.d2`, `.dot`, `.gv` or `.drawio` (draw.io desktop exports it, cropped), then
`\lkdiagram[max width=0.8\linewidth]{diagrams/<name>}` (aliases `\lkmermaid \lkdtwo \lkgraphviz`).
latexmk builds the PDF through rules in `latexmkrc`; `latexkit render [-f]` does it by hand.
Mermaid theme: `diagrams/mermaid.json`. A missing tool yields a red notice PDF instead of an error;
after installing the tool run `latexkit render`.

### OpenTikZ figures

```bash
latexkit asset list attention        # search (icons, templates, examples)
latexkit asset show encoder-decoder  # metadata + edit_contract (parameters, invariants)
latexkit asset add encoder-decoder   # -> figures/encoder-decoder.tex (+ .meta.json)
```
```latex
\begin{figure}\centering
  \lktikzfig[max height=6cm]{figures/encoder-decoder}
  \caption{...}\label{fig:encdec}
\end{figure}
```
Edit the `\def` parameters at the top of the copied file. Keep node names and the palette
(`otblue otorange otteal otpurple otvermillion otyellow otgray`) as the meta file's
`edit_contract` says. The figure's `\newcommand`, colors and TikZ libraries run; its
`\usepackage` lines are skipped (`asset add` prints any package to add). A figure's
`\newcommand` may reuse a document command name; images next to the file are found.

### Neural-network blocks (PlotNeuralNet, assets of type `nn`)

`latexkit asset list nn` → `nn-alexnet nn-lenet nn-vgg16 nn-fcn8 nn-fcn32 nn-hed nn-unet
nn-unet-ushape nn-softmax-loss`. Or draw in the document (diagram module loads the layers):
```latex
\begin{tikzpicture}
  \pic[shift={(0,0,0)}] at (0,0,0) {RightBandedBox={name=c1, caption=conv1,
       xlabel={{"64","64"}}, zlabel=224, fill=\ConvColor, bandfill=\ConvReluColor,
       height=36, width={2,2}, depth=36}};
  \pic[shift={(0,0,0)}] at (c1-east) {Box={name=p1, fill=\PoolColor, opacity=0.5,
       height=28, width=1, depth=28}};
  \pic[shift={(2,0,0)}] at (p1-east) {Box={name=fc, caption=fc, xlabel={{"10",}},
       fill=\SoftmaxColor, height=3, width=1.5, depth=20}};
  \pic[shift={(1.5,0,0)}] at (fc-east) {Ball={name=sum, fill=\SumColor, radius=2.5, logo=$+$}};
  \draw[connection] (p1-east) -- node{\midarrow} (fc-west);
\end{tikzpicture}
```
Anchors: `<name>-east/-west/-north/-south/-anchor/-near/-far`. Colors: `\ConvColor \ConvReluColor
\PoolColor \UnpoolColor \FcColor \FcReluColor \SoftmaxColor \SumColor`. Edges: `connection`,
`copyconnection` with `\midarrow`, `\copymidarrow`. Python generator:
`assets/vendor/plotneuralnet/pycore/tikzeng.py` (`to_head`, `to_Conv`, `to_Pool`, `to_connection`...).

## plot

```latex
\begin{tikzpicture}
  \begin{axis}[lkplot, xlabel={Step}, ylabel={PSNR (dB)}, legend pos=south east]
    \addplot table[x=step, y=ours, col sep=comma] {plots/results.csv};
    \legend{Ours}
  \end{axis}
\end{tikzpicture}

\begin{axis}[lkbar, symbolic x coords={NeRF, 3DGS, Ours}, ylabel={FPS}, ymin=0]
  \addplot coordinates {(NeRF, 0.1) (3DGS, 120) (Ours, 95)};
\end{axis}
```
`lkplot` = Okabe-Ito colors with markers; `lkbar`, `lkhbar` for bars. groupplots, fillbetween,
statistics, dateplot libraries are loaded.

Python (SciencePlots styles ship in `plots/styles/`, no install of SciencePlots needed):
```python
from latexkit_plot import use_style, save
use_style("science", "ieee")          # also: nature, grid, no-latex, high-vis, bright, ...
fig, ax = plt.subplots(figsize=(3.4, 2.3))
save(fig, "psnr")                     # -> figures/psnr.pdf
```
Run `latexkit plot` (uses `uv run --with matplotlib` when uv exists), then `\lkfig{psnr}{Caption}{fig:psnr}`.

## code

```latex
\begin{lkcode}[Python][label=lst:train]{Training loop}
for x, y in loader: ...
\end{lkcode}
\lkcodefile[Python]{code/train.py}{optional title}
\begin{lkterminal}
$ pip install torch
\end{lkterminal}
\lkfile{path/to/file.py}     % file name in running text
```
Languages: any listings language plus `yaml`, `json`, `dockerfile`. Vietnamese text in code works.

## box

`keyidea info tip warning question examplebox summary`, each with optional title:
`\begin{warning}[Careful] ... \end{warning}`. New box: `\lknewbox{name}{color}{Tiêu đề}{Title}`.
`lkframe` = plain frame. `checklist` list with `\item` (open) and `\done` (checked).

## math

`amsmath amssymb mathtools bm`; environments `theorem lemma proposition corollary definition example
remark proof` (not in beamer, which has its own). Macros: `\R \N \Z \E \Prob \argmin \argmax
\abs{} \norm{} \vect{} \mat{} \T \dd`.

## algo, science

`algorithm` + `algpseudocode` (`\Require \Ensure \State \If \For \While \Return \Comment`), localized.
`siunitx` (`\SI{9.81}{\metre\per\second\squared}`, `\num{}`, `S` columns) and `mhchem` (`\ce{H2O}`).
Both need `texlive-science`; without it the document still compiles and shows a notice.

## Other helpers

`\lkkey{term}` highlighted term · `\todo{...}` · `\lkfig[0.8]{file}{Caption}{label}` ·
`\lkfigs{Caption}{label}{a/Left, b/Right}` · `\lktitlepage` with `\subtitle{}` and `\institution{}`.

## Document types

| Type | Class | Notes |
|---|---|---|
| `notes` | article | reading-note skeleton: paper details, summary, problem, contributions, method, results, assessment, next steps |
| `paper` | article + authblk | `\author[1,2]{...}` `\affil[1]{...}`; acknowledgments and data/code availability sections |
| `report` | report | roman-numbered front matter: acknowledgments, summary, contents, lists of figures/tables, abbreviations; chapters in `chapters/` |
| `book` | book | preface, lists, `\index{term}` + `\printindex` (imakeidx, latexmk runs makeindex) |
| `slides` | beamer | outline at each `\section`, references frame, backup frames after `\appendix` |
| `thesis` | report + scrextend 13pt, setspace 1.3, geometry 3.5/2/2.5/2.5 cm (loaded before latexkit) | `front/` cover, subcover, declaration, acknowledgments, abstract-vi/en, abbreviations; `chapters/01..05`, appendix |
| `proposal` | article | info table, objectives, plan as `ganttchart` (pgfgantt), budget table, risks |
| `poster` | tikzposter A0 | `\begin{columns}\column{0.33}\block{Title}{body}...\end{columns}`; color style `latexkit` uses `accent` |
| `exam` | exam | `\question[2]`, `\part[1]`, `\begin{choices}\choice ...\CorrectChoice`, `\begin{solution}`; uncomment `\printanswers` for the answer key (writing lines are hidden there) |
| `cv` | article + latexkit-cv | one column, plain text order for applicant tracking systems |
| `letter` | article + latexkit-cv | gray header band, date, recipient, subject, body, closing |

### latexkit-cv (cv, letter)
```latex
\cvheader{Jane Doe}{Computer Vision Engineer}{email@example.com, \href{https://github.com/username}{github.com/username}}
\cvsection{Experience}
\cventry{Company}{City}{Role}{2024 -- now}
\begin{cvitems} \item Built ... \end{cvitems}
\cvproject{Project}{PyTorch, FastAPI}{2025}
\cvskill{Languages}{Python, C++}
\letterheader{Jane Doe}{email@example.com, City}      % letter: gray band
```

### New template
A folder `templates/<name>/main.tex` becomes type `<name>`. Placeholders: `{{TITLE}} {{AUTHOR}}
{{DATE}} {{YEAR}} {{PKGOPTS}}`, `<<vi:...||en:...>>`, `%%IF module` ... `%%ENDIF` (also `%%IF a|b`,
`%%IF !a`). Optional `template.json`: `{"description", "modules", "options", "title", "minimal"}`.
Test with `-l vi`, `-l en`, `-m none` and fix every error.
