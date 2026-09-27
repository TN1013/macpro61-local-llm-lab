# Thermal Qualification Methodology

[日本語版](thermal-qualification.ja.md)

## Overview

This document describes the long-duration qualification methodology
used for Apple Mac Pro (Late 2013 / MacPro6,1) nodes in the
MacPro6,1 Local LLM Lab.

The objective is to evaluate system stability, thermal behavior, and
the presence of hardware errors using a reproducible procedure before
and after CPU, memory, GPU, and other hardware upgrades.

Individual node measurement results are stored under `results/`.
This document describes the common qualification methodology used
across the project.

## Basic Qualification Strategy

Qualification does not rely on a single maximum-load test.

Instead, multiple long-duration workloads targeting different parts
of the hardware are executed sequentially.

The current qualification sequence is:

| Phase | Duration | Primary target |
|---|---:|---|
| Memory stress | 3 h | System memory / memory subsystem |
| Dual GPU stress | 2 h | Both FirePro GPUs |
| CPU mixed workload | 1 h | CPU |

Thermal conditions are checked between phases, and cooldown is
performed when necessary.

## Pre-flight Checks

Before qualification begins, the following conditions are checked:

- No residual processes from previous tests
- SMC fan-control state
- CPU and GPU temperature sensors
- EDAC state
- Sufficient available disk space
- Presence of qualification scripts
- Fan-controller state

If a preceding experiment is still running, qualification begins only
after that experiment has completed.

## Thermal Telemetry

CPU temperature, both GPU temperatures, and main fan speed are
recorded continuously during qualification.

The primary telemetry fields are:

- Timestamp
- Test phase
- CPU temperature
- GPU temperature ×2
- Main fan RPM

The current qualification implementation normally records thermal
telemetry at 5-second intervals.

## Thermal Safety Limits

Software thermal safety limits are used so that an unattended
long-duration qualification run can be terminated safely.

The current experimental stop thresholds are:

| Device | Stop threshold |
|---|---:|
| CPU | 88 °C |
| GPU | 85 °C |

These values are project-defined experimental stop thresholds.

They must not be interpreted as Apple-specified maximum safe
temperatures for the MacPro6,1.

If a threshold is reached, the qualification run is terminated and
the event is recorded as a thermal stop.

## Fan Control

During qualification, a custom fan controller is used through the
Linux `applesmc` interface.

The controller monitors CPU and GPU temperatures and adjusts the
MacPro6,1 main fan speed according to thermal conditions.

The approximate observed main fan operating range is:

| State | Fan speed |
|---|---:|
| Minimum | 790 RPM |
| Maximum | 1900 RPM |

For details of the fan-control implementation, see:

[Fan Control Methodology](fan-control.md)

## Memory Qualification

Memory qualification uses `stress-ng`.

The test form used for the MP61-N01 S0 qualification was:

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
