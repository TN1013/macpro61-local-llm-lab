# MacPro6,1 Linux 6.12.110 → 6.12.111 pp512 Regression Boundary

> **日本語で読まれる方へ:**
> 完全な日本語版は [README.ja.md](README.ja.md) にあります。

## 日本語概要

Mac Pro (Late 2013 / MacPro6,1) 5台を使用し、
Linux 6.12.108から6.12.112までを同一のcold-test protocolで比較しました。

FirePro D300搭載4台では、pp512 throughputが
Linux 6.12.108〜6.12.110では約63 tok/sで安定していた一方、
Linux 6.12.111で約16.45 tok/sへ低下し、
Linux 6.12.112でも同じ低性能状態が継続しました。

この結果により、本実験条件におけるpp512 performance regressionの境界を
**Linux 6.12.110 → 6.12.111** の間へ局所化しました。

原因となる正確なkernel commitまたはsubsystemは、まだ特定していません。

詳しくは [README.ja.md](README.ja.md) を参照してください。

---

## English

## Status

Completed controlled boundary study — 2026-10-11.

## Summary

A controlled five-node MacPro6,1 experiment was performed across Linux
6.12.108, 6.12.109, 6.12.110, 6.12.111, and 6.12.112 using the same
cold-test protocol and preserved benchmark identity.

On the four FirePro D300 nodes, Vulkan operation-offload pp512 throughput
remained near 63 tok/s through Linux 6.12.110, then dropped abruptly to
approximately 16.45 tok/s under Linux 6.12.111.

Linux 6.12.112 remained at the same regressed performance level.

Under the controlled conditions of this campaign, the observed pp512
regression boundary is therefore localized between:

**Linux 6.12.110 and Linux 6.12.111.**

The exact responsible upstream kernel commit or subsystem has not yet
been identified.

## Relationship to earlier work

The 2026-10-03 kernel/Vulkan study established a large and reproducible
performance difference between Linux 6.12.107 and 6.12.111.

That earlier publication did not establish the exact intermediate
release boundary.

This 2026-10-11 follow-up publication does not rewrite or replace the
earlier study. It adds a new controlled K108–K112 experiment that narrows
the observed boundary to the transition from 6.12.110 to 6.12.111.

The 2026-10-10 fleet-kernel-qualification and thermal-identification
publications also remain unchanged historical records.

## Test fleet

| Label | CPU | GPU |
| --- | --- | --- |
| Lab1 | Xeon E5-1620 v2 | FirePro D300 ×2 |
| Lab2 | Xeon E5-1620 v2 | FirePro D300 ×2 |
| Lab3 | Xeon E5-1620 v2 | FirePro D300 ×2 |
| Legacy18 | Xeon E5-1620 v2 | FirePro D300 ×2 |
| USB2 | Xeon E5-1650 v2 | FirePro D500 ×2 |

`Legacy18` is the historical fleet node formerly associated with the
old Lab4 identity. It is not the later Lab4/USB1 thermal-test system.

## Kernel series

The controlled campaign tested:

- Linux 6.12.108-labtest
- Linux 6.12.109-labtest
- Linux 6.12.110-labtest
- Linux 6.12.111-labtest
- Linux 6.12.112-labtest

All five kernels completed successfully on all five nodes.

The campaign final result was:

`PASS_ALL_KERNELS`

## Benchmark path

The canonical cold benchmark exercised the llama.cpp Vulkan
operation-offload pp512 path.

Relevant options included:

    -dev Vulkan0 / Vulkan1
    -ngl 0
    -lzm off
    -t 4
    -n 1
    -nopo 0
    -nkvo 1
    -p 512
    -r 5
    -b 512
    -ub 512

`-ngl 0` means that no model layers are offloaded to the GPU, but Vulkan
operation offload remains active. These measurements therefore must not
be described as pure CPU benchmarks.

Both Vulkan devices were measured independently on every node.

## D300 fleet result

Mean pp512 throughput across Lab1, Lab2, Lab3, and Legacy18:

| Kernel | Vulkan0 tok/s | Vulkan1 tok/s |
| --- | ---: | ---: |
| 6.12.108 | 63.2875 | 62.8450 |
| 6.12.109 | 63.1375 | 62.8275 |
| 6.12.110 | 62.9525 | 62.8875 |
| 6.12.111 | 16.4750 | 16.4225 |
| 6.12.112 | 16.4825 | 16.4275 |

The high-performance region is stable across K108, K109, and K110.

The low-performance region is likewise stable across K111 and K112.

## K110 → K111 boundary

For Vulkan0:

    62.9525 → 16.4750 tok/s
    change: -73.829%
    slowdown: 3.821x

For Vulkan1:

    62.8875 → 16.4225 tok/s
    change: -73.886%
    slowdown: 3.829x

This is an abrupt step change rather than a gradual decline across the
tested kernel series.

## Persistence in K112

K111 → K112 changed only:

    Vulkan0: +0.046%
    Vulkan1: +0.030%

The regression therefore persisted in Linux 6.12.112.

## Cross-node reproducibility

The D300 nodes showed strong agreement on the regressed side.

K111:

    Vulkan0: 16.45–16.49 tok/s
    Vulkan1: 16.41–16.43 tok/s

K112:

    Vulkan0: 16.45–16.50 tok/s
    Vulkan1: 16.42–16.44 tok/s

This behavior reproduced independently across four D300-equipped
MacPro6,1 systems.

## D500 observation

USB2, equipped with dual FirePro D500 GPUs, also transitioned to a lower
performance state.

K111:

    Vulkan0: 20.06 tok/s
    Vulkan1: 19.99 tok/s

K112:

    Vulkan0: 20.24 tok/s
    Vulkan1: 20.07 tok/s

The effect magnitude differs from the D300 result and should not be
treated as identical across GPU families.

## Thermal and execution validity

This boundary campaign used the established thermal-safety controls.

Every kernel/node test completed with valid cold benchmark results,
recovery checks, fan-state restoration, controller collection, and
manifest verification.

`PASS_COLD` means that the controlled test protocol completed
successfully and produced valid evidence. It does not mean that the
measured performance was non-regressed.

## What this publication establishes

This experiment establishes that, under the controlled conditions used
here:

1. Linux 6.12.108, 6.12.109, and 6.12.110 form a stable
   high-performance pp512 region on the tested D300 fleet.
2. Linux 6.12.111 introduces an abrupt approximately 74% pp512 throughput
   reduction relative to 6.12.110.
3. Linux 6.12.112 remains in the same regressed performance region.
4. The observed tested-release boundary is therefore localized between
   Linux 6.12.110 and Linux 6.12.111.
5. The boundary reproduces across both Vulkan devices and multiple
   independent MacPro6,1 systems.

## What this publication does not establish

This study does **not** yet establish:

- the exact offending upstream Linux commit;
- the responsible kernel subsystem;
- that `amdgpu` alone is responsible;
- the precise mechanism producing the pp512 slowdown;
- that the same behavior occurs on every GFX6 system or Linux distribution.

Those questions require a separate commit-level narrowing or bisect
study.

## Data

Processed publication data are stored under `data/`:

- `kernel-boundary-results.csv`
- `kernel-boundary-results.json`
- `d300-kernel-summary.json`
- `boundary-deltas.json`
- `boundary-summary.md`

The normalized result dataset contains 50 measurements:

    5 kernels × 5 nodes × 2 Vulkan devices

## Provenance

See [PROVENANCE.md](PROVENANCE.md).

Publication file integrity is recorded in `SHA256SUMS.txt`.

## Next research step

The release-level boundary is now localized.

The logical next study is commit-level narrowing between Linux 6.12.110
and Linux 6.12.111, while preserving the same benchmark identity,
thermal controls, and validation procedure.
