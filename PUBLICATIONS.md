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

Publication:

- [English](publications/2026-10-10-thermal-identification/README.md)
- [日本語](publications/2026-10-10-thermal-identification/README.ja.md)

Data and reproducibility material are included in the publication
directory.

The kernel-performance and thermal-control studies currently remain
separate research tracks. Future work is expected to combine LLM
throughput, dual-GPU utilization, kernel behavior, thermal behavior,
and adaptive fan control under the same sustained workload.

---

## Publication policy

Future research will be added as new dated publications.

Earlier publications will normally remain unchanged so that the
development of the project, experimental methods, interpretations, and
later corrections can be followed historically.

If an earlier conclusion later requires correction or reinterpretation,
that change should be documented in a new follow-up publication with an
explicit reference to the earlier report.
