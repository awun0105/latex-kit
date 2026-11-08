<a id="top"></a>

<p align="center"><img src="./assets/banner/banner.png" alt="latexkit: LaTeX notes, papers, reports, books and slides from one toolkit" /></p>

<div align="center">

**Quick LaTeX documents built on one package that every document type shares.**

[Tiếng Việt](README.md) · English

</div>

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
- [Advanced Usage](#advanced-usage)
- [Documentation](#documentation)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Overview

latex-kit is a LaTeX package (`latexkit`) and a command (`latexkit`). The command creates ready-to-build projects for notes, papers, reports, books and beamer slides, in Vietnamese or English. Every document type loads the same package, so a table, diagram or code block written for notes can be copied into a report or slides unchanged. The kit runs on Linux, macOS and Windows; [`gallery/gallery.pdf`](gallery/gallery.pdf) shows every component next to its code.

## Key Features

- **5 document types:** `notes`, `paper`, `report`, `book`, `slides`. Labels, box titles, `\cref` names and theorems follow `lang=vi` or `lang=en`.
- **Tables:** `lktable`, `lktablex`, `lktblr`, marks such as `\best` and `\cmark`, cells shaded by value, plus gradbars data bars and sparklines.
- **Diagrams:**
  - Drawn in TikZ: shared flowchart and architecture styles, `\lkpipeline`, `\lktimeline`.
  - Written as text or drawn in draw.io: Mermaid, D2, Graphviz and draw.io files, which latexmk turns into PDF.
- **Figure library:** 73 OpenTikZ figures and 9 PlotNeuralNet network architectures, added to a project with one command.
- **Charts:** pgfplots with the `lkplot` style, or matplotlib with the SciencePlots styles bundled in the kit.
- **Code, boxes, math, algorithms:** `lkcode`, `lkterminal`, `keyidea`, `warning`, `theorem`, `algorithm`, `siunitx`.
- **Coding-agent skill:** the `latex-kit` skill teaches Claude Code and Codex how to use the kit. When a request for a table, diagram or chart leaves things open, the agent asks up to 3 questions to pick the right component, and never invents data.

## Repository Structure

| Path | Contents |
|---|---|
| `latexkit.py` | The `latexkit` command (Python, standard library only) |
| `tex/latexkit/` | `latexkit.sty`, 8 modules, gradbars and the PlotNeuralNet 3D blocks |
| `templates/` | Templates for the 5 document types and shared files in `_common/` |
| `assets/vendor/` | Bundled assets: OpenTikZ, PlotNeuralNet, gradbars, SciencePlots |
| `gallery/` | Document showing every component with its code |
| `skill/latex-kit/` | Coding-agent skill and the `reference.md` lookup sheet |

## Getting Started

Requires Python 3.8+ and TeX Live or MiKTeX with LuaLaTeX and latexmk.

1. Get the repository, then install the package, the `latexkit` command and the skill:
   ```bash
   python3 latex-kit/latexkit.py install --skill
   ```
2. Check what is missing. The command lists missing engines, packages and tools, with install hints:
   ```bash
   latexkit doctor
   ```
   On Ubuntu/Debian, the recommended TeX packages are:
   ```bash
   sudo apt install texlive-luatex texlive-latex-extra texlive-pictures texlive-science \
     texlive-bibtex-extra texlive-xetex biber graphviz
   ```
3. Create a project. Run `latexkit new` with no arguments to answer one question at a time:
   ```bash
   latexkit new paper my-paper -t "My Paper" -l en -m all
   ```
4. Build it. The result is `my-paper/build/main.pdf`; `latexmk -pvc` rebuilds on every save.
   ```bash
   cd my-paper && latexmk
   ```

## Advanced Usage

**Common components.** The full list with examples is in [`reference.md`](skill/latex-kit/reference.md).

| Need | Write |
|---|---|
| Results table | `\begin{lktable}[H]{Caption}{tab:x}{l ccc} ... \end{lktable}` |
| Data bars in tables | `\gradbar[max=100]{72.4}`, `\gradspark{3,5,2}`, `gradtable` |
| Flowchart, architecture | `\begin{tikzpicture}[lk]` with nodes `process`, `decision`, `io`, `datastore` |
| Diagram file | `diagrams/x.mmd`, `.d2`, `.dot` or `.drawio`, then `\lkdiagram{diagrams/x}` |
| Library figure | `latexkit asset add nn-unet`, then `\lktikzfig{figures/nn-unet}` |
| Chart | `\begin{axis}[lkplot]`, or `latexkit plot` for `plots/*.py` |
| Code, note boxes | `lkcode`, `lkterminal`, `keyidea`, `warning`, `summary` |

**Package options.** `\usepackage[lang=en, accent=8B0000, style=plain, float=here, margin=2cm]{latexkit}`. For a venue submission, switch `\documentclass` to the venue class and add `style=plain, margin=none, bib=none` to keep the class layout.

**Diagram tools (optional).**
- Mermaid: `npm install -g @mermaid-js/mermaid-cli`.
- D2: download from [d2lang.com](https://d2lang.com/tour/install).
- Graphviz: install with `apt`, `brew` or `winget`.
- draw.io: download from [drawio-desktop](https://github.com/jgraph/drawio-desktop/releases).

When a tool is missing, the figure shows a red notice and the document still builds. After installing the tool, run `latexkit render`.

**Other commands.**
- `latexkit asset list <word>`: search the figure library.
- `latexkit bundle <folder>`: copy the package into a project, for Overleaf or another machine.
- `latexkit gallery`: rebuild the gallery.
- `latexkit --help`: list every command.

## Documentation

- [`gallery/gallery.pdf`](gallery/gallery.pdf): every component next to the code that makes it, plus the whole figure library.
- [`skill/latex-kit/reference.md`](skill/latex-kit/reference.md): package options, commands and environments of each module.
- [`assets/vendor/VENDORED.md`](assets/vendor/VENDORED.md): sources, versions and local changes of the bundled assets.

## Acknowledgments

The kit bundles [OpenTikZ](https://github.com/opentikz/opentikz), [PlotNeuralNet](https://github.com/HarisIqbal88/PlotNeuralNet), [gradbars](https://github.com/Tape5try/gradbars) and [SciencePlots](https://github.com/garrettj403/SciencePlots). Diagram files use [Mermaid](https://github.com/mermaid-js/mermaid-cli), [D2](https://github.com/d2lang/d2), [Graphviz](https://graphviz.org) and [draw.io](https://github.com/jgraph/drawio-desktop).

## License

The latex-kit code is released under the [MIT License](LICENSE). Bundled assets keep their own licenses: OpenTikZ figures are CC0 1.0; OpenTikZ code, PlotNeuralNet, gradbars and SciencePlots are MIT.

[Back to Top](#top)
