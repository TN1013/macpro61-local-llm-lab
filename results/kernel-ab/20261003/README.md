# Linux 6.12.107 vs 6.12.111 Vulkan op-offload experiment

**Status:** Completed dataset

**Date:** 2026-10-03

## Experiment summary

A 36-cycle unattended A/B experiment was completed on four MacPro6,1
systems to compare Debian Linux 6.12.107-1 and 6.12.111-1 while running
the llama.cpp Vulkan operation-offload pp512 benchmark.

Each cycle tested:

    Linux 6.12.107
      run 1
      run 2

    Linux 6.12.111
      run 1
      run 2

on four nodes:

    Lab1 - FirePro D300 / Pitcairn
    Lab2 - FirePro D300 / Pitcairn
    Lab3 - FirePro D300 / Pitcairn
    Lab5 - FirePro D500 / Tahiti

The completed A/B dataset contains:

    36 cycles
    4 nodes
    2 kernels
    2 runs per kernel boot
    576 measurements total

Each node/kernel combination therefore contains 72 measurements.

A fifth D300 system, Lab4, remained fixed on Linux 6.12.107 and was
measured independently as a long-duration reference.

## Benchmark environment

Model:

- `Qwen3-8B-Q4_K_M.gguf`
- llama.cpp build `7ac59a6e3 (11207)`

Relevant benchmark options:

    -dev Vulkan0
    -ngl 0
    -nopo 0
    -nkvo 1
    -lzm off
    -t 4
    -p 512
    -n 1
    -r 10
    -b 512
    -ub 512

`-ngl 0` disables model-layer GPU offload, but does not disable Vulkan
operation offload. Operation offload remains enabled unless explicitly
disabled with `-nopo 1`.

Therefore this benchmark must not be described as a pure CPU benchmark.

## Final run-level aggregate

| Node | GPU | Kernel | n | pp512 mean (tok/s) | Across-run SD |
|---|---|---|---:|---:|---:|
| Lab1 | FirePro D300 / Pitcairn | 6.12.107 | 72 | 63.167 | 0.657 |
| Lab1 | FirePro D300 / Pitcairn | 6.12.111 | 72 | 16.454 | 0.043 |
| Lab2 | FirePro D300 / Pitcairn | 6.12.107 | 72 | 62.983 | 0.769 |
| Lab2 | FirePro D300 / Pitcairn | 6.12.111 | 72 | 16.445 | 0.050 |
| Lab3 | FirePro D300 / Pitcairn | 6.12.107 | 72 | 62.942 | 0.735 |
| Lab3 | FirePro D300 / Pitcairn | 6.12.111 | 72 | 16.446 | 0.044 |
| Lab5 | FirePro D500 / Tahiti | 6.12.107 | 72 | 39.433 | 1.408 |
| Lab5 | FirePro D500 / Tahiti | 6.12.111 | 72 | 20.049 | 0.062 |

`Across-run SD` is the standard deviation across the run-level
`pp512_tps` measurements. It is distinct from the standard deviation
reported internally by each individual `llama-bench` invocation.

## D300 aggregate

Combining Lab1, Lab2, and Lab3:

    Linux 6.12.107 -> 63.031 tok/s
    Linux 6.12.111 -> 16.448 tok/s
    ratio           -> 3.832x

The large performance difference reproduced independently across all
three D300 systems.

## D500 aggregate

For Lab5:

    Linux 6.12.107 -> 39.433 tok/s
    Linux 6.12.111 -> 20.049 tok/s
    ratio           -> 1.967x

The effect size differs substantially from the D300 result.

## Lab5 / D500 run-order effect

A secondary repeatable effect was observed on Lab5 under Linux
6.12.107.

Across 36 cycles:

| Kernel | Run | n | Mean tok/s | Across-cycle SD | Mean llama-bench reported SD |
|---|---:|---:|---:|---:|---:|
| 6.12.107 | 1 | 36 | 40.829 | 0.085 | 5.725 |
| 6.12.107 | 2 | 36 | 38.036 | 0.056 | 0.131 |
| 6.12.111 | 1 | 36 | 20.053 | 0.066 | 0.171 |
| 6.12.111 | 2 | 36 | 20.044 | 0.059 | 0.177 |

Under 6.12.107, run 1 averaged 2.793 tok/s more than run 2, corresponding
to a 7.34% difference relative to run 2.

The first invocation also showed a much larger mean internally reported
standard deviation.

The cause of this run-order effect has not been established. Possible
power-state, clock-state, driver-state, cache-state, or Vulkan
execution-state explanations remain hypotheses.

No comparable run-order effect was observed on Lab5 under 6.12.111 or
on the tested D300 systems.

## Fixed reference

Lab4 remained on its existing Linux 6.12.107 environment and did not
participate in kernel cycling.

It completed 255 successful reference measurements:

| Node | GPU | Kernel | n | pp512 mean (tok/s) | Across-run SD |
|---|---|---|---:|---:|---:|
| Lab4 | FirePro D300 / Pitcairn | 6.12.107 | 255 | 62.431 | 0.432 |

Lab4 remained near the approximately 62 tok/s range throughout the
long-duration experiment and did not show a collapse toward the
approximately 16.45 tok/s level observed on D300 systems under
Linux 6.12.111.

Lab4 is a fixed reference rather than a pure controlled kernel
comparison because its storage device and OS history differ from those
of the A/B nodes.

## Interpretation

The completed experiment demonstrates a large and reproducible
kernel-dependent performance difference in this specific llama.cpp
Vulkan operation-offload pp512 benchmark.

The completed measurements support the endpoint comparison:

    D300 / Pitcairn:
      6.12.107 / 6.12.111 = 3.832x

    D500 / Tahiti:
      6.12.107 / 6.12.111 = 1.967x

The exact responsible kernel commit or subsystem has not been
identified.

The current results should not be described as proving an amdgpu
regression or identifying a specific upstream Linux change.

## Intermediate kernel builds

Upstream Linux 6.12.108, 6.12.109, and 6.12.110 were successfully built
for follow-up testing.

These custom kernels use a common configuration derived from the Debian
6.12.111 configuration and the same local build procedure.

Their provenance is therefore not identical to the Debian-packaged
6.12.107 and 6.12.111 endpoint kernels used for this completed A/B
dataset.

A performance transition observed with the custom 6.12.108-6.12.110
kernels may narrow the investigation window, but by itself would not
prove an exact upstream release or commit boundary.

A stronger boundary experiment would build upstream 6.12.107 through
6.12.111 with the same configuration, toolchain, and build procedure,
or use consistently matched Debian source packages.

## Data files

- `summary.raw.tsv` — raw 576-measurement summary produced by the
  unattended A/B runner
- `summary.csv` — machine-readable converted A/B dataset
- `lab4-fixed-reference.raw.log` — complete fixed-reference runner output
- `lab4-fixed-reference.csv` — machine-readable Lab4 dataset

## Reproduction and analysis

The raw files are converted and summarized with:

    python3 scripts/kernel-ab/analyze-results.py

Figures are generated with:

    python3 scripts/kernel-ab/plot-results.py

Related investigation report:

- `docs/findings/kernel-vulkan-op-offload-20261003.md`
- `docs/findings/kernel-vulkan-op-offload-20261003.ja.md`
