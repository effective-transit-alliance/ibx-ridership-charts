#!/usr/bin/env -S mise exec -- uv run --script
# /// script
# requires-python = ">=3.15"
# dependencies = []
# ///
"""Generate ridership.svg and ridership.png from ridership.csv."""

import csv
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).parent
TITLE = "IBX and Related Ridership (average weekday riders)"
COLORS = {
    "IBX Projection": "#2a6fdb",
    "Other Projection": "#8db4f0",
    "Current Ridership": "#9aa3ad",
}
DEFAULT_COLOR = "#e07b39"

BAR_H = 28
GAP = 10
LABEL_W = 230
YEAR_W = 50
CHART_W = 520
VALUE_W = 70
TOP = 80
LEFT = 20
BOTTOM = 50
WIDTH = LEFT + LABEL_W + YEAR_W + CHART_W + VALUE_W + 20
FONT = "Helvetica, Arial, sans-serif"


def main():
    with open(HERE / "ridership.csv", newline="") as f:
        rows = [
            (r["label"], float(r["riders_per_day"]), r.get("year", ""), r["group"])
            for r in csv.DictReader(f)
        ]
    rows.sort(key=lambda r: r[1], reverse=True)

    max_val = max(v for _, v, _, _ in rows)
    step = 50000
    axis_max = -(-max_val // step) * step
    height = TOP + len(rows) * (BAR_H + GAP) + BOTTOM
    x0 = LEFT + LABEL_W + YEAR_W

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" font-family="{FONT}">',
        f'<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="{LEFT}" y="34" font-size="22" font-weight="bold" fill="#1a1a1a">{escape(TITLE)}</text>',
    ]

    # Legend.
    lx = LEFT
    groups = list(dict.fromkeys(g for _, _, _, g in rows))
    for g in groups:
        out.append(f'<rect x="{lx}" y="48" width="14" height="14" rx="2" fill="{COLORS.get(g, DEFAULT_COLOR)}"/>')
        out.append(f'<text x="{lx + 20}" y="60" font-size="14" fill="#333">{escape(g)}</text>')
        lx += 30 + 8 * len(g)

    # Gridlines and axis labels.
    plot_bottom = TOP + len(rows) * (BAR_H + GAP)
    v = 0
    while v <= axis_max:
        x = x0 + CHART_W * v / axis_max
        out.append(f'<line x1="{x:.1f}" y1="{TOP - 6}" x2="{x:.1f}" y2="{plot_bottom}" stroke="#e3e3e3"/>')
        out.append(
            f'<text x="{x:.1f}" y="{plot_bottom + 20}" font-size="13" fill="#666" '
            f'text-anchor="middle">{int(v / 1000)}k</text>'
        )
        v += step

    # Bars.
    for i, (label, val, year, group) in enumerate(rows):
        y = TOP + i * (BAR_H + GAP)
        w = CHART_W * val / axis_max
        cy = y + BAR_H / 2 + 5
        out.append(
            f'<text x="{x0 - YEAR_W - 6}" y="{cy}" font-size="15" fill="#1a1a1a" '
            f'text-anchor="end">{escape(label)}</text>'
        )
        out.append(
            f'<text x="{x0 - 10}" y="{cy}" font-size="14" fill="#777" '
            f'text-anchor="end">{escape(year)}</text>'
        )
        out.append(
            f'<rect x="{x0}" y="{y}" width="{w:.1f}" height="{BAR_H}" rx="3" '
            f'fill="{COLORS.get(group, DEFAULT_COLOR)}"/>'
        )
        out.append(f'<text x="{x0 + w + 8:.1f}" y="{cy}" font-size="14" fill="#333">{val:,.0f}</text>')

    out.append("</svg>")
    svg_path = HERE / "ridership.svg"
    svg_path.write_text("\n".join(out) + "\n")

    # 2x density for a crisp PNG in Google Docs.
    subprocess.run(
        ["magick", "-density", "192", str(svg_path), str(HERE / "ridership.png")],
        check=True,
    )


if __name__ == "__main__":
    main()
