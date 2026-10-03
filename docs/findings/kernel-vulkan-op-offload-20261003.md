# Kernel-dependent Vulkan op-offload performance on MacPro6,1

**Status:** Completed reproducible A/B finding

**Date:** 2026-10-03

## Summary

During LLM benchmarking of multiple Apple Mac Pro (Late 2013 /
MacPro6,1) systems, a large and reproducible performance difference was
observed between Debian Linux kernels 6.12.107-1 and 6.12.111-1 when
using the llama.cpp Vulkan operation-offload pp512 path on AMD GFX6
GPUs.

The completed A/B experiment contains 576 measurements over 36 cycles.

The exact responsible upstream Linux commit or subsystem has not yet
been identified.

## Initial observation

One D300-equipped MacPro6,1 system, later retained as Lab4, produced
approximately 62 tokens/s in the pp512 benchmark while otherwise
similar D300 systems produced approximately 16 tokens/s.

Lab4 was running Linux 6.12.107 while the slower systems were running
Linux 6.12.111.

The Lab4 installation was deliberately left unchanged and was then used
as a fixed reference.

## Benchmark semantics

The diagnostic benchmark uses the following relevant options:

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

An important detail is that `-ngl 0` means zero model layers are
offloaded to the GPU, but Vulkan operation offload remains enabled.

Therefore these measurements must not be described as pure CPU
benchmarks.

When operation offload was disabled with `-nopo 1`, the large
kernel-dependent pp512 difference disappeared. KV offload did not
explain the observed difference.

## Same-machine kernel A/B/A test

A same-machine experiment on Lab2 strongly localized the performance
change to the kernel version.

Observed pp512 performance was approximately:

    Linux 6.12.111 -> 16.46 tok/s
    Linux 6.12.107 -> 62.09 tok/s
    Linux 6.12.111 -> 16.43 tok/s

The hardware, model, and userspace benchmark binary were unchanged.

## Completed 36-cycle A/B experiment

Lab1, Lab2, Lab3, and Lab5 were alternated between Linux 6.12.107 and
6.12.111 for 36 cycles.

Two pp512 benchmark invocations were executed per kernel boot.

This produced:

    36 cycles
    4 tested nodes
    2 kernels
    2 runs per boot
    576 total A/B measurements

Each node/kernel combination therefore contains 72 measurements.

Final per-node aggregates are:

| Node | GPU | Kernel | n | Mean tok/s | Across-run SD |
|---|---|---:|---:|---:|---:|
| Lab1 | D300 / Pitcairn | 6.12.107 | 72 | 63.167 | 0.657 |
| Lab1 | D300 / Pitcairn | 6.12.111 | 72 | 16.454 | 0.043 |
| Lab2 | D300 / Pitcairn | 6.12.107 | 72 | 62.983 | 0.769 |
| Lab2 | D300 / Pitcairn | 6.12.111 | 72 | 16.445 | 0.050 |
| Lab3 | D300 / Pitcairn | 6.12.107 | 72 | 62.942 | 0.735 |
| Lab3 | D300 / Pitcairn | 6.12.111 | 72 | 16.446 | 0.044 |
| Lab5 | D500 / Tahiti | 6.12.107 | 72 | 39.433 | 1.408 |
| Lab5 | D500 / Tahiti | 6.12.111 | 72 | 20.049 | 0.062 |

## D300 / Pitcairn aggregate

Combining Lab1, Lab2, and Lab3 gives:

    Linux 6.12.107 -> 63.031 tok/s
    Linux 6.12.111 -> 16.448 tok/s
    ratio           -> 3.832x

The result reproduced independently across all three D300 nodes.

## D500 / Tahiti result

The D500-equipped Lab5 system also exhibits a kernel-dependent
difference:

    Linux 6.12.107 -> 39.433 tok/s
    Linux 6.12.111 -> 20.049 tok/s
    ratio           -> 1.967x

The magnitude differs substantially from the D300 result. The two GPU
configurations therefore should not be treated as having an identical
effect size.

## D500 run-order effect under Linux 6.12.107

A secondary and highly repeatable run-order effect was observed on Lab5
with the D500 under Linux 6.12.107.

Across 36 cycles:

    run 1 -> 40.829 tok/s
    run 2 -> 38.036 tok/s
    difference -> 2.793 tok/s
    run 1 versus run 2 -> +7.34%

The across-cycle standard deviation was small:

    run 1 -> 0.085 tok/s
    run 2 -> 0.056 tok/s

However, the mean standard deviation reported internally by
`llama-bench` differed sharply:

    run 1 mean reported SD -> 5.725 tok/s
    run 2 mean reported SD -> 0.131 tok/s

This indicates a repeatable state difference between the first and
second benchmark invocation after a 6.12.107 boot on this D500 system.

The current data do not identify the mechanism. Possible explanations
such as GPU power-state, clock-state, driver-state, cache-state, or
Vulkan execution-state transitions remain hypotheses and are not
established by this experiment.

No comparable run-order effect was observed on Lab5 under 6.12.111 or
on the D300 systems.

## Fixed reference

Lab4 was intentionally kept on its existing Linux 6.12.107 environment
without kernel A/B cycling.

It completed 255 successful reference measurements:

    n    -> 255
    mean -> 62.431 tok/s
    SD   -> 0.432 tok/s

The fixed reference did not show a comparable long-duration collapse
toward the approximately 16.45 tok/s level seen on the D300 systems
under Linux 6.12.111.

Lab4 is treated as a fixed reference rather than a pure controlled
kernel comparison because its storage device and OS history differ from
those of the other nodes.

## Checks performed

The investigation has constrained several simpler explanations:

- both GPUs within tested D300 nodes show the same node-level behavior;
- a single defective GPU does not explain the result;
- observed PCIe links were 8.0 GT/s x16 on the compared D300 systems;
- checked primary Vulkan, Mesa, and libdrm runtime components matched;
- checked Pitcairn firmware files matched;
- CPU model, threading configuration, and checked power-policy settings
  did not explain the pp512 difference;
- KV offload did not reproduce the large effect;
- disabling Vulkan operation offload removed the large difference.

These checks do not prove that every possible userspace or hardware
factor is identical.

## What is established

The completed experiments support the following statement:

> A large and reproducible Linux-kernel-dependent performance difference
> exists between Debian kernel 6.12.107-1 and 6.12.111-1 on the tested
> MacPro6,1 systems when exercising the llama.cpp Vulkan
> operation-offload pp512 path on AMD GFX6 GPUs.

The measured effect is approximately 3.832x on the three tested D300
systems and 1.967x on the tested D500 system.

## What is not established

The current data do not establish:

- the exact offending upstream Linux commit;
- that amdgpu alone is responsible;
- the exact upstream release boundary at which the behavior changes;
- whether Debian-specific patches, configuration, or build conditions
  contribute to the observed endpoint difference;
- the mechanism behind the D500 6.12.107 run-order effect;
- whether the same behavior occurs on other GFX6 hardware or other
  Linux distributions.

## Intermediate-kernel builds

Upstream Linux 6.12.108, 6.12.109, and 6.12.110 were successfully built
for follow-up testing.

These custom kernels use a common configuration derived from the Debian
6.12.111 configuration and were built through the same local build
procedure.

They are not identical in provenance to the Debian-packaged 6.12.107
and 6.12.111 endpoint kernels used in the completed A/B experiment.

Therefore, even if testing 6.12.108 through 6.12.110 reveals a sharp
transition, that result alone will not prove that the responsible
boundary is an upstream stable release or identify a specific commit.

A stronger boundary test would compare upstream 6.12.107 through
6.12.111 built with an identical configuration, toolchain, and build
procedure, or compare Debian source packages under consistently matched
conditions.

## Next steps

The next controlled test is to evaluate the already-built upstream
6.12.108, 6.12.109, and 6.12.110 kernels on a single test node before
expanding testing to other nodes.

If a transition is identified, the relevant stable-kernel changes can
then be narrowed further through patch-level testing or selective commit
reversion.

Additional planned work includes Xeon CPU upgrades, memory-capacity and
memory-bandwidth experiments, and Thunderbolt 2 multi-node inference.
