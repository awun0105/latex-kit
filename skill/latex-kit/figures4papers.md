# figures4papers in latexkit

House style for publication figures from [figures4papers](https://github.com/ChenLiu-1996/figures4papers)
(Chen Liu; figures in Nature Machine Intelligence, ICML, NeurIPS, ECCV). License **CC BY-NC 4.0**:
keep the credit line, no commercial use. Vendored at `assets/vendor/figures4papers/` in the kit:
`f4p.py` (helpers), `styles/` (mplstyle), `recipes/` (12 scripts, `latexkit asset list plot`),
`upstream/` (original scripts and the upstream `scientific-figure-making` skill: open
`upstream/scientific-figure-making/references/design-theory.md` for the full rationale, and the
`upstream/figure_*/*.py` script named in a recipe's `origin` when the recipe is not close enough).

## When to use it

- Paper/report/poster figures that compare a proposed method with baselines: comparison or ablation
  bars, radar, sweeps, training curves, heatmaps, concept panels.
- Not for: exploratory plots, interactive charts, figures that must use the document font (use
  pgfplots `lkplot`, or `axis[lkf4p]` for the same look in pgfplots).

Ask first (guard in SKILL.md) when unclear: which method is "ours", which metrics/panels, and whether
the data is given. Never invent numbers: the recipes hold example values to replace.

## Rules of the style

1. Color story: **blue `#0F4D92` = proposed method**, `#3775BA` = its variants/ablations;
   greens (`#DDF3DE #AADCA9 #8BCF8B`) = related or improved methods; pinks/reds (`#F6CFCB #E9A6A1
   #B64342`) = baselines/contrasts; gray `#CFCECE` = reference; gold `#FFD700` = one callout only.
   Same mapping in every figure of the document.
2. Top/right spines off, no grid, frameless legend; sans font (Helvetica → Arial → Liberation Sans).
3. Sizes: big comparison bars `LARGE` (font 24, spines 3, wide canvas such as `(7*panels, 6)`);
   compact panels `COMPACT` (font 15, spines 2). The figure is scaled to `\linewidth` by `\lkfig[1]`,
   so keep the font/width ratio; a wider canvas gives smaller text in the PDF.
4. Many methods × several metrics: one panel per metric, `ax.set_xticks([])`, legend in its own panel
   (`legend_panel`). Tighten the y-range around the data (`tight_ylim`), never 0–100 when values sit
   in 80–95.
5. Bars get black edges (`linewidth` 1.5–3); hatches (`//`, `..`) when bars share a hue or the paper
   may be printed in gray. Ablations: one hue, opacity growing with completeness (`alpha_ramp`).
6. Lines: 2–4 curves per axis, width 2.5–3, uncertainty as `fill_between` bands.
7. Export: `finalize_figure(fig, "name")` → `figures/name.pdf` (vector, `tight_layout(pad=2)`,
   300 dpi for rasters, TrueType fonts). Add `formats=["pdf", "png"]` for slides or the web.

## f4p.py API

| Name | Use |
|---|---|
| `PALETTE`, `DEFAULT_COLORS`, `BASELINE_TO_OURS`, `HATCHES` | colors (keys: `blue_main blue_secondary green_1..3 red_1 red_2 red_strong neutral highlight teal violet magenta red_soft yellow_1 gray_1..3`) |
| `FigureStyle(font_size, axes_linewidth, use_tex)`, `LARGE`, `COMPACT` | style presets |
| `apply_publication_style(style)` | set rcParams once, before plotting |
| `create_subplots(r, c, figsize)` | `(fig, flat axes)` |
| `make_grouped_bar(ax, categories, series, labels, colors=, errors=, hatches=, annotate=)` | grouped bars; returns last `BarContainer` |
| `annotate_bars(ax, bars, fmt)` | values above bars |
| `make_trend(ax, x, ys, labels, y_std=)` | lines with bands |
| `make_heatmap(ax, m, xlabels, ylabels, cmap=, annotate=, vmin=, vmax=)` | heatmap without seaborn; returns `(image, colorbar)` |
| `make_scatter(ax, x, y)` | scatter with edges |
| `make_radar(polar_ax, axis_labels, values, labels, limits=, ticks=)` | radar, per-spoke scales |
| `gradient_line(ax, x, y, color)` | curve fading in left→right |
| `make_sphere_illustration(ax)` | shaded sphere for concept panels |
| `alpha_ramp(color, n)`, `tight_ylim(ax, values)`, `legend_panel(ax, handles, labels)`, `bar_handles(colors, labels)`, `mark_events(ax, x, y, {x: "label"})` | small helpers |
| `finalize_figure(fig, "name", formats=None)` | save to `figures/` and close |

## Recipes (`latexkit asset add <id>` → `plots/<id>.py`)

| Id | Figure | Upstream origin |
|---|---|---|
| `f4p-bars-comparison` | methods × metrics, error bars, legend panel | ImmunoStruct `plot_bars.py` |
| `f4p-bars-ablation` | horizontal ablation, opacity ramp, component labels from 0/1 codes | ImmunoStruct `plot_bars.py` |
| `f4p-bars-grouped` | grouped bars, hatches, values on top | skill tutorial 1, CellSpliceNet |
| `f4p-bars-panels` | grid of category panels, same methods | Brainteaser `plot_correctness_by_category.py` |
| `f4p-bars-log` | throughput on log axis with values | RNAGenScape `plot_comparison_speed.py` |
| `f4p-trend-cumulative` | cumulative areas by month, event arrows | ophthal_review `plot_trend.py` |
| `f4p-trend-panels` | train/val curves with bands, legend panel | skill tutorial 2 |
| `f4p-lines-sweep` | sweep panels, lines + markers | RNAGenScape `plot_sweep.py` |
| `f4p-lines-gradient` | fading training curves, dashed reference | VIGIL `plot_posttraining.py` |
| `f4p-radar` | radar with per-benchmark scales | VIGIL `plot_comparison_radar.py` |
| `f4p-heatmap` | annotated count matrix with totals | ophthal_review `plot_composition.py` |
| `f4p-sphere` | points on a shaded sphere | Dispersion `plot_idea.py` |

Each recipe saves `figures/<file name>.pdf`, so `--name results` gives `figures/results.pdf`.
`latexkit plot` runs every `plots/*.py` (except the helpers) with `uv run --with matplotlib --with numpy`.
