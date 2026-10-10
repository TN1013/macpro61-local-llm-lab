# MacPro6,1 Local LLM Lab — Publications and Research History

This file is an append-only index of research publications produced by
the MacPro6,1 Local LLM Lab.

Published research documents are preserved as historical records.
Later work is added as new publications rather than silently replacing
earlier findings.

## 2026-10-03 — Linux kernel / Vulkan performance study

**Kernel-dependent Vulkan op-offload performance on MacPro6,1**

A reproducible A/B study comparing Linux 6.12.107 and 6.12.111 on
MacPro6,1 systems.

Highlights:

- 36 A/B cycles
- 576 measurements
- Vulkan operation-offload pp512 path
- large kernel-dependent performance difference
- exact responsible kernel change not yet identified

Publication:

- [Kernel-dependent Vulkan op-offload performance](docs/findings/kernel-vulkan-op-offload-20261003.md)

This remains the historical report of that experiment and is not
superseded by the thermal study below.

---

## 2026-10-10 — Thermal identification study

**MacPro6,1 thermal identification under sustained CPU + dual-GPU load**

A follow-up study investigating thermal behavior, Apple SMC automatic
fan response, fixed fan speeds, and dynamic fan-speed changes under
simultaneous CPU + dual-GPU workload.

- [English](publications/2026-10-10-thermal-identification/README.md)
- [日本語](publications/2026-10-10-thermal-identification/README.ja.md)

Data and reproducibility material are included in the publication
directory.

The kernel-performance and thermal-control studies currently remain
separate research tracks. Future work is expected to combine LLM
throughput, dual-GPU utilization, kernel behavior, thermal behavior,
and adaptive fan control under the same sustained workload.

---

## 2026-10-10 — Fleet kernel qualification study

**MacPro6,1 fleet kernel qualification — K108 to K112**

A follow-up publication preserving the previously unpublished five-node fleet/kernel
qualification work from 2026-10-06 through 2026-10-10.

Highlights:

- K108 / K109 / K110 / K112 official fleet runs: 5/5 SUCCESS
- stable K107–K110 pp512 reference region on D300 and D500 nodes
- K110 PCI GPU temperature-asymmetry observation
- K111 historical-dataset validation and archival provenance
- identical K112 artifact deployment with preserved SHA-256 hashes
- invalid first K109 attempt explicitly excluded as an automation error

### 日本語概要

2026年10月6日から10月10日にかけて実施した、
Mac Pro (Late 2013 / MacPro6,1) 5台による
Linux kernelおよびLocal LLMの長時間fleet検証をまとめたpublicationです。

主な内容は以下の通りです。

- K108 / K109 / K110 / K112の公式fleet runは5台すべてSUCCESS
- K107〜K110ではpp512 performanceが安定
- K108 / K109の温度最大値を記録
- K110では2基のAMD GPU間の温度差を観測
- K111 historical datasetを再検証
- K112では同一artifact setを5台へ配備してqualificationを実施

日本語の詳細本文は、以下を参照してください。

- [日本語版](publications/2026-10-10-fleet-kernel-qualification/README.ja.md)

This publication adds the previously unpublished fleet/kernel qualification record
without modifying the earlier kernel/Vulkan or thermal-identification studies.

---

## Publication policy

Future research will be added as new dated publications.

Earlier publications will normally remain unchanged so that the
development of the project, experimental methods, interpretations, and
later corrections can be followed historically.

If an earlier conclusion later requires correction or reinterpretation,
that change should be documented in a new follow-up publication with an
explicit reference to the earlier report.
