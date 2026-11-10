#!/usr/bin/env python3
"""latexkit — create LaTeX projects (notes, paper, report, book, slides) that share
one component package, and manage their diagrams, plots and figure assets.

Runs on Windows, macOS and Linux with Python 3.8+ and no extra Python packages.
Run `latexkit --help` or `latexkit <command> --help`.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

KIT = Path(__file__).resolve().parent
TEX_DIR = KIT / "tex" / "latexkit"
TEMPLATES = KIT / "templates"
COMMON = TEMPLATES / "_common"
OPENTIKZ = KIT / "assets" / "vendor" / "opentikz"
PLOTNN = KIT / "assets" / "vendor" / "plotneuralnet"
F4P = KIT / "assets" / "vendor" / "figures4papers"
ASSET_ROOTS = {"OpenTikZ": OPENTIKZ, "PlotNeuralNet": PLOTNN, "figures4papers": F4P}
SCIENCEPLOTS = KIT / "assets" / "vendor" / "scienceplots" / "styles"
PYHELPER = KIT / "assets" / "python" / "latexkit_plot.py"
F4P_HELPER = F4P / "f4p.py"
F4P_STYLES = F4P / "styles"
PLOT_HELPERS = {"latexkit_plot.py", "f4p.py"}  # copied into plots/, not run by `latexkit plot`
SKILL_SRC = KIT / "skill" / "latex-kit"

TYPES = {
    "notes": "Ghi chú học tập, đọc paper / study and reading notes (article)",
    "paper": "Bài báo khoa học / research paper (article)",
    "report": "Báo cáo nhiều chương / multi-chapter report (report)",
    "book": "Sách, giáo trình / book with parts and chapters (book)",
    "slides": "Slide thuyết trình / presentation (beamer)",
    "thesis": "Luận văn, đồ án tốt nghiệp / thesis (report, front matter, lists)",
    "proposal": "Đề cương nghiên cứu / research proposal (article, plan, budget)",
    "poster": "Poster hội nghị A0 / conference poster (tikzposter)",
    "exam": "Bài tập, đề thi / assignment or exam (exam class, points, solutions)",
    "cv": "CV một cột / one-column CV (ATS friendly)",
    "letter": "Thư xin việc, thư trang trọng / cover or formal letter",
}
# Modules used when -m is not given, per type (other types: DEFAULT_MODULES).
TYPE_MODULES = {
    "proposal": ["table", "diagram", "plot", "box"],
    "poster": ["table", "diagram", "plot", "box", "math"],
    "exam": ["table", "math", "code"],
    "cv": [],
    "letter": [],
}
# Extra package options per type.
TYPE_OPTS = {
    "notes": ["parskip", "float=here"],
    "paper": ["style=plain"],
    "thesis": ["float=here"],
    "proposal": ["parskip"],
    "poster": ["style=plain", "margin=none", "float=here"],
    "exam": ["style=plain"],
    "cv": ["style=plain", "margin=none"],
    "letter": ["style=plain", "margin=none"],
}
DEFAULT_TITLES = {
    "notes": ("Ghi chú", "Notes"), "paper": ("Tên bài báo", "Paper Title"),
    "report": ("Báo cáo", "Report"), "book": ("Tên sách", "Book Title"),
    "slides": ("Bài trình bày", "Presentation"), "thesis": ("Tên đề tài", "Thesis Title"),
    "proposal": ("Đề cương nghiên cứu", "Research Proposal"), "poster": ("Tên poster", "Poster Title"),
    "exam": ("Bài kiểm tra", "Exam"), "cv": ("Nguyễn Văn A", "Jane Doe"),
    "letter": ("Thư ứng tuyển", "Cover Letter"),
}


def discover_templates() -> None:
    """Folders in templates/ without a built-in entry become types too.
    Optional templates/<name>/template.json: {"description", "modules", "options", "title", "minimal"}."""
    if not TEMPLATES.exists():
        return
    for d in sorted(TEMPLATES.iterdir()):
        if not d.is_dir() or d.name.startswith("_") or d.name in TYPES or not (d / "main.tex").exists():
            continue
        cfg = {}
        if (d / "template.json").exists():
            cfg = json.loads((d / "template.json").read_text(encoding="utf-8"))
        TYPES[d.name] = cfg.get("description", f"{d.name} (templates/{d.name})")
        if "modules" in cfg:
            TYPE_MODULES[d.name] = cfg["modules"]
        if "options" in cfg:
            TYPE_OPTS[d.name] = cfg["options"]
        if "title" in cfg:
            DEFAULT_TITLES[d.name] = (cfg["title"], cfg["title"])
        if cfg.get("minimal"):
            MINIMAL_TYPES.add(d.name)


# Types that need no diagrams/, plots/, code/ or references.bib from _common.
MINIMAL_TYPES = {"cv", "letter"}
discover_templates()
MODULES = {
    "table": "booktabs, tabularx, tabularray, gradbars, lktable, \\best, \\cmark, heat cells",
    "diagram": "TikZ styles, \\lkpipeline, \\lktimeline, OpenTikZ, PlotNeuralNet, Mermaid/Graphviz/D2/draw.io",
    "plot": "pgfplots with a shared look (lkplot, lkbar)",
    "code": "lkcode, \\lkcodefile, lkterminal (listings or minted)",
    "box": "keyidea, info, tip, warning, question, examplebox, summary",
    "math": "amsmath, theorems, \\R, \\argmin, \\norm",
    "algo": "algorithm + algpseudocode",
    "science": "siunitx, mhchem",
}
DEFAULT_MODULES = ["table", "diagram", "plot", "code", "box", "math"]
ENGINES = {"lualatex": 4, "xelatex": 5, "pdflatex": 1}
DIAGRAM_EXT = (".mmd", ".dot", ".gv", ".d2", ".drawio")


# ---------------------------------------------------------------- helpers
def say(msg: str = "") -> None:
    print(msg, flush=True)


def die(msg: str, code: int = 1) -> "None":
    print(f"latexkit: {msg}", file=sys.stderr)
    sys.exit(code)


def which(*names: str) -> str | None:
    for n in names:
        p = shutil.which(n)
        if p:
            return p
    return None


def ask(prompt: str, default: str = "", choices: list[str] | None = None) -> str:
    hint = f" [{default}]" if default else ""
    while True:
        try:
            val = input(f"{prompt}{hint}: ").strip()
        except EOFError:
            val = ""
        val = val or default
        if not choices or val in choices:
            return val
        say(f"  Chọn một trong / choose one of: {', '.join(choices)}")


def render_text(text: str, ctx: dict, modules: set[str], lang: str) -> str:
    """Fill a template: {{KEY}}, <<vi:...||en:...>>, and %%IF module ... %%ENDIF blocks."""
    out, stack = [], []
    for line in text.splitlines(keepends=True):
        s = line.strip()
        m = re.match(r"%%IF\s+(!?)([\w|]+)", s)
        if m:
            neg, names = m.group(1) == "!", m.group(2).split("|")
            hit = any(n in modules or n == lang for n in names)
            stack.append(hit != neg)
            continue
        if s.startswith("%%ENDIF"):
            stack.pop()
            continue
        if all(stack):
            out.append(line)
    text = "".join(out)
    pick = 1 if lang == "vi" else 2
    text = re.sub(r"<<vi:(.*?)\|\|en:(.*?)>>", lambda m: m.group(pick), text, flags=re.S)
    for k, v in ctx.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def copy_tree(src: Path, dst: Path, ctx: dict, modules: set[str], lang: str) -> None:
    for path in sorted(src.rglob("*")):
        rel = path.relative_to(src)
        if rel.as_posix() == "template.json":   # template settings, not part of the project
            continue
        target = dst / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix in {".tex", ".bib", ".md", ".py", ".json", ".mmd", ".dot", ".d2", ".drawio", ".csv"} \
                or path.name in {"latexmkrc", ".gitignore"}:
            target.write_text(render_text(path.read_text(encoding="utf-8"), ctx, modules, lang),
                              encoding="utf-8")
        else:
            shutil.copy2(path, target)


def copy_tree_file(path: Path, target: Path, ctx: dict, modules: set[str], lang: str) -> None:
    target.write_text(render_text(path.read_text(encoding="utf-8"), ctx, modules, lang), encoding="utf-8")


def texmfhome() -> Path:
    try:
        out = subprocess.run(["kpsewhich", "-var-value", "TEXMFHOME"], capture_output=True,
                             text=True, check=True).stdout.strip()
        if out:
            return Path(out).expanduser()
    except (OSError, subprocess.CalledProcessError):
        pass
    return Path.home() / "texmf"


def find_browser() -> str | None:
    env = os.environ.get("PUPPETEER_EXECUTABLE_PATH")
    if env:
        return env
    cands = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
             "microsoft-edge", "msedge", "chrome"]
    found = which(*cands)
    if found:
        return found
    for p in [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium"]:
        if Path(p).exists():
            return p
    return None


# ---------------------------------------------------------------- new
def cmd_new(a: argparse.Namespace) -> None:
    interactive = a.type is None or a.dir is None
    if interactive:
        say("latexkit — tạo project mới / new project\n")
        for k, v in TYPES.items():
            say(f"  {k:7} {v}")
        a.type = a.type or ask("\nLoại / type", "notes", list(TYPES))
        a.dir = a.dir or ask("Thư mục / folder", a.type)
        a.title = a.title or ask("Tiêu đề / title", "Untitled")
        a.author = a.author or ask("Tác giả / author", default_author())
        a.lang = a.lang or ask("Ngôn ngữ / language (vi, en)", "vi", ["vi", "en"])
        if a.modules is None:
            say("\nModule: " + ", ".join(MODULES) + ", all, none")
            a.modules = ask("Module", ",".join(TYPE_MODULES.get(a.type, DEFAULT_MODULES)) or "none")
    if a.type not in TYPES:
        die(f"unknown type '{a.type}'. Types: {', '.join(TYPES)}")
    lang = a.lang or "vi"
    mods = parse_modules(a.modules if a.modules is not None
                         else ",".join(TYPE_MODULES.get(a.type, DEFAULT_MODULES)) or "none")
    dst = Path(a.dir).expanduser().resolve()
    if dst.exists() and any(dst.iterdir()):
        die(f"{dst} already exists and is not empty")

    title = a.title or DEFAULT_TITLES.get(a.type, ("Tài liệu", "Untitled"))[0 if lang == "vi" else 1]
    # "none" first: only the chosen modules load (the package turns some on by default).
    opts = [f"lang={lang}", "none"] + sorted(mods, key=list(MODULES).index)
    opts += TYPE_OPTS.get(a.type, [])
    if a.bib != "natbib":
        opts.append(f"bib={a.bib}")
    if a.minted:
        opts.append("minted")
    ctx = {
        "TITLE": title,
        "AUTHOR": a.author or default_author(),
        "DATE": r"\today",
        "YEAR": str(_dt.date.today().year),
        "PKGOPTS": ", ".join(opts),
        "PDF_MODE": str(ENGINES[a.engine]),
        "ENGINE": a.engine,
        "SHELL_ESCAPE": "1" if a.minted else "0",
    }
    if lang == "vi" and a.engine == "pdflatex":
        say("note: Vietnamese needs LuaLaTeX or XeLaTeX; switching engine to lualatex")
        ctx["PDF_MODE"], ctx["ENGINE"] = "4", "lualatex"

    dst.mkdir(parents=True, exist_ok=True)
    if a.type in MINIMAL_TYPES:
        for name in ("latexmkrc", ".gitignore"):
            copy_tree_file(COMMON / name, dst / name, ctx, mods, lang)
    else:
        copy_tree(COMMON, dst, ctx, mods, lang)
    copy_tree(TEMPLATES / a.type, dst, ctx, mods, lang)
    if "plot" in mods and a.type not in MINIMAL_TYPES:
        install_plot_helpers(dst / "plots")
    else:
        shutil.rmtree(dst / "plots", ignore_errors=True)
    if "diagram" not in mods:
        shutil.rmtree(dst / "diagrams", ignore_errors=True)
        shutil.rmtree(dst / "figures", ignore_errors=True)
    if "code" not in mods:
        shutil.rmtree(dst / "code", ignore_errors=True)
    if a.bundle or not (texmfhome() / "tex" / "latex" / "latexkit" / "latexkit.sty").exists():
        do_bundle(dst, quiet=True)
        say("  (package copied into the project, so it compiles anywhere)")
    say(f"Created {dst}  [{a.type}, {lang}, {', '.join(sorted(mods))}]")
    say(f"  build:   cd \"{dst}\" && latexmk     (or: latexkit build \"{dst}\")")
    say("  output:  build/main.pdf")


def default_author() -> str:
    try:
        name = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True).stdout.strip()
        if name:
            return name
    except OSError:
        pass
    return os.environ.get("USER") or os.environ.get("USERNAME") or "Author"


def parse_modules(spec: str | None) -> set[str]:
    if spec is None:
        return set(DEFAULT_MODULES)
    names = {s.strip() for s in spec.replace(" ", ",").split(",") if s.strip()}
    if "all" in names:
        return set(MODULES)
    names.discard("none")
    bad = names - set(MODULES)
    if bad:
        die(f"unknown module(s): {', '.join(sorted(bad))}. Modules: {', '.join(MODULES)}, all")
    return names


# ---------------------------------------------------------------- render diagrams
def render_one(src: Path, force: bool = False, quiet: bool = False) -> bool:
    dst = src.with_suffix(".pdf")
    if not force and dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        if not quiet:
            say(f"  up to date  {src}")
        return True
    ext = src.suffix
    if ext == ".mmd":
        exe = which("mmdc", "mmdc.cmd")
        if not exe:
            say("  mmdc not found: npm install -g @mermaid-js/mermaid-cli")
            placeholder_pdf(dst, f"{src.name}: Mermaid CLI (mmdc) is not installed")
            return False
        cmd = [exe, "-q", "-i", str(src), "-o", str(dst)]
        cfg = src.parent / "mermaid.json"
        if cfg.exists():
            cmd += ["-c", str(cfg)]
        browser = find_browser()
        tmp = None
        if browser:
            tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
            json.dump({"executablePath": browser, "args": ["--no-sandbox"]}, tmp)
            tmp.close()
            cmd += ["-p", tmp.name]
        ok = run(cmd, quiet)
        if tmp:
            os.unlink(tmp.name)
    elif ext in (".dot", ".gv"):
        exe = which("dot", "dot.exe")
        if not exe:
            say("  dot not found: install Graphviz (apt install graphviz / brew install graphviz / winget install Graphviz)")
            placeholder_pdf(dst, f"{src.name}: Graphviz (dot) is not installed")
            return False
        ok = run([exe, "-Tpdf", str(src), "-o", str(dst)], quiet)
    elif ext == ".d2":
        exe = which("d2", "d2.exe")
        if not exe:
            say("  d2 not found: https://d2lang.com/tour/install")
            placeholder_pdf(dst, f"{src.name}: D2 is not installed")
            return False
        browser = find_browser()
        if browser:  # SVG printed by a browser: tight page, real fonts
            svg = dst.with_suffix(".tmp.svg")
            ok = run([exe, "--pad", "8", str(src), str(svg)], quiet) and svg_to_pdf(svg, dst, browser)
            svg.unlink(missing_ok=True)
        else:        # d2's own PDF export: works offline, page has extra white space
            ok = run([exe, "--pad", "10", str(src), str(dst)], quiet)
    elif ext == ".drawio":
        exe = find_drawio()
        if not exe:
            say("  draw.io not found: https://github.com/jgraph/drawio-desktop/releases")
            placeholder_pdf(dst, f"{src.name}: draw.io desktop is not installed")
            return False
        cmd = [exe, "--export", "--format", "pdf", "--crop", "--output", str(dst), str(src)]
        if sys.platform.startswith("linux"):
            cmd.insert(1, "--no-sandbox")
            if not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY") and which("xvfb-run"):
                cmd = ["xvfb-run", "-a"] + cmd   # Electron needs a display
        ok = run(cmd, quiet)
    else:
        say(f"  skip {src} (unknown type)")
        return False
    if not quiet:
        say(f"  {'built' if ok else 'FAILED'}  {src} -> {dst.name}")
    return ok


def find_drawio() -> str | None:
    exe = which("drawio", "draw.io", "drawio.exe")
    if exe:
        return exe
    for c in (Path.home() / ".local/opt/drawio/drawio",
              Path("/opt/drawio/drawio"),
              Path("/Applications/draw.io.app/Contents/MacOS/draw.io"),
              Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "draw.io" / "draw.io.exe",
              Path(os.environ.get("LOCALAPPDATA", "C:/")) / "Programs" / "draw.io" / "draw.io.exe"):
        if c.exists():
            return str(c)
    return None


def svg_to_pdf(svg: Path, pdf: Path, browser: str) -> bool:
    """Print an SVG to a PDF page of exactly its size with a headless browser."""
    text = svg.read_text(encoding="utf-8")
    m = re.search(r'<svg[^>]*?viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', text)
    if not m:
        return False
    w, h = m.group(1), m.group(2)
    html = (f'<!doctype html><html><head><meta charset="utf-8"><style>'
            f'@page{{size:{w}px {h}px;margin:0}}html,body{{margin:0;padding:0}}'
            f'body>svg{{display:block;width:{w}px;height:{h}px}}</style></head>'
            f'<body>{text[text.index("<svg"):]}</body></html>')
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "page.html"
        page.write_text(html, encoding="utf-8")
        out = Path(tmp) / "out.pdf"
        r = subprocess.run([browser, "--headless", "--disable-gpu", "--no-sandbox",
                            "--no-pdf-header-footer", f"--print-to-pdf={out}", page.as_uri()],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0 or not out.exists():
            sys.stderr.write(r.stderr)
            return False
        shutil.copy2(out, pdf)
    return True


def placeholder_pdf(pdf: Path, message: str) -> None:
    """Write a one-page PDF with a notice, dated 1970 so the next render replaces it."""
    msg = message.encode("ascii", "replace").replace(b"(", b"[").replace(b")", b"]")
    width = max(240, 7 * len(msg) + 30)
    stream = (b"1 0.4 0.4 RG 1 0.96 0.96 rg 1 w 1 1 %d 38 re B BT 0.7 0 0 rg /F1 12 Tf 14 15 Td (%s) Tj ET"
              % (width - 2, msg))
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d 40] /Contents 4 0 R "
            b"/Resources << /Font << /F1 5 0 R >> >> >>" % width,
            b"<< /Length %d >>\nstream\n%s\nendstream" % (len(stream), stream),
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    out, offsets = bytearray(b"%PDF-1.4\n"), []
    for i, o in enumerate(objs, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n%s\nendobj\n" % (i, o)
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    out += b"".join(b"%010d 00000 n \n" % off for off in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    pdf.write_bytes(bytes(out))
    os.utime(pdf, (0, 0))


def run(cmd: list[str], quiet: bool) -> bool:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stdout + r.stderr)
    return r.returncode == 0


def cmd_render(a: argparse.Namespace) -> None:
    targets = [Path(p) for p in (a.paths or ["diagrams"])]
    files: list[Path] = []
    for t in targets:
        if t.is_dir():
            files += sorted(p for p in t.rglob("*") if p.suffix in DIAGRAM_EXT)
        elif t.exists():
            files.append(t)
        else:
            die(f"{t} not found")
    if not files and not a.quiet:
        say("no .mmd / .dot / .gv / .d2 / .drawio files found")
    ok = all([render_one(f, a.force, a.quiet) for f in files])
    sys.exit(0 if ok else 1)


# ---------------------------------------------------------------- build / plot
def cmd_build(a: argparse.Namespace) -> None:
    d = Path(a.dir)
    if not which("latexmk"):
        die("latexmk not found. Install TeX Live or MiKTeX (with Perl for latexmk).")
    force = a.force
    if (d / "plots").is_dir() and a.plots:
        plot_dir(d)
        force = True  # new figures/*.pdf: make latexmk forget errors about missing files
    r = subprocess.run(["latexmk", *(["-g"] if force else []), "main.tex"], cwd=d)
    if r.returncode == 0:
        say(f"PDF: {d / 'build' / 'main.pdf'}")
    sys.exit(r.returncode)


def install_plot_helpers(plots: Path, force: bool = True) -> None:
    """plots/latexkit_plot.py + f4p.py and plots/styles/ (SciencePlots, figures4papers)."""
    styles = plots / "styles"
    styles.mkdir(parents=True, exist_ok=True)
    if force or not any(styles.rglob("science.mplstyle")):
        shutil.copytree(SCIENCEPLOTS, styles, dirs_exist_ok=True)
    if force or not (styles / "figures4papers").exists():
        shutil.copytree(F4P_STYLES, styles / "figures4papers", dirs_exist_ok=True)
    for src in (PYHELPER, F4P_HELPER):
        if force or not (plots / src.name).exists():
            shutil.copy2(src, plots / src.name)


def run_plot_script(script: Path, env: dict | None = None) -> bool:
    if which("uv"):
        cmd = ["uv", "run", "--quiet", "--with", "matplotlib", "--with", "numpy", "python", script.name]
    else:
        cmd = [sys.executable, script.name]
    r = subprocess.run(cmd, cwd=script.parent, env={**os.environ, **(env or {})})
    return r.returncode == 0


def plot_dir(d: Path) -> bool:
    scripts = sorted((d / "plots").glob("*.py"))
    scripts = [s for s in scripts if s.name not in PLOT_HELPERS]
    ok = True
    for s in scripts:
        say(f"  plot  {s.relative_to(d)}")
        if not run_plot_script(s):
            say("  failed. Needs matplotlib: pip install matplotlib numpy")
            ok = False
    return ok


def cmd_plot(a: argparse.Namespace) -> None:
    sys.exit(0 if plot_dir(Path(a.dir)) else 1)


# ---------------------------------------------------------------- assets (OpenTikZ, PlotNeuralNet, figures4papers)
def catalog() -> list[dict]:
    items = []
    for source, root in ASSET_ROOTS.items():
        path = root / "catalog.json"
        if not path.exists():
            continue
        for i in json.loads(path.read_text(encoding="utf-8")):
            items.append({**i, "source": source})
    if not items:
        die("asset catalogs are missing (assets/vendor/opentikz, plotneuralnet, figures4papers)")
    return items


def asset_tex(item: dict) -> Path:
    """The asset's source file: a standalone .tex figure, or a .py script for plot recipes."""
    d = ASSET_ROOTS[item.get("source", "OpenTikZ")] / item["path"]
    if item.get("type") == "plot":
        py = d / f"{Path(item['path']).name}.py"
        if not py.exists():
            die(f"no plot script {py}")
        return py
    for name in ("template.tex", "figure.tex", "example.tex", Path(item["path"]).name + ".tex"):
        if (d / name).exists():
            return d / name
    texs = sorted(d.glob("*.tex"))
    if not texs:
        die(f"no .tex file in {d}")
    return texs[0]


def cmd_asset(a: argparse.Namespace) -> None:
    items = catalog()
    if a.action == "list":
        q = (a.query or "").lower()
        types = {i["type"] for i in items}
        rows = [i for i in items if not q or (i["type"] == q if q in types else q in json.dumps(i).lower())]
        for i in rows:
            say(f"{i['type']:8} {i['id']:28} {i['name']}")
        say(f"\n{len(rows)} item(s). Add one: latexkit asset add <id>")
        return
    item = next((i for i in items if i["id"] == a.query or i["path"] == a.query), None)
    if not item:
        die(f"asset '{a.query}' not found. Try: latexkit asset list {a.query}")
    src = asset_tex(item)
    if a.action == "show":
        say(json.dumps(item, indent=2, ensure_ascii=False))
        meta = next(src.parent.glob("*.meta.json"), None)
        if meta:
            say(meta.read_text(encoding="utf-8"))
        say(f"\nsource: {src}")
        return
    # add
    if item.get("type") == "plot":
        add_plot_asset(a, item, src)
        return
    out_dir = Path(a.to or "figures")
    out_dir.mkdir(parents=True, exist_ok=True)
    name = a.name or item["id"]
    dst = out_dir / f"{name}.tex"
    if dst.exists() and not a.force:
        die(f"{dst} exists (use --force to overwrite)")
    shutil.copy2(src, dst)
    for img in src.parent.iterdir():   # images the figure includes (\includegraphics{cats.jpg})
        if img.suffix.lower() in {".png", ".jpg", ".jpeg"} and not img.name.startswith("preview"):
            shutil.copy2(img, out_dir / img.name)
    meta = next(src.parent.glob("*.meta.json"), None)
    if meta:
        shutil.copy2(meta, out_dir / f"{name}.meta.json")
    check_preamble(src)
    rel = dst.with_suffix("").as_posix()
    say(f"Added {dst}  ({item['source']}, {item.get('license', 'CC0-1.0')})")
    say("Use it in the document:")
    say("  \\begin{figure}\\centering")
    say(f"    \\lktikzfig{{{rel}}}")
    say(f"    \\caption{{{item['name']}}}\\label{{fig:{name}}}")
    say("  \\end{figure}")
    if meta:
        say(f"Edit the \\def parameters at the top of {dst.name}; {name}.meta.json lists them.")


def add_plot_asset(a: argparse.Namespace, item: dict, src: Path) -> None:
    """figures4papers recipe: plots/<name>.py (+ helpers); `latexkit plot` makes figures/<name>.pdf."""
    out_dir = Path(a.to or "plots")
    out_dir.mkdir(parents=True, exist_ok=True)
    name = a.name or item["id"]
    dst = out_dir / f"{name}.py"
    if dst.exists() and not a.force:
        die(f"{dst} exists (use --force to overwrite)")
    shutil.copy2(src, dst)
    install_plot_helpers(out_dir, force=False)
    fig = (out_dir.parent / "figures" / name).as_posix()
    say(f"Added {dst}  ({item['source']}, {item.get('license')}: attribution, non-commercial)")
    say(f"Replace the example numbers at the top of {dst.name}, then make the PDF:")
    say("  latexkit plot          (or: latexkit build)")
    say("Use it in the document:")
    say(f"  \\lkfig[1]{{{fig}}}{{{item['name']}}}{{fig:{name}}}")


PRELOADED = {"tikz", "amsmath", "amssymb", "xcolor", "graphicx", "latexkit-nn", "import"}


def check_preamble(src: Path) -> None:
    """Warn about packages a figure loads that latexkit does not (\\lktikzfig skips \\usepackage)."""
    pre = src.read_text(encoding="utf-8").split("\\begin{document}")[0]
    need = set()
    for m in re.finditer(r"^[^%\n]*\\usepackage(?:\[[^\]]*\])?\{([^}]*)\}", pre, flags=re.M):
        need |= {x.strip() for x in m.group(1).split(",")} - PRELOADED
    if need:
        say("Note: this figure also needs, in the document preamble:")
        say(f"  \\usepackage{{{', '.join(sorted(need))}}}")


# ---------------------------------------------------------------- bundle / install
def do_bundle(dst: Path, quiet: bool = False) -> None:
    for f in TEX_DIR.rglob("*"):   # flat copy: LaTeX finds the files next to main.tex
        if f.is_file() and f.suffix in {".sty", ".tex"}:
            shutil.copy2(f, dst / f.name)
    if not quiet:
        say(f"Copied latexkit package files into {dst}")


def cmd_bundle(a: argparse.Namespace) -> None:
    d = Path(a.dir)
    if not (d / "main.tex").exists():
        die(f"{d} has no main.tex")
    do_bundle(d)


def cmd_install(a: argparse.Namespace) -> None:
    target = texmfhome() / "tex" / "latex" / "latexkit"
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_symlink() or target.is_file():
        target.unlink()
    elif target.is_dir():
        shutil.rmtree(target)
    try:
        target.symlink_to(TEX_DIR, target_is_directory=True)
        say(f"Linked {target} -> {TEX_DIR}")
    except OSError:  # Windows without developer mode: copy instead
        shutil.copytree(TEX_DIR, target)
        say(f"Copied package to {target} (run `latexkit install` again after updates)")
    if which("mktexlsr") and os.name == "nt":
        subprocess.run(["initexmf", "--update-fndb"], capture_output=True)

    if os.name == "nt":
        say(f"Add a shortcut: create latexkit.cmd containing\n  @python \"{KIT / 'latexkit.py'}\" %*")
    else:
        bindir = Path.home() / ".local" / "bin"
        bindir.mkdir(parents=True, exist_ok=True)
        link = bindir / "latexkit"
        if link.exists() or link.is_symlink():
            link.unlink()
        link.symlink_to(KIT / "latexkit.py")
        say(f"Linked {link}")
    if a.skill:
        install_skill()


def install_skill() -> None:
    """Install the agent skill. With a skills hub (~/.agents/skills) the skill is copied
    there and linked into ~/.claude/skills and ~/.codex/skills; otherwise it is copied
    into ~/.claude/skills."""
    home = Path.home()
    hub = home / ".agents" / "skills"
    targets = [hub] if hub.is_dir() else [home / ".claude" / "skills"]
    for t in targets:
        t.mkdir(parents=True, exist_ok=True)
        dst = t / "latex-kit"
        _remove(dst)
        shutil.copytree(SKILL_SRC, dst)
        text = (dst / "SKILL.md").read_text(encoding="utf-8").replace("{{KIT}}", KIT.as_posix())
        (dst / "SKILL.md").write_text(text, encoding="utf-8")
        say(f"Installed skill: {dst}")
    if hub.is_dir():
        for agent in (home / ".claude" / "skills", home / ".codex" / "skills"):
            if not agent.parent.exists():
                continue
            agent.mkdir(parents=True, exist_ok=True)
            link = agent / "latex-kit"
            _remove(link)
            try:
                link.symlink_to(hub / "latex-kit", target_is_directory=True)
                say(f"Linked {link} -> {hub / 'latex-kit'}")
            except OSError:
                shutil.copytree(hub / "latex-kit", link)
                say(f"Copied skill to {link}")


def _remove(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def cmd_skill(a: argparse.Namespace) -> None:
    install_skill()


# ---------------------------------------------------------------- doctor
def cmd_doctor(a: argparse.Namespace) -> None:
    def row(name: str, ok: bool, hint: str = "") -> None:
        say(f"  [{'ok' if ok else '--'}] {name}" + ("" if ok else f"   -> {hint}"))

    say("Engines and build")
    for e in ("lualatex", "xelatex", "pdflatex", "latexmk", "biber"):
        row(e, bool(which(e)), "install TeX Live / MiKTeX" if e != "biber" else "needed only for bib=biblatex")
    say("LaTeX packages")
    for pkg in ("tikz", "pgfplots", "tcolorbox", "tabularray", "forest", "listings", "adjustbox",
                "siunitx", "algpseudocode", "biblatex", "minted", "fontspec", "pgf-umlsd"):
        r = subprocess.run(["kpsewhich", f"{pkg}.sty"], capture_output=True, text=True) if which("kpsewhich") else None
        row(pkg, bool(r and r.stdout.strip()), "texlive-science / texlive-bibtex-extra / tlmgr install " + pkg)
    r = subprocess.run(["kpsewhich", "latexkit.sty"], capture_output=True, text=True) if which("kpsewhich") else None
    row("latexkit.sty in TEXMFHOME", bool(r and r.stdout.strip()), "latexkit install")
    say("Diagram and plot tools")
    row("mmdc (Mermaid)", bool(which("mmdc", "mmdc.cmd")), "npm install -g @mermaid-js/mermaid-cli")
    row("browser for Mermaid", bool(find_browser()), "install Chrome/Chromium/Edge")
    row("dot (Graphviz)", bool(which("dot")), "apt install graphviz / brew install graphviz / winget install Graphviz")
    row("d2", bool(which("d2")), "https://d2lang.com/tour/install")
    row("draw.io desktop", bool(find_drawio()), "https://github.com/jgraph/drawio-desktop/releases")
    row("uv or matplotlib (plots)", bool(which("uv")) or _has_module("matplotlib"),
        "pip install matplotlib numpy")
    say("Assets")
    items = catalog()
    for source, root in ASSET_ROOTS.items():
        n = sum(1 for i in items if i["source"] == source)
        row(f"{source} ({n} figures)", n > 0, "re-clone the latex-kit repo")
    row("gradbars", (TEX_DIR / "gradbars" / "gradbars.sty").exists(), "re-clone the latex-kit repo")
    row("SciencePlots styles", SCIENCEPLOTS.exists(), "re-clone the latex-kit repo")
    row("figures4papers style (f4p.py)", F4P_HELPER.exists() and F4P_STYLES.exists(), "re-clone the latex-kit repo")


def _has_module(name: str) -> bool:
    import importlib.util
    return importlib.util.find_spec(name) is not None


# ---------------------------------------------------------------- gallery
def cmd_gallery(a: argparse.Namespace) -> None:
    g = KIT / "gallery"
    lines = ["% Generated by `latexkit gallery`: every OpenTikZ, PlotNeuralNet and figures4papers asset.\n"]
    plots = g / "plots"
    for item in catalog():
        if item.get("type") == "plot":   # run the recipe, show its PDF
            pdf = plots / f"{item['id']}.pdf"
            if not pdf.exists() or pdf.stat().st_mtime < asset_tex(item).stat().st_mtime:
                say(f"  plot  {item['id']}")
                run_plot_script(asset_tex(item), {"LATEXKIT_FIGURES": str(plots), "PYTHONPATH": str(F4P)})
            body = ("\\adjustbox{max width=\\linewidth, max height=4.2cm}{\\includegraphics{plots/%s}}"
                    % item["id"]
                    if pdf.exists() else "\\textit{(needs matplotlib)}")
            lines.append("\\begin{lkasset}{%s}{%s}{%s}\n  %s\n\\end{lkasset}\n"
                         % (item["type"], item["id"], item["name"].replace("&", "\\&"), body))
            continue
        rel = os.path.relpath(asset_tex(item).with_suffix(""), g).replace(os.sep, "/")
        lines.append(
            "\\begin{lkasset}{%s}{%s}{%s}\n  \\lktikzfig[max height=4.2cm]{%s}\n\\end{lkasset}\n"
            % (item["type"], item["id"], item["name"].replace("&", "\\&"), rel))
    (g / "catalog.tex").write_text("".join(lines), encoding="utf-8")
    r = subprocess.run(["latexmk", "gallery.tex"], cwd=g)
    if r.returncode == 0:
        shutil.copy2(g / "build" / "gallery.pdf", g / "gallery.pdf")
        say(f"Gallery: {g / 'gallery.pdf'}")
    sys.exit(r.returncode)


def cmd_list(a: argparse.Namespace) -> None:
    say("Types:")
    for k, v in TYPES.items():
        say(f"  {k:8} {v}")
    say("\nModules (default: " + ", ".join(DEFAULT_MODULES) + "):")
    for k, v in MODULES.items():
        say(f"  {k:8} {v}")


# ---------------------------------------------------------------- main
def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="latexkit", description=__doc__.split("\n\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    n = sub.add_parser("new", help="create a project (asks questions when type or folder is missing)")
    n.add_argument("type", nargs="?", choices=list(TYPES),
                   help="document type (latexkit list shows each one); omit to be asked")
    n.add_argument("dir", nargs="?", help="folder to create (must not exist or be empty)")
    n.add_argument("-t", "--title", help="document title (default depends on the type)")
    n.add_argument("-a", "--author", help="author name (default: git config user.name)")
    n.add_argument("-l", "--lang", choices=["vi", "en"],
                   help="language of labels, headings and sample text (default vi)")
    n.add_argument("-m", "--modules",
                   help="package parts to load: table,diagram,plot,code,box,math,algo,science, 'all' or 'none'"
                        " (default depends on the type)")
    n.add_argument("--engine", choices=list(ENGINES), default="lualatex")
    n.add_argument("--bib", choices=["natbib", "biblatex", "none"], default="natbib")
    n.add_argument("--minted", action="store_true", help="minted code highlighting (needs -shell-escape)")
    n.add_argument("--bundle", action="store_true", help="copy the package into the project")
    n.set_defaults(func=cmd_new)

    sub.add_parser("list", help="list document types and modules").set_defaults(func=cmd_list)

    r = sub.add_parser("render", help="build PDFs from .mmd / .dot / .gv / .d2 / .drawio files")
    r.add_argument("paths", nargs="*", help="files or folders (default: diagrams/)")
    r.add_argument("-f", "--force", action="store_true")
    r.add_argument("-q", "--quiet", action="store_true")
    r.set_defaults(func=cmd_render)

    b = sub.add_parser("build", help="run plots (if any) and latexmk in a project")
    b.add_argument("dir", nargs="?", default=".")
    b.add_argument("--no-plots", dest="plots", action="store_false")
    b.add_argument("-f", "--force", action="store_true", help="force a full rebuild")
    b.set_defaults(func=cmd_build)

    pl = sub.add_parser("plot", help="run plots/*.py (SciencePlots, figures4papers styles) to make figures/*.pdf")
    pl.add_argument("dir", nargs="?", default=".")
    pl.set_defaults(func=cmd_plot)

    s = sub.add_parser("asset", help="figure library (OpenTikZ, PlotNeuralNet, figures4papers plots): list, show, add")
    s.add_argument("action", choices=["list", "show", "add"])
    s.add_argument("query", nargs="?", help="search text (list) or asset id (show, add)")
    s.add_argument("--to", help="folder for `add` (default figures/; plot recipes: plots/)")
    s.add_argument("--name", help="file name for `add` (default: asset id)")
    s.add_argument("-f", "--force", action="store_true")
    s.set_defaults(func=cmd_asset)

    bu = sub.add_parser("bundle", help="copy the package into a project (for Overleaf or sharing)")
    bu.add_argument("dir", nargs="?", default=".")
    bu.set_defaults(func=cmd_bundle)

    i = sub.add_parser("install", help="make \\usepackage{latexkit} and the latexkit command work everywhere")
    i.add_argument("--skill", action="store_true", help="also install the agent skill")
    i.set_defaults(func=cmd_install)

    sub.add_parser("skill", help="install the latex-kit skill for coding agents").set_defaults(func=cmd_skill)
    sub.add_parser("doctor", help="check engines, packages and tools").set_defaults(func=cmd_doctor)
    sub.add_parser("gallery", help="build gallery/gallery.pdf with every component and asset").set_defaults(func=cmd_gallery)

    a = p.parse_args(argv)
    if a.cmd == "asset" and a.action in ("show", "add") and not a.query:
        die(f"asset {a.action} needs an id (see: latexkit asset list)")
    a.func(a)


if __name__ == "__main__":
    main()
