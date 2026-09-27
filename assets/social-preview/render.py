#!/usr/bin/env python3
"""Render a 1280x640 GitHub social preview in the portfolio's editorial-split blueprint style.

Usage: render.py SPEC.json OUTPUT.png

The spec is JSON; relative paths in it resolve against the spec's directory:

    {
      "color": "#146C43",                      block color, same as the offer's cover
      "heading": ["Line one", "line two"],     one to three lines
      "subtitle": "Short · dotted · summary",
      "steps": [{"label": "First step", "icon": "icons/a.svg"}, ...],   exactly three; icon optional
      "illustration": "illustration.svg",      optional SVG fragment drawn on a 728x640 blueprint grid
      "mark": "mark.svg"                       optional white logo, top left of the block
    }

Rendering uses headless Chrome (set CHROME to override the binary) and the vendored OFL fonts in ./fonts.
Only the standard library is required.
"""

import html
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
FONTS = HERE / "fonts"
WIDTH, HEIGHT = 1280, 640

WHITE = "#FFFFFF"

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
]

CROP = (
    '<path d="M0,0 h28 M0,0 v28 M728,0 h-28 M728,0 v28 M0,640 h28 M0,640 v-28 '
    'M728,640 h-28 M728,640 v-28" stroke-width="3"/>'
)


def grid():
    """Blueprint grid: a faint 32 px lattice with a stronger line every 128 px."""
    lines = []
    for x in range(0, 729, 32):
        opacity = 0.22 if x % 128 == 0 else 0.09
        lines.append(
            f'<path d="M{x},0 V640" stroke="{WHITE}" stroke-opacity="{opacity}" stroke-width="1"/>'
        )
    for y in range(0, 641, 32):
        opacity = 0.22 if y % 128 == 0 else 0.09
        lines.append(
            f'<path d="M0,{y} H728" stroke="{WHITE}" stroke-opacity="{opacity}" stroke-width="1"/>'
        )
    return "".join(lines)


def blueprint(inner):
    return (
        f'{grid()}<g fill="none" stroke="{WHITE}" stroke-width="2.5" stroke-linecap="round" '
        f'stroke-linejoin="round" font-family="JBM" font-size="18">{inner}{CROP}</g>'
    )


def font_faces():
    faces = [
        ("Inter", 400, "inter-latin-400-normal.woff2"),
        ("Inter", 600, "inter-latin-600-normal.woff2"),
        ("Inter", 700, "inter-latin-700-normal.woff2"),
        ("JBM", 400, "jetbrains-mono-latin-400-normal.woff2"),
        ("JBM", 600, "jetbrains-mono-latin-600-normal.woff2"),
    ]
    return "".join(
        f"@font-face{{font-family:{family};font-weight:{weight};src:url({(FONTS / name).as_uri()})}}"
        for family, weight, name in faces
    )


def image(path, size):
    return f'<img src="{path.as_uri()}" width="{size}" height="{size}" alt="">'


def load_spec(spec_path):
    spec = json.loads(spec_path.read_text())
    base = spec_path.parent
    for key in ("color", "heading", "subtitle", "steps"):
        if key not in spec:
            raise SystemExit(f"spec is missing '{key}'")
    if not 1 <= len(spec["heading"]) <= 3:
        raise SystemExit("heading must have one to three lines")
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", spec["color"]):
        raise SystemExit("color must be a hex color such as #0A62D0")
    if len(spec["steps"]) != 3 or not all(step.get("label") for step in spec["steps"]):
        raise SystemExit("steps must have exactly three entries, each with a label")

    def resolve(value):
        path = (base / value).resolve()
        if not path.is_file():
            raise SystemExit(f"file not found: {path}")
        return path

    for step in spec["steps"]:
        if step.get("icon"):
            step["icon"] = resolve(step["icon"])
    for key in ("illustration", "mark"):
        if spec.get(key):
            spec[key] = resolve(spec[key])
    return spec


def page(spec):
    color = spec["color"]
    heading = "<br>".join(html.escape(line) for line in spec["heading"])
    illustration = spec["illustration"].read_text() if spec.get("illustration") else ""
    mark = (
        f'<div class="mark">{image(spec["mark"], 44)}</div>' if spec.get("mark") else ""
    )
    steps = []
    for number, step in enumerate(spec["steps"], start=1):
        icon = (
            f'<div class="ic">{image(step["icon"], 48)}</div>'
            if step.get("icon")
            else ""
        )
        steps.append(
            f'<div class="st"><em>0{number}</em>{icon}<span>{html.escape(step["label"])}</span></div>'
        )
    css = f"""
{font_faces()}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{WIDTH}px;height:{HEIGHT}px;overflow:hidden}}
body{{font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased;position:relative;background:#FFFFFF;color:#111}}
.blk{{position:absolute;left:0;top:0;bottom:0;width:752px;background:{color};color:#fff}}
.mark{{position:absolute;left:56px;top:48px}}
.ill{{position:absolute;right:32px;top:28px}}
h1{{position:absolute;left:56px;bottom:104px;font-size:44px;line-height:1.08;font-weight:700;
    letter-spacing:-.03em;white-space:nowrap}}
.blk p{{position:absolute;left:56px;bottom:56px;font-size:21px;color:rgba(255,255,255,.86)}}
.steps{{position:absolute;left:800px;right:48px;top:50%;transform:translateY(-50%)}}
.st{{display:flex;align-items:center;gap:18px;padding:30px 0;border-top:2px solid #ECECEC}}
.st:last-child{{border-bottom:2px solid #ECECEC}}
.st em{{font:600 18px JBM,monospace;font-style:normal;color:{color};width:26px;flex:none}}
.st .ic{{width:48px;height:48px;display:flex;align-items:center;justify-content:center;flex:none}}
.st span{{font-size:22px;font-weight:600;letter-spacing:-.015em;line-height:1.2}}
"""
    body = f"""<div class="blk">{mark}
<svg class="ill" width="400" height="352" viewBox="0 0 728 640">{blueprint(illustration)}</svg>
<h1>{heading}</h1><p>{html.escape(spec["subtitle"])}</p></div>
<div class="steps">{"".join(steps)}</div>"""
    # The page only loads local fonts and images; the policy blocks scripts and network access from spec content.
    csp = "default-src 'none'; img-src file:; font-src file:; style-src 'unsafe-inline'"
    return (
        f'<!doctype html><html><head><meta charset="utf-8">'
        f'<meta http-equiv="Content-Security-Policy" content="{csp}">'
        f"<style>{css}</style></head><body>{body}</body></html>"
    )


def chrome():
    override = os.environ.get("CHROME")
    for candidate in [override] if override else CHROME_CANDIDATES:
        found = shutil.which(candidate) or (
            candidate if pathlib.Path(candidate).is_file() else None
        )
        if found:
            return found
    raise SystemExit("Chrome or Chromium not found; set CHROME to its path")


def render(spec_path, out_path):
    spec = load_spec(spec_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        src = pathlib.Path(tmp) / "preview.html"
        src.write_text(page(spec))
        result = subprocess.run(
            [
                chrome(),
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--allow-file-access-from-files",
                "--force-device-scale-factor=1",
                f"--window-size={WIDTH},{HEIGHT}",
                "--virtual-time-budget=3000",
                f"--screenshot={out_path.resolve()}",
                src.as_uri(),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
    if result.returncode != 0 or not out_path.is_file():
        raise SystemExit(
            f"Chrome failed to render {out_path} (exit {result.returncode}):\n{result.stderr}"
        )


def main(argv):
    if len(argv) != 3:
        raise SystemExit(__doc__)
    render(pathlib.Path(argv[1]).resolve(), pathlib.Path(argv[2]))
    print(f"wrote {argv[2]}")


if __name__ == "__main__":
    main(sys.argv)
