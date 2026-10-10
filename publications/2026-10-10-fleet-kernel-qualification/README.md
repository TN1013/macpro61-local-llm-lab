# MacPro6,1 Fleet Kernel Qualification — K108 to K112

> **日本語で読まれる方へ:**
> 完全な日本語版は [README.ja.md](README.ja.md) にあります。

## 日本語概要

このpublicationは、Mac Pro (Late 2013 / MacPro6,1) 5台を使用して実施した、
Linux kernelおよびLocal LLMの長時間fleet検証結果をまとめたものです。

K108、K109、K110、K112の公式fleet runでは、対象とした5台すべてが
SUCCESSとなりました。

また、K107〜K110におけるpp512 performanceの安定性、
K108/K109の温度最大値、K110で観測した2基のAMD GPU間の温度差、
K111 historical datasetの再検証、
K112における同一artifact setの5台への配備について記録しています。

より詳しい日本語本文は
[README.ja.md](README.ja.md)
を参照してください。

---

## English


## Status

Completed publication record — 2026-10-10.

This publication records previously unpublished fleet-qualification results from the
MacPro6,1 Local LLM Lab during the 2026-10-06 through 2026-10-10 experiment series.

It is intentionally separate from the 2026-10-03 Linux kernel / Vulkan performance
study and the 2026-10-10 thermal identification study. Those earlier publications
remain historical records and are not rewritten here.

## Scope

This publication covers:

- official five-node K108, K109, K110, and K112 long-duration runs;
- cross-kernel pp512 stability observed from K107 through K110;
- the K110 fleet GPU-temperature asymmetry observation;
- archival validation of the historical K111 dataset;
- K112 kernel build provenance and identical-artifact fleet deployment;
- explicit exclusion of the invalid first K109 attempt.

The already released K107↔K111 regression finding is not presented here as a new
discovery. K111 appears here only where needed to document validation and provenance.

## Fleet

| Label | CPU | GPU |
| --- | --- | --- |
| Lab1 | Xeon E5-1620 v2 | FirePro D300 ×2 |
| Lab2 | Xeon E5-1620 v2 | FirePro D300 ×2 |
| Lab3 | Xeon E5-1620 v2 | FirePro D300 ×2 |
| old Lab4 | Xeon E5-1620 v2 | FirePro D300 ×2 |
| USB2 | Xeon E5-1650 v2 | FirePro D500 ×2 |

`old Lab4` is the historical fleet node and is not the later Lab4/USB1 thermal-test system.

## Official fleet runs

| Kernel | Official run | Final archive | Result |
| --- | --- | --- | --- |
| K108 | `k108-to1300-retry-20261006-190829` | `final-20261007-153455` | 5/5 SUCCESS |
| K109 | `k109-to1300-retry-20261007-162623` | `final-20261008-130717` | 5/5 SUCCESS |
| K110 | `k110-to1300-20261008-170221` | `final-20261009-130832` | 5/5 SUCCESS |
| K112 | `k112-to1300-retry-20261009-162051` | `final-20261010-155301` | 5/5 SUCCESS |

Cycle fields are not directly comparable across all runs.

- K108 and K109 use the official reported final-cycle fields.
- K110 reports the highest fully completed cycle before the deadline-truncated cycle.
- K112 uses the verified official final-cycle fields.

See `data/fleet-runs.tsv` and `data/k110-cycle-coverage.tsv`.

K108 and K109 reported zero thermal waits in their official summaries.
For K110, all five nodes have SUCCESS and DEADLINE_REACHED markers, but an explicit
thermal-wait counter was not established from the preserved final archive used here.
K112 likewise does not assert a separate thermal-wait count in this publication.

The K109 official summary identifies two deadline-truncated samples that are excluded
from performance analysis: Lab1 `c79-cpu` and USB2 `c73-nopo1`.

## K107–K110 pp512 stability

Across K107, K108, K109, and K110, all 20 node/kernel sets in the comparison had
zero missing RC0 logs.

GPU pp512 medians remained in a narrow range:

- D300 fleet nodes: approximately **61.95–62.56 tok/s**
- USB2 / D500: approximately **51.47–51.55 tok/s**

This establishes a stable high-performance reference region across K107–K110 for
the tested fleet. It does **not** identify the exact K111 regression boundary.
The 2026-10-03 K107↔K111 A/B publication remains the authoritative report for that
regression, whose responsible kernel commit/subsystem is still unidentified.

## K108 and K109 thermal maxima

### K108

| Node | Te0 max °C | GPU max °C | CPU max °C |
| --- | ---: | ---: | ---: |
| Lab1 | 78.8 | 75 | 79 |
| Lab2 | 74.8 | 73 | 74 |
| Lab3 | 78.5 | 76 | 79 |
| Lab4 | 75.8 | 80 | 82 |
| USB2 | 83.2 | 75 | 76 |

### K109

| Node | Te0 max °C | GPU max °C | CPU max °C |
| --- | ---: | ---: | ---: |
| Lab1 | 79.2 | 66 | 68 |
| Lab2 | 75.0 | 67 | 65 |
| Lab3 | 78.2 | 69 | 69 |
| Lab4 | 76.2 | 73 | 69 |
| USB2 | 85.2 | 70 | 67 |

These are fleet-run telemetry observations, not universal operating limits.

## K110 paired GPU temperature observation

K110 preserved paired temperature snapshots from the two AMD GPU PCI functions
identified in the sensor output as `amdgpu-pci-0200` and `amdgpu-pci-0600`.

Across all available `sensors-cycle-*.txt` snapshots, the mean
`06:00.0 − 02:00.0` temperature difference was positive on every node:

| Node | Paired samples | Mean °C | Median °C | Min °C | Max °C | Positive samples |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Lab1 | 78 | +6.64 | +7.00 | -1.00 | +7.00 | 77/78 |
| Lab2 | 75 | +5.64 | +6.00 | -1.00 | +7.00 | 74/75 |
| Lab3 | 76 | +5.71 | +6.00 | 0.00 | +7.00 | 75/76 |
| Lab4 | 75 | +8.63 | +9.00 | +3.00 | +10.00 | 75/75 |
| USB2 | 70 | +4.57 | +5.00 | 0.00 | +6.00 | 69/70 |

This result is intentionally described by PCI function rather than assuming a
GPU0/GPU1 logical mapping.

It is an observational within-run temperature difference only. It does not establish
a hardware fault, a universal MacPro6,1 physical-side asymmetry, or the cause of the
difference.

## K111 historical dataset validation

The historical source dataset at `kernel-test/results/20261003-011042` was
re-identified and archived without reclassifying it as a five-node formal K111 soak.

Validated structure:

- 288 K111 logs;
- 36 cycles × 2 repeats × 4 labels;
- labels: Lab1, Lab2, Lab3, Lab5;
- kernel: `6.12.111+deb13-amd64`;
- llama.cpp build: `7ac59a6e3 (11207)`;
- combined K107+K111 parser result: 576 rows;
- SSH return code 0 for all 576 rows;
- no missing pp512 or tg1 measurements;
- every 36-cycle × 2-repeat series complete.

Historical archive:

`macpro-fleet-bench/archives/k111-historical-20261003/final-20261010-162130`

Manifest SHA-256:

`a8e3443296bf60b4fb50056f07bb4bfd0eedc9f326b6960c4ec6657007361da7`

The performance conclusion from this dataset was already published in the
2026-10-03 kernel/Vulkan study and is not claimed here as a new finding.

## K112 build and fleet deployment

K112 was built as a reproducible lab artifact, and the same artifact set was installed
across all five formal fleet nodes before the official K112 qualification run.

| Artifact | SHA-256 |
| --- | --- |
| image package | `d7c102f1b6c7e91b7275f9f5be2e18fd4f497e683a7368f1aa77abe1f8de1102` |
| headers package | `f1f3ecf56a1742474c3c7d0243139a3ae8ecec1f022ce6070ef151a08948215f` |
| `vmlinuz` | `8d1d54d22545f8d160fdc8a12f2c4ae5f381fad99b9994376c333d5b1bd42d69` |
| source tar.xz | `164dc9d1f6c93c61a15e1f071c48379b467f2b17c469cce7223471968208ed03` |

Official final archive:

`macpro-fleet-bench/archives/k112-to1300-retry-20261009-162051/final-20261010-155301`

Final archive manifest SHA-256:

`e5b4360df613160f65782b2da4d0593a6511934d9358b62a9840900c51542d9f`

Final node summary:

- Lab1: cycle 42
- Lab2: cycle 41
- Lab3: cycle 42
- old Lab4: cycle 41
- USB2: cycle 48
- 5/5 `SUCCESS=yes`
- 5/5 `DEADLINE_REACHED=yes`
- 5/5 `FAILED=no`
- 5/5 `LAUNCH_FAILED=no`

This establishes a reproducible five-node qualification point for
`6.12.112-labtest`.

## Excluded run

The first K109 attempt, `k109-to1300-20261007-161325`, is explicitly excluded from
the official series. The deadline was supplied as an ISO-formatted string instead of
epoch seconds, causing immediate deadline termination.

It is preserved as an automation error, not treated as a kernel or node failure.

Official K109 result:

`k109-to1300-retry-20261007-162623`

## What this publication establishes

1. K108, K109, K110, and K112 official fleet runs completed successfully on all five
   formal nodes.
2. K107–K110 pp512 medians stayed within a narrow high-performance region on the
   tested D300 and D500 reference nodes.
3. The historical K111 dataset is structurally complete and traceable, but is not a
   five-node formal soak.
4. K112 has preserved artifact hashes and was deployed as the same artifact across
   the five-node fleet before successful qualification.
5. K110 showed a positive mean `06:00.0 − 02:00.0` GPU temperature difference on all five nodes.

## What this publication does not establish

This publication does **not** establish:

- the exact Linux kernel commit that caused the K111 regression;
- that K110's PCI GPU temperature difference is a hardware defect;
- that cycle counts from different official runs are directly comparable as
  throughput measurements;
- a production thermal policy or production fan curve.

## Data files

Processed publication tables are stored in `data/`:

- `fleet-runs.tsv`
- `k108-k109-thermal-maxima.tsv`
- `k110-pci-gpu-temperature-difference.tsv`
- `k110-cycle-coverage.tsv`
- `kernel-throughput-stability.tsv`
- `k111-historical-validation.tsv`
- `k112-artifact-hashes.tsv`

## Related publications

- 2026-10-03 — Kernel-dependent Vulkan operation-offload performance
- 2026-10-10 — Thermal identification under sustained CPU + dual-GPU load

This publication adds the previously unpublished fleet/kernel qualification record
without modifying either earlier study.
