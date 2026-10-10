#!/usr/bin/env python3

import csv
import math
import statistics
from pathlib import Path

HOME = Path.home()
WORK = HOME / "macpro-fleet-bench/thermal-analysis/20261010"

RUNS = {
    "Lab4-new-204":
        WORK / "Lab4-new-204/macpro-lab4-thermal-id-20261010-074717",
    "Lab7-207":
        WORK / "Lab7-207/macpro-lab7-thermal-id-20261010-074720",
}

TEMP_COLS = [
    "cpu_max_mC",
    "gpu0_mC",
    "gpu1_mC",
    "TG0D_mC",
    "TG1D_mC",
    "Te0t_mC",
    "TPCD_mC",
]

IMPORTANT_PHASES = [
    "auto-idle",
    "auto-combined",
    "steady-r1900",
    "steady-r1700",
    "steady-r1500",
    "steady-r1300",
    "steady-r1100",
]

AMBIENT_KEYS = ["TA0P", "TA1P", "TA2P"]

OUT = WORK / "analysis-results"
OUT.mkdir(parents=True, exist_ok=True)


def fnum(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except ValueError:
        return None


def load_telemetry(path):
    rows = []
    with path.open(newline="") as fh:
        for r in csv.DictReader(fh):
            x = dict(r)

            x["mono_s"] = fnum(r["mono_s"])
            x["fan_target"] = fnum(r["fan_target"])
            x["fan_input"] = fnum(r["fan_input"])
            x["fan_output"] = fnum(r["fan_output"])

            try:
                x["load"] = int(r["load"])
            except Exception:
                x["load"] = 0

            for c in TEMP_COLS:
                v = fnum(r[c])
                x[c] = None if v is None else v / 1000.0

            vals = [
                x["gpu0_mC"],
                x["gpu1_mC"],
            ]
            vals = [v for v in vals if v is not None]
            x["gpu_hot_C"] = max(vals) if vals else None

            rows.append(x)

    return rows


def lin_slope_per_min(rows, col, window_s=180):
    """Least-squares slope over final window, in C/min."""
    usable = [
        r for r in rows
        if r["mono_s"] is not None and r.get(col) is not None
    ]

    if len(usable) < 3:
        return None

    end = usable[-1]["mono_s"]
    cut = end - window_s
    usable = [r for r in usable if r["mono_s"] >= cut]

    if len(usable) < 3:
        return None

    xs = [r["mono_s"] for r in usable]
    ys = [r[col] for r in usable]

    xm = statistics.mean(xs)
    ym = statistics.mean(ys)

    den = sum((x - xm) ** 2 for x in xs)
    if den == 0:
        return None

    slope_c_per_s = (
        sum((x - xm) * (y - ym) for x, y in zip(xs, ys))
        / den
    )

    return slope_c_per_s * 60.0


def mean_tail(rows, col, window_s=120):
    usable = [
        r for r in rows
        if r["mono_s"] is not None and r.get(col) is not None
    ]
    if not usable:
        return None

    end = usable[-1]["mono_s"]
    cut = end - window_s
    vals = [
        r[col] for r in usable
        if r["mono_s"] >= cut
    ]

    return statistics.mean(vals) if vals else None


def summarize(rows):
    if not rows:
        return None

    times = [r["mono_s"] for r in rows if r["mono_s"] is not None]
    duration = max(times) - min(times) if len(times) >= 2 else 0.0

    fans = [
        r["fan_input"] for r in rows
        if r["fan_input"] is not None
    ]

    result = {
        "samples": len(rows),
        "duration_s": duration,
        "fan_mean": statistics.mean(fans) if fans else None,
        "fan_min": min(fans) if fans else None,
        "fan_max": max(fans) if fans else None,
    }

    cols = [
        "cpu_max_mC",
        "gpu0_mC",
        "gpu1_mC",
        "gpu_hot_C",
        "TG0D_mC",
        "TG1D_mC",
        "Te0t_mC",
        "TPCD_mC",
    ]

    for col in cols:
        vals = [r[col] for r in rows if r.get(col) is not None]
        result[f"{col}_mean"] = statistics.mean(vals) if vals else None
        result[f"{col}_max"] = max(vals) if vals else None
        result[f"{col}_tail120"] = mean_tail(rows, col, 120)
        result[f"{col}_slope180"] = lin_slope_per_min(rows, col, 180)

    return result


def contiguous_segments(rows):
    """
    Split telemetry whenever phase changes.
    This is essential because dynamic-r1100/r1500/r1900
    each occur twice.
    """
    out = []
    current = []

    for r in rows:
        if not current:
            current = [r]
            continue

        if r["phase"] == current[-1]["phase"]:
            current.append(r)
        else:
            out.append(current)
            current = [r]

    if current:
        out.append(current)

    return out


def fmt(v, nd=2):
    if v is None:
        return ""
    if isinstance(v, int):
        return str(v)
    return f"{v:.{nd}f}"


def write_tsv(path, headers, data):
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(
            fh,
            fieldnames=headers,
            delimiter="\t",
            lineterminator="\n",
        )
        w.writeheader()
        for row in data:
            w.writerow(row)


phase_output = []
segment_output = []
ambient_output = []

for role, run in RUNS.items():
    telem_path = run / "telemetry.csv"
    smc_path = run / "smc-long.csv"

    if not telem_path.exists():
        raise SystemExit(f"missing {telem_path}")

    rows = load_telemetry(telem_path)

    #
    # 1. Main fixed-phase summary
    #
    for phase in IMPORTANT_PHASES:
        subset = [r for r in rows if r["phase"] == phase]

        # auto-combined and steady phases contain preparation/settle rows.
        # Only actual workload rows are used for thermal load analysis.
        if phase == "auto-combined" or phase.startswith("steady-r"):
            subset = [r for r in subset if r["load"] == 1]

        s = summarize(subset)
        if not s:
            continue

        phase_output.append({
            "role": role,
            "phase": phase,
            "samples": s["samples"],
            "duration_s": fmt(s["duration_s"], 1),

            "fan_mean_rpm": fmt(s["fan_mean"], 1),
            "fan_min_rpm": fmt(s["fan_min"], 0),
            "fan_max_rpm": fmt(s["fan_max"], 0),

            "cpu_mean_C": fmt(s["cpu_max_mC_mean"]),
            "cpu_max_C": fmt(s["cpu_max_mC_max"]),
            "cpu_tail120_C": fmt(s["cpu_max_mC_tail120"]),
            "cpu_slope180_C_min": fmt(s["cpu_max_mC_slope180"], 3),

            "gpu0_mean_C": fmt(s["gpu0_mC_mean"]),
            "gpu0_max_C": fmt(s["gpu0_mC_max"]),
            "gpu0_tail120_C": fmt(s["gpu0_mC_tail120"]),
            "gpu0_slope180_C_min": fmt(s["gpu0_mC_slope180"], 3),

            "gpu1_mean_C": fmt(s["gpu1_mC_mean"]),
            "gpu1_max_C": fmt(s["gpu1_mC_max"]),
            "gpu1_tail120_C": fmt(s["gpu1_mC_tail120"]),
            "gpu1_slope180_C_min": fmt(s["gpu1_mC_slope180"], 3),

            "gpu_hot_max_C": fmt(s["gpu_hot_C_max"]),
            "gpu_hot_tail120_C": fmt(s["gpu_hot_C_tail120"]),
            "gpu_hot_slope180_C_min": fmt(
                s["gpu_hot_C_slope180"], 3
            ),

            "TG0D_max_C": fmt(s["TG0D_mC_max"]),
            "TG1D_max_C": fmt(s["TG1D_mC_max"]),
            "Te0t_max_C": fmt(s["Te0t_mC_max"]),
            "TPCD_max_C": fmt(s["TPCD_mC_max"]),
        })

    #
    # 2. Contiguous dynamic segments
    #
    dyn_index = 0

    for seg in contiguous_segments(rows):
        phase = seg[0]["phase"]

        if not phase.startswith("dynamic-r"):
            continue

        seg = [r for r in seg if r["load"] == 1]
        if not seg:
            continue

        dyn_index += 1
        s = summarize(seg)

        segment_output.append({
            "role": role,
            "segment": dyn_index,
            "phase": phase,
            "start_timestamp": seg[0]["timestamp"],
            "end_timestamp": seg[-1]["timestamp"],
            "samples": s["samples"],
            "duration_s": fmt(s["duration_s"], 1),

            "fan_mean_rpm": fmt(s["fan_mean"], 1),

            "cpu_start_C": fmt(seg[0]["cpu_max_mC"]),
            "cpu_end_C": fmt(seg[-1]["cpu_max_mC"]),
            "cpu_max_C": fmt(s["cpu_max_mC_max"]),
            "cpu_slope180_C_min": fmt(
                s["cpu_max_mC_slope180"], 3
            ),

            "gpu0_start_C": fmt(seg[0]["gpu0_mC"]),
            "gpu0_end_C": fmt(seg[-1]["gpu0_mC"]),
            "gpu0_max_C": fmt(s["gpu0_mC_max"]),
            "gpu0_slope180_C_min": fmt(
                s["gpu0_mC_slope180"], 3
            ),

            "gpu1_start_C": fmt(seg[0]["gpu1_mC"]),
            "gpu1_end_C": fmt(seg[-1]["gpu1_mC"]),
            "gpu1_max_C": fmt(s["gpu1_mC_max"]),
            "gpu1_slope180_C_min": fmt(
                s["gpu1_mC_slope180"], 3
            ),

            "gpu_hot_tail120_C": fmt(
                s["gpu_hot_C_tail120"]
            ),
            "gpu_hot_slope180_C_min": fmt(
                s["gpu_hot_C_slope180"], 3
            ),
        })

    #
    # 3. Ambient-ish SMC sensors.
    #    We report raw keys separately; do NOT yet assume any one of
    #    TA0P/TA1P/TA2P is true room ambient.
    #
    if smc_path.exists():
        grouped = {}

        with smc_path.open(newline="") as fh:
            for r in csv.DictReader(fh):
                if r["key"] not in AMBIENT_KEYS:
                    continue

                phase = r["phase"]
                if (
                    phase not in IMPORTANT_PHASES
                    and not phase.startswith("dynamic-r")
                ):
                    continue

                try:
                    temp_c = float(r["temp_mC"]) / 1000.0
                except Exception:
                    continue

                grouped.setdefault(
                    (phase, r["key"]), []
                ).append(temp_c)

        for (phase, key), vals in sorted(grouped.items()):
            ambient_output.append({
                "role": role,
                "phase": phase,
                "key": key,
                "samples": len(vals),
                "mean_C": fmt(statistics.mean(vals)),
                "min_C": fmt(min(vals)),
                "max_C": fmt(max(vals)),
            })


phase_headers = [
    "role", "phase", "samples", "duration_s",
    "fan_mean_rpm", "fan_min_rpm", "fan_max_rpm",

    "cpu_mean_C", "cpu_max_C",
    "cpu_tail120_C", "cpu_slope180_C_min",

    "gpu0_mean_C", "gpu0_max_C",
    "gpu0_tail120_C", "gpu0_slope180_C_min",

    "gpu1_mean_C", "gpu1_max_C",
    "gpu1_tail120_C", "gpu1_slope180_C_min",

    "gpu_hot_max_C", "gpu_hot_tail120_C",
    "gpu_hot_slope180_C_min",

    "TG0D_max_C", "TG1D_max_C",
    "Te0t_max_C", "TPCD_max_C",
]

segment_headers = [
    "role", "segment", "phase",
    "start_timestamp", "end_timestamp",
    "samples", "duration_s", "fan_mean_rpm",

    "cpu_start_C", "cpu_end_C",
    "cpu_max_C", "cpu_slope180_C_min",

    "gpu0_start_C", "gpu0_end_C",
    "gpu0_max_C", "gpu0_slope180_C_min",

    "gpu1_start_C", "gpu1_end_C",
    "gpu1_max_C", "gpu1_slope180_C_min",

    "gpu_hot_tail120_C",
    "gpu_hot_slope180_C_min",
]

ambient_headers = [
    "role", "phase", "key",
    "samples", "mean_C", "min_C", "max_C",
]

write_tsv(
    OUT / "phase-summary.tsv",
    phase_headers,
    phase_output,
)

write_tsv(
    OUT / "dynamic-segments.tsv",
    segment_headers,
    segment_output,
)

write_tsv(
    OUT / "ambient-smc-summary.tsv",
    ambient_headers,
    ambient_output,
)

print(f"OUTPUT={OUT}")
print()
print("===== PHASE SUMMARY =====")

for r in phase_output:
    print(
        f"{r['role']:13s} "
        f"{r['phase']:16s} "
        f"n={r['samples']:>4} "
        f"sec={r['duration_s']:>6} "
        f"fan={r['fan_mean_rpm']:>7} "
        f"CPU max/tail={r['cpu_max_C']:>5}/{r['cpu_tail120_C']:>5} "
        f"slope={r['cpu_slope180_C_min']:>7} "
        f"GPUhot max/tail={r['gpu_hot_max_C']:>5}/{r['gpu_hot_tail120_C']:>5} "
        f"slope={r['gpu_hot_slope180_C_min']:>7}"
    )

print()
print("===== DYNAMIC SEGMENTS =====")

for r in segment_output:
    print(
        f"{r['role']:13s} "
        f"seg={r['segment']} "
        f"{r['phase']:14s} "
        f"sec={r['duration_s']:>6} "
        f"fan={r['fan_mean_rpm']:>7} "
        f"CPU {r['cpu_start_C']:>5}->{r['cpu_end_C']:>5} "
        f"max={r['cpu_max_C']:>5} "
        f"slope={r['cpu_slope180_C_min']:>7} "
        f"GPUtail={r['gpu_hot_tail120_C']:>5} "
        f"slope={r['gpu_hot_slope180_C_min']:>7}"
    )

print()
print("FILES:")
print(OUT / "phase-summary.tsv")
print(OUT / "dynamic-segments.tsv")
print(OUT / "ambient-smc-summary.tsv")
