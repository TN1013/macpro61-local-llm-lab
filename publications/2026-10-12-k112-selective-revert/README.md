# MacPro6,1 Linux 6.12.112 Selective-Revert Validation

> **日本語で読まれる方へ:**
> 完全な日本語版は [README.ja.md](README.ja.md) にあります。

## Status

Commit-level bisect and selective-revert validation completed — 2026-10-12.

## Summary

The preceding controlled kernel-boundary study localized a reproducible
MacPro6,1 / FirePro D300 Vulkan pp512 performance regression to the
transition from Linux 6.12.110 to Linux 6.12.111.

A subsequent git bisect isolated the first bad commit as:

`0af7a28c53f1dab35d74f48966da5651dbde7492`

`drm/amd/pm/si: Fix updating clock limits from power states`

Its direct parent:

`16052dbffa6647df6f40a4567a3a423ff53676d8`

remained in the high-performance region.

On Lab1, the direct commit boundary measured approximately:

| Commit | Vulkan0 pp512 | Vulkan1 pp512 | Classification |
| --- | ---: | ---: | --- |
| parent `16052dbf` | 63.18 | 63.07 | GOOD |
| first bad `0af7a28c` | 16.45 | 16.48 | BAD |

To test causality independently of the bisect classification, Linux
6.12.112 was rebuilt with only the identified offending commit selectively
reverted.

The resulting kernel was:

`6.12.112-revert-0af7`

Using the preserved canonical cold benchmark, Lab1 produced:

| Kernel | Vulkan0 pp512 | Vulkan1 pp512 |
| --- | ---: | ---: |
| Linux 6.12.112 D300 fleet mean | 16.4825 | 16.4275 |
| Linux 6.12.112 with selective revert, Lab1 | 63.27 | 62.64 |

The selective-revert kernel therefore returned the D300 system to the
approximately 63 tok/s performance region seen before the regression.

## Relationship to previous publication

This publication is a follow-up to:

[Linux 6.12.110 → 6.12.111 regression boundary](../2026-10-11-kernel-regression-boundary/README.md)

The earlier publication remains unchanged as the historical release-level
boundary result.

That study explicitly did not identify the responsible commit. This
follow-up performs the commit-level narrowing and selective-revert
validation.

## First bad commit

First bad commit:

`0af7a28c53f1dab35d74f48966da5651dbde7492`

Subject:

`drm/amd/pm/si: Fix updating clock limits from power states`

Direct parent:

`16052dbffa6647df6f40a4567a3a423ff53676d8`

The change is in:

`drivers/gpu/drm/amd/pm/legacy-dpm/si_dpm.c`

The commit modifies Southern Islands legacy-DPM clock-limit handling.

## Selective-revert build

Linux 6.12.112 base:

`7aba70ab2e8d8ab3cd45abcaa15e1119a00dc42a`

Local revert commit:

`2ca44dfc8f8bb482311796ab9d295d7219a1874e`

Kernel release:

`6.12.112-revert-0af7`

The generated K112 configuration was byte-identical to the vanilla
6.12.112-labtest configuration.

Config SHA256:

`a4c7bb87dd9c51d02875ec2bc6588d63a021694ce1afef296a1c20cc965009e7`

Kernel image SHA256:

`853b37824e6d3a8df19ec77f6cfc157bae54b4b121eb3ac66d500b8be9b4ca7e`

Revert patch SHA256:

`e34fa6310240be1cd18723fe462d70837f6f9e889e54349f2e07865f6321d07e`

## Benchmark identity

The same canonical operation-offload benchmark identity used in the
release-boundary study was preserved.

llama.cpp commit:

`7ac59a6e3ad851cd41af00f678effab0598ba9a8`

llama-bench SHA256:

`2735454274bb661268ef9ef8c441f932b59ff6fa548b11c4ffd87ca9d0cb6ed1`

Model:

`Qwen3-8B-Q4_K_M.gguf`

Model SHA256:

`d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785`

Relevant options:

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

`-ngl 0` does not make this a pure CPU benchmark. Vulkan operation
offload remains active.

## Result

The selective-revert run completed with:

`PASS_COLD`

Vulkan0:

`63.27 tok/s`

Vulkan1:

`62.64 tok/s`

These values are effectively back in the pre-regression K108-K110
performance region.

For reference, the D300 fleet means were:

| Kernel | Vulkan0 | Vulkan1 |
| --- | ---: | ---: |
| 6.12.110 | 62.9525 | 62.8875 |
| 6.12.112 vanilla | 16.4825 | 16.4275 |

## What this establishes

Under the controlled conditions of this research:

1. The release-level regression begins between Linux 6.12.110 and 6.12.111.
2. Git bisect identifies `0af7a28c53f1` as the first bad commit.
3. Its direct parent remains in the high-performance region.
4. The first-bad commit produces the low-performance region on Lab1.
5. Selectively reverting that commit from Linux 6.12.112 restores
   approximately 63 tok/s pp512 performance.
6. The combined bisect and selective-revert evidence provides strong causal
   evidence that the change introduced by `0af7a28c53f1` is responsible for
   the observed regression on the tested D300 MacPro6,1 system.

## What this does not establish

This result does not yet establish:

- the exact runtime DPM/clock-state mechanism producing the slowdown;
- whether every GFX6/Southern Islands system is affected identically;
- whether the same selective revert restores every FirePro D500 system;
- whether the revert is suitable as a general upstream fix.

The commit changes legacy SI DPM clock-limit handling, but mechanism-level
claims require direct clock/DPM telemetry.

## D500 context and next step

The previous release-level campaign already observed the regressed-side
state on the USB2 FirePro D500 system under K111/K112.

However, the selective-revert kernel has not yet been validated on D500
hardware.

The next cross-GPU validation is therefore to run the exact same
`6.12.112-revert-0af7` kernel binary on:

- USB2 — FirePro D500 x2
- Lab7 — FirePro D500 x2

A separate mechanism study should compare vanilla K112 and selective-revert
K112 DPM/clock telemetry under an identical Vulkan workload.

## Evidence

Small reproducibility and integrity artifacts are preserved in `evidence/`.

Normalized result data are stored in `data/`.

See [PROVENANCE.md](PROVENANCE.md) for hashes and experiment identity.
