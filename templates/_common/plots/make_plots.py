"""<<vi:Vẽ đồ thị từ dữ liệu thí nghiệm, lưu vào figures/*.pdf.||en:Make figures/*.pdf from experiment data.>>

<<vi:Chạy||en:Run>>:  latexkit plot   (<<vi:hoặc||en:or>>: python make_plots.py)
<<vi:Styles của SciencePlots nằm sẵn trong plots/styles, không cần cài SciencePlots.||en:SciencePlots styles ship in plots/styles; SciencePlots itself is not needed.>>
"""
import csv
from pathlib import Path

import matplotlib.pyplot as plt

from latexkit_plot import use_style, save

# "science" + "ieee" = paper look; "no-latex" avoids needing LaTeX inside matplotlib.
# <<vi:Bỏ "no-latex" để chữ trong hình dùng font LaTeX.||en:Drop "no-latex" to render text with LaTeX.>>
use_style("science", "grid", "no-latex")

rows = list(csv.DictReader(open(Path(__file__).with_name("results.csv"))))
step = [int(r["step"]) for r in rows]

fig, ax = plt.subplots(figsize=(3.4, 2.3))
ax.plot(step, [float(r["baseline"]) for r in rows], label="Baseline")
ax.plot(step, [float(r["ours"]) for r in rows], label="Ours")
ax.set_xlabel("<<vi:Bước huấn luyện||en:Training step>>")
ax.set_ylabel("PSNR (dB)")
ax.legend()
save(fig, "psnr")   # -> figures/psnr.pdf
