# MP61-N01 S0 Qualification Results — 2026-09-27

[日本語版](qualification-20260927.ja.md)

## Overview

Long-duration qualification testing was performed on `MP61-N01`
in its S0 as-acquired configuration.

The purpose of this qualification was to establish a baseline for
system stability and thermal behavior before planned CPU, memory,
and other hardware upgrades.

## System Configuration

| Component | Configuration |
|---|---|
| Node | MP61-N01 |
| Stage | S0 — As Acquired |
| Model | Apple Mac Pro (Late 2013 / MacPro6,1) |
| CPU | Intel Xeon E5-1620 v2 (4C/8T) |
| Memory | 12 GB DDR3-1866 ECC |
| GPU | AMD FirePro D300 2 GB ×2 |
| OS | Debian 13 |
| Kernel | Linux 6.12.107+deb13-amd64 |

## Qualification Sequence

The following sequence of continuous tests was performed on 2026-09-27.

| Phase | Duration | Result |
|---|---:|---|
| Memory stress | 3 h | PASS |
| Dual GPU stress | 2 h | PASS |
| CPU mixed workload | 1 h | PASS |

Overall result:

**PASS**

No thermal safety stop occurred during the qualification sequence.

## Thermal Summary

Number of telemetry samples:

**4,304 samples**

### Peak Values

| Metric | Peak | Phase |
|---|---:|---|
| CPU | 68.0 °C | Dual GPU stress |
| GPU0 | 65.0 °C | Dual GPU stress |
| GPU1 | 65.0 °C | Dual GPU stress |
| Main fan | 1901 RPM | Dual GPU stress |

### Phase Averages

| Phase | Samples | CPU Avg | GPU0 Avg | GPU1 Avg | Fan Avg |
|---|---:|---:|---:|---:|---:|
| Memory stress | 2150 | 49.2 °C | 39.7 °C | 40.6 °C | 1019.3 RPM |
| Dual GPU stress | 1434 | 61.6 °C | 62.5 °C | 63.2 °C | 1842.1 RPM |
| CPU mixed workload | 716 | 53.7 °C | 39.5 °C | 40.5 °C | 1410.5 RPM |

## Reliability

Post-test verification produced the following results:

| Check | Result |
|---|---|
| EDAC Correctable Errors | 0 |
| EDAC Uncorrectable Errors | 0 |
| Kernel / hardware error log matches | 0 |
| Thermal safety stop | None |
| Residual test processes | None |
| Overall qualification | PASS |

## Final Fan / SMC State

After completion of the qualification sequence, the custom fan
controller was stopped and the SMC fan control state was verified
to have returned to automatic mode.

```text
manual=0
output=790
input=789 RPM
