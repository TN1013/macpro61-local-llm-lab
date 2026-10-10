# Weekly Research Synthesis — 2026-10-10

This document connects the three research tracks that were active during the week.

## 1. Kernel / Vulkan performance

The previously published 2026-10-03 A/B study established a large, reproducible
kernel-dependent difference in the llama.cpp Vulkan operation-offload pp512 path
between Linux 6.12.107 and 6.12.111 on MacPro6,1.

That report remains unchanged.

During this week, the historical K111 dataset was revalidated and archived with
complete provenance. The validation confirmed 288 K111 logs and 576 combined
K107+K111 rows, with no missing pp512/tg1 measurements.

## 2. Fleet kernel qualification

The official K108, K109, K110, and K112 fleet runs all completed successfully on
five nodes.

K107–K110 pp512 medians remained in a narrow high-performance region on the tested
D300 and D500 reference nodes. K112 added preserved build hashes and same-artifact
deployment across all five nodes.

This fleet series provides the reproducibility and long-duration qualification
context that was not previously represented by a standalone publication.

## 3. Thermal / SMC / fan control

The separate 2026-10-10 thermal-identification publication investigated sustained
CPU + dual-GPU thermal behavior, Apple SMC AUTO response, fixed fan speeds, and
dynamic fan-speed changes.

That work remains a separate historical publication.

## Combined interpretation

The week established three complementary facts:

- performance can change sharply with kernel behavior;
- fleet-level reproducibility requires identical artifacts and long-duration
  multi-node qualification;
- sustained Local LLM work also requires explicit thermal characterization.

The next research stage should combine these tracks under the same controlled Local
LLM workload, measuring throughput, both GPUs, kernel version, fan response,
temperature, and sustained stability together.

No current publication claims to have identified the exact K111 regression commit,
a production fan curve, or a universal cause for the observed PCI GPU temperature asymmetry.
