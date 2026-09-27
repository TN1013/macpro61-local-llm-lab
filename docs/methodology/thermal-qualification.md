
## 英語版 `thermal-qualification.md`

英語版も現在の内容をすべて削除して、対応する内容にします。

```markdown
# Thermal Qualification Methodology

[日本語版](thermal-qualification.ja.md)

## Overview

This document describes the long-duration qualification methodology
used for Apple Mac Pro (Late 2013 / MacPro6,1) nodes in the
MacPro6,1 Local LLM Lab.

The objective is to evaluate system stability, thermal behavior, and
hardware errors using a reproducible procedure before and after CPU,
memory, GPU, and other hardware changes.

Individual experimental results are stored under `results/`.
This document describes the common methodology.

## Qualification Sequence

The current qualification sequence uses multiple long-duration
workloads targeting different parts of the system.

| Phase | Duration | Primary target |
|---|---:|---|
| Memory stress | 3 h | System memory / memory subsystem |
| Dual GPU stress | 2 h | Both FirePro GPUs |
| CPU mixed workload | 1 h | CPU |

Thermal conditions are checked between phases and cooldown is
performed when necessary.

## Pre-flight Checks

Before qualification, the system is checked for residual test
processes, SMC fan-control state, CPU and GPU temperature sensors,
EDAC state, available storage, qualification scripts, and fan
controller state.

If a preceding experiment is still running, qualification waits until
that experiment has completed.

## Thermal Telemetry

CPU temperature, both GPU temperatures, and main fan speed are
recorded continuously during qualification.

The primary telemetry fields are:

- Timestamp
- Test phase
- CPU temperature
- Two GPU temperature readings
- Main fan RPM

The current qualification implementation normally records thermal
telemetry at 5-second intervals.

## Thermal Safety Limits

Software thermal limits are used so that an unattended qualification
run can be terminated safely.

Current experimental stop thresholds:

| Device | Stop threshold |
|---|---:|
| CPU | 88 °C |
| GPU | 85 °C |

These values are project-defined experimental stop thresholds.

They must not be interpreted as Apple-specified maximum safe
temperatures for the MacPro6,1.

Reaching a threshold terminates the qualification and is recorded as
a thermal stop.

## Fan Control

Qualification uses a custom fan controller through the Linux
`applesmc` interface.

The controller monitors CPU and GPU temperatures and adjusts the
single main MacPro6,1 system fan accordingly.

Observed approximate fan range:

| State | Fan speed |
|---|---:|
| Minimum | 790 RPM |
| Maximum | 1900 RPM |

See:

[Fan Control Methodology](fan-control.md)

## Memory Qualification

Memory qualification uses `stress-ng`.

The form used for the MP61-N01 S0 qualification was:

```bash
stress-ng \
  --vm 2 \
  --vm-bytes 70% \
  --vm-method all \
  --verify \
  --metrics \
  --vmstat 60 \
  --thermalstat 60 \
  --timestamp \
  --timeout 3h
