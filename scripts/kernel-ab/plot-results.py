#!/usr/bin/env python3

from pathlib import Path
import csv
import html
import statistics

BASE = Path(__file__).resolve().parents[2]
DATA = BASE / "data/kernel-ab/20261003"
FIG = BASE / "figures/kernel-ab/20261003"

FIG.mkdir(parents=True, exist_ok=True)


def read_csv(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


rows = read_csv(DATA / "summary.csv")
lab4_rows = read_csv(DATA / "lab4-fixed-reference.csv")

for r in rows:
    r["pp512_tps"] = float(r["pp512_tps"])

for r in lab4_rows:
    r["run"] = int(r["run"])
    r["pp512_tps"] = float(r["pp512_tps"])


def values(node, kernel):
    return [
        r["pp512_tps"]
        for r in rows
        if r["node"] == node and r["kernel"] == kernel
    ]


def svg_bar_chart(path, title, labels, means, errors, ymax=None):
    width = 1000
    height = 620

    left = 90
    right = 40
    top = 70
    bottom = 125

    plot_w = width - left - right
    plot_h = height - top - bottom

    if ymax is None:
        ymax = max(m + e for m, e in zip(means, errors)) * 1.18

    bar_space = plot_w / len(labels)
    bar_w = bar_space * 0.58

    def y(v):
        return top + plot_h - (v / ymax) * plot_h

    out = []

    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
    )
    out.append('<rect width="100%" height="100%" fill="white"/>')

    out.append(
        f'<text x="{width/2}" y="35" text-anchor="middle" '
        f'font-family="sans-serif" font-size="24">'
        f'{html.escape(title)}</text>'
    )

    # horizontal grid and Y labels
    ticks = 7
    for i in range(ticks + 1):
        v = ymax * i / ticks
        yy = y(v)

        out.append(
            f'<line x1="{left}" y1="{yy:.1f}" '
            f'x2="{width-right}" y2="{yy:.1f}" '
            f'stroke="#dddddd" stroke-width="1"/>'
        )

        out.append(
            f'<text x="{left-12}" y="{yy+5:.1f}" '
            f'text-anchor="end" font-family="sans-serif" '
            f'font-size="14">{v:.0f}</text>'
        )

    # axes
    out.append(
        f'<line x1="{left}" y1="{top}" '
        f'x2="{left}" y2="{top+plot_h}" '
        f'stroke="black" stroke-width="1.5"/>'
    )

    out.append(
        f'<line x1="{left}" y1="{top+plot_h}" '
        f'x2="{width-right}" y2="{top+plot_h}" '
        f'stroke="black" stroke-width="1.5"/>'
    )

    # bars
    for i, (label, mean, err) in enumerate(zip(labels, means, errors)):
        cx = left + bar_space * (i + 0.5)
        x0 = cx - bar_w / 2
        yy = y(mean)
        h = top + plot_h - yy

        out.append(
            f'<rect x="{x0:.1f}" y="{yy:.1f}" '
            f'width="{bar_w:.1f}" height="{h:.1f}" '
            f'fill="#6f8fb3"/>'
        )

        # error bar
        y1 = y(mean + err)
        y2 = y(max(0, mean - err))

        out.append(
            f'<line x1="{cx:.1f}" y1="{y1:.1f}" '
            f'x2="{cx:.1f}" y2="{y2:.1f}" '
            f'stroke="black" stroke-width="2"/>'
        )

        out.append(
            f'<line x1="{cx-8:.1f}" y1="{y1:.1f}" '
            f'x2="{cx+8:.1f}" y2="{y1:.1f}" '
            f'stroke="black" stroke-width="2"/>'
        )

        out.append(
            f'<line x1="{cx-8:.1f}" y1="{y2:.1f}" '
            f'x2="{cx+8:.1f}" y2="{y2:.1f}" '
            f'stroke="black" stroke-width="2"/>'
        )

        out.append(
            f'<text x="{cx:.1f}" y="{y(mean+err)-12:.1f}" '
            f'text-anchor="middle" font-family="sans-serif" '
            f'font-size="15">{mean:.2f}</text>'
        )

        label_lines = label.split("\n")
        base_y = top + plot_h + 25

        for j, line in enumerate(label_lines):
            out.append(
                f'<text x="{cx:.1f}" y="{base_y+j*18:.1f}" '
                f'text-anchor="middle" font-family="sans-serif" '
                f'font-size="14">{html.escape(line)}</text>'
            )

    out.append(
        f'<text x="25" y="{top+plot_h/2}" '
        f'transform="rotate(-90 25 {top+plot_h/2})" '
        f'text-anchor="middle" font-family="sans-serif" '
        f'font-size="16">pp512 throughput (tokens/s)</text>'
    )

    out.append("</svg>")

    path.write_text("\n".join(out) + "\n")


def svg_line_chart(path, title, runs, throughput):
    width = 1000
    height = 620

    left = 90
    right = 40
    top = 70
    bottom = 90

    plot_w = width - left - right
    plot_h = height - top - bottom

    ymin = min(throughput) - 1.0
    ymax = max(throughput) + 1.0
    mean_v = statistics.mean(throughput)

    def x(v):
        if max(runs) == min(runs):
            return left + plot_w / 2
        return left + (v - min(runs)) / (max(runs) - min(runs)) * plot_w

    def y(v):
        return top + plot_h - (v - ymin) / (ymax - ymin) * plot_h

    out = []

    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
    )
    out.append('<rect width="100%" height="100%" fill="white"/>')

    out.append(
        f'<text x="{width/2}" y="35" text-anchor="middle" '
        f'font-family="sans-serif" font-size="24">'
        f'{html.escape(title)}</text>'
    )

    ticks = 6

    for i in range(ticks + 1):
        v = ymin + (ymax - ymin) * i / ticks
        yy = y(v)

        out.append(
            f'<line x1="{left}" y1="{yy:.1f}" '
            f'x2="{width-right}" y2="{yy:.1f}" '
            f'stroke="#dddddd" stroke-width="1"/>'
        )

        out.append(
            f'<text x="{left-12}" y="{yy+5:.1f}" '
            f'text-anchor="end" font-family="sans-serif" '
            f'font-size="14">{v:.1f}</text>'
        )

    points = " ".join(
        f"{x(r):.1f},{y(v):.1f}"
        for r, v in zip(runs, throughput)
    )

    out.append(
        f'<polyline points="{points}" fill="none" '
        f'stroke="#6f8fb3" stroke-width="2"/>'
    )

    for r, v in zip(runs, throughput):
        out.append(
            f'<circle cx="{x(r):.1f}" cy="{y(v):.1f}" '
            f'r="3" fill="#6f8fb3"/>'
        )

    mean_y = y(mean_v)

    out.append(
        f'<line x1="{left}" y1="{mean_y:.1f}" '
        f'x2="{width-right}" y2="{mean_y:.1f}" '
        f'stroke="#555555" stroke-width="1.5" '
        f'stroke-dasharray="8,6"/>'
    )

    out.append(
        f'<text x="{width-right-5}" y="{mean_y-8:.1f}" '
        f'text-anchor="end" font-family="sans-serif" '
        f'font-size="14">mean = {mean_v:.2f} tok/s</text>'
    )

    out.append(
        f'<text x="{width/2}" y="{height-25}" '
        f'text-anchor="middle" font-family="sans-serif" '
        f'font-size="16">Run</text>'
    )

    out.append(
        f'<text x="25" y="{top+plot_h/2}" '
        f'transform="rotate(-90 25 {top+plot_h/2})" '
        f'text-anchor="middle" font-family="sans-serif" '
        f'font-size="16">pp512 throughput (tokens/s)</text>'
    )

    out.append("</svg>")

    path.write_text("\n".join(out) + "\n")


# D300
labels = []
means = []
errors = []

for node in ("lab1", "lab2", "lab3"):
    for kernel in ("107", "111"):
        v = values(node, kernel)

        labels.append(f"{node}\n6.12.{kernel}")
        means.append(statistics.mean(v))
        errors.append(statistics.stdev(v) if len(v) > 1 else 0)

lab4_v = [r["pp512_tps"] for r in lab4_rows]

labels.append("lab4\n6.12.107\nfixed ref")
means.append(statistics.mean(lab4_v))
errors.append(statistics.stdev(lab4_v))

svg_bar_chart(
    FIG / "d300-kernel-comparison.svg",
    "MacPro6,1 FirePro D300: Linux kernel comparison",
    labels,
    means,
    errors,
    ymax=72,
)


# D500
v107 = values("lab5", "107")
v111 = values("lab5", "111")

svg_bar_chart(
    FIG / "d500-kernel-comparison.svg",
    "MacPro6,1 FirePro D500: Linux kernel comparison",
    ["6.12.107", "6.12.111"],
    [statistics.mean(v107), statistics.mean(v111)],
    [
        statistics.stdev(v107),
        statistics.stdev(v111),
    ],
    ymax=48,
)


# Lab4
runs = [r["run"] for r in lab4_rows]
throughput = [r["pp512_tps"] for r in lab4_rows]

svg_line_chart(
    FIG / "lab4-fixed-reference.svg",
    "Lab4 fixed Linux 6.12.107 reference",
    runs,
    throughput,
)


print("Generated:")

for p in sorted(FIG.glob("*.svg")):
    print(" ", p.relative_to(BASE))
