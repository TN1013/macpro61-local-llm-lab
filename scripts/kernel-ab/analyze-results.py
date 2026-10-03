#!/usr/bin/env python3

from pathlib import Path
import csv
import re
import statistics

BASE = Path(__file__).resolve().parents[2]
DATA = BASE / "data/kernel-ab/20261003"

src = DATA / "summary.raw.tsv"
dst = DATA / "summary.csv"

rows = []

pat = re.compile(
    r"pp512\s*\|\s*([0-9.]+)\s*±\s*([0-9.]+)"
)

with src.open() as f:
    for line in f:
        parts = line.rstrip("\n").split("\t", 5)

        if len(parts) != 6:
            continue

        timestamp, cycle, kernel, run, node, result = parts

        m = pat.search(result)
        if not m:
            continue

        rows.append({
            "timestamp": timestamp,
            "cycle": cycle.split("=", 1)[1],
            "kernel": kernel.split("=", 1)[1],
            "run": run.split("=", 1)[1],
            "node": node,
            "pp512_tps": float(m.group(1)),
            "reported_sd_tps": float(m.group(2)),
        })

with dst.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)

lab4_src = DATA / "lab4-fixed-reference.raw.log"
lab4_dst = DATA / "lab4-fixed-reference.csv"

lab4_rows = []

lab4_pat = re.compile(
    r"\[(.*?)\].*run=(\d+)\s+rc=(\d+).*"
    r"pp512\s*\|\s*([0-9.]+)\s*±\s*([0-9.]+)"
)

with lab4_src.open() as f:
    for line in f:
        m = lab4_pat.search(line)
        if not m:
            continue

        lab4_rows.append({
            "timestamp": m.group(1),
            "run": int(m.group(2)),
            "rc": int(m.group(3)),
            "kernel": "6.12.107",
            "node": "lab4",
            "pp512_tps": float(m.group(4)),
            "reported_sd_tps": float(m.group(5)),
        })

with lab4_dst.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=lab4_rows[0].keys(), lineterminator="\n")
    w.writeheader()
    w.writerows(lab4_rows)

print("A/B measurements:", len(rows))
print("Lab4 measurements:", len(lab4_rows))

print("\nGrouped A/B means:")

groups = {}

for r in rows:
    key = (r["node"], r["kernel"])
    groups.setdefault(key, []).append(r["pp512_tps"])

for key, values in sorted(groups.items()):
    print(
        key[0],
        key[1],
        f"n={len(values)}",
        f"mean={statistics.mean(values):.3f}",
        f"sd={statistics.stdev(values):.3f}" if len(values) > 1 else ""
    )

if lab4_rows:
    vals = [r["pp512_tps"] for r in lab4_rows]
    print(
        "\nlab4 fixed 107:",
        f"n={len(vals)}",
        f"mean={statistics.mean(vals):.3f}",
        f"sd={statistics.stdev(vals):.3f}" if len(vals) > 1 else ""
    )

print("\nGrouped A/B means by run:")

run_groups = {}

for r in rows:
    key = (r["node"], r["kernel"], r["run"])
    run_groups.setdefault(key, []).append(r)

for key, items in sorted(run_groups.items()):
    node, kernel, run = key
    vals = [r["pp512_tps"] for r in items]
    reported_sds = [r["reported_sd_tps"] for r in items]

    print(
        node,
        kernel,
        f"run={run}",
        f"n={len(vals)}",
        f"mean={statistics.mean(vals):.3f}",
        f"run_sd={statistics.stdev(vals):.3f}" if len(vals) > 1 else "",
        f"mean_reported_sd={statistics.mean(reported_sds):.3f}"
    )

# D300 aggregate: lab1, lab2, lab3
d300_nodes = {"lab1", "lab2", "lab3"}

d300_by_kernel = {}

for r in rows:
    if r["node"] in d300_nodes:
        d300_by_kernel.setdefault(r["kernel"], []).append(r["pp512_tps"])

if "107" in d300_by_kernel and "111" in d300_by_kernel:
    d300_107 = statistics.mean(d300_by_kernel["107"])
    d300_111 = statistics.mean(d300_by_kernel["111"])

    print("\nD300 aggregate:")
    print(
        f"107 mean={d300_107:.3f}",
        f"111 mean={d300_111:.3f}",
        f"ratio={d300_107 / d300_111:.3f}x"
    )

# D500 / lab5 aggregate
lab5_by_kernel = {}

for r in rows:
    if r["node"] == "lab5":
        lab5_by_kernel.setdefault(r["kernel"], []).append(r["pp512_tps"])

if "107" in lab5_by_kernel and "111" in lab5_by_kernel:
    lab5_107 = statistics.mean(lab5_by_kernel["107"])
    lab5_111 = statistics.mean(lab5_by_kernel["111"])

    print("\nD500 / lab5 aggregate:")
    print(
        f"107 mean={lab5_107:.3f}",
        f"111 mean={lab5_111:.3f}",
        f"ratio={lab5_107 / lab5_111:.3f}x"
    )

# Lab5 kernel 107 run-order effect
lab5_107_run1 = [
    r["pp512_tps"]
    for r in rows
    if r["node"] == "lab5"
    and r["kernel"] == "107"
    and r["run"] == "1"
]

lab5_107_run2 = [
    r["pp512_tps"]
    for r in rows
    if r["node"] == "lab5"
    and r["kernel"] == "107"
    and r["run"] == "2"
]

if lab5_107_run1 and lab5_107_run2:
    run1_mean = statistics.mean(lab5_107_run1)
    run2_mean = statistics.mean(lab5_107_run2)
    delta = run1_mean - run2_mean
    percent = (run1_mean / run2_mean - 1.0) * 100.0

    print("\nLab5 kernel 107 run-order effect:")
    print(
        f"run1 mean={run1_mean:.3f}",
        f"run2 mean={run2_mean:.3f}",
        f"delta={delta:.3f}",
        f"run1_vs_run2={percent:.2f}%"
    )
