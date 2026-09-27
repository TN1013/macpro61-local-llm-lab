# Fan Control Methodology

[日本語版](fan-control.ja.md)

## Overview

This document describes the custom fan-control methodology used for
long-duration workload testing of Apple Mac Pro (Late 2013 / MacPro6,1)
nodes in the MacPro6,1 Local LLM Lab.

The MacPro6,1 uses a shared Thermal Core for the CPU and two GPUs,
with airflow provided by a single main system fan.

This project uses the Linux `applesmc` interface to control the main fan
while monitoring CPU and GPU temperatures under Debian Linux.

The objective is not to maximize benchmark scores, but to maintain
reproducible thermal conditions during long-duration qualification
testing and to respond conservatively to excessive temperature rise.

## Target System

The current fan-control methodology is intended for the following platform:

| Item | Configuration |
|---|---|
| Platform | Apple Mac Pro (Late 2013) |
| Model Identifier | MacPro6,1 |
| Cooling architecture | Shared Thermal Core |
| Main system fan | Single fan |
| Operating system | Debian Linux |
| Kernel interface | `applesmc` |

On MP61-N01, an approximate main fan operating range of
790 RPM to 1900 RPM has been observed.

These values describe behavior observed on the project hardware and
must not be interpreted as an Apple-specified fan-control range.

## Control Objective

The custom fan controller increases main fan speed in response to
rising CPU and GPU temperatures.

Because the CPU and both GPUs share the MacPro6,1 cooling system,
the controller considers the thermal state of the system rather than
optimizing cooling for only one component.

The primary objectives are:

- Limit temperature rise during long-duration workloads
- Improve reproducibility between qualification runs
- Increase cooling rapidly when temperature rises
- Avoid rapid fan-speed reductions when temperature falls
- Fail safely when sensor information becomes unavailable
- Return fan control to the SMC automatic mode after testing

## Fan Control Curve

The current controller uses the following temperature and fan-speed
values as primary control points:

| Temperature | Fan target |
|---:|---:|
| 50 °C | 900 RPM |
| 55 °C | 1230 RPM |
| 60 °C | 1570 RPM |
| 65 °C | 1900 RPM |

Approximate observed fan operating range:

| State | Fan speed |
|---|---:|
| Automatic / idle region | approximately 790 RPM |
| Qualification maximum | approximately 1900 RPM |

These values are experimental control settings defined by this project.

They are not intended to reproduce the original Apple MacPro6,1
fan-control curve.

## Fast Attack / Slow Release

The controller uses a **fast attack / slow release** strategy.

When temperature rises, fan speed is increased rapidly toward the
required cooling level.

When temperature falls, fan speed is reduced more gradually rather
than immediately dropping to a lower target.

This asymmetric response helps reduce fan-speed hunting around
temperature boundaries.

It also provides a conservative thermal response by increasing cooling
quickly while avoiding premature reduction of cooling capacity.

## Shared Thermal Core Consideration

The CPU and both GPUs in the MacPro6,1 do not use completely independent
cooling systems.

They share the Thermal Core and the single main system fan.

As a result, GPU workloads can influence CPU temperature, while CPU
workloads can alter the overall thermal state of the system.

The controller therefore monitors multiple available temperature
sensors rather than relying on a single component temperature.

The objective is to stabilize the thermal state of the complete
MacPro6,1 system.

## Fail-safe Behavior

If temperature sensor acquisition fails or the controller cannot make
a valid thermal-control decision, the system fails toward increased
cooling.

The current fail-safe behavior sets the main fan to the maximum
qualification control value of approximately 1900 RPM.

```text
FAILSAFE FAN TARGET = 1900 RPM
```

Missing sensor data must not be interpreted as a low-temperature
condition that would reduce fan speed.

This fail-safe behavior is particularly important during unattended
long-duration qualification runs.

## Singleton Protection

Multiple fan-controller processes issuing different SMC fan targets
could result in an undefined or unstable control state.

The controller therefore operates as a singleton and prevents multiple
controller instances from running simultaneously.

Pre-flight checks also verify that no previous fan-control process
remains active before a new qualification run begins.

## Thermal Safety and Fan Control

Fan control and qualification thermal safety have separate functions.

The fan controller adjusts cooling capacity in response to temperature.

The Thermal Qualification system independently applies experimental
stop thresholds:

| Device | Qualification stop threshold |
|---|---:|
| CPU | 88 °C |
| GPU | 85 °C |

If temperature continues to rise while the fan is already operating at
maximum qualification speed and one of these thresholds is reached,
the qualification workload is terminated.

Fan control is therefore not used as a substitute for the independent
thermal safety-stop mechanism.

See:

[Thermal Qualification Methodology](thermal-qualification.md)

## Telemetry

Where possible, fan-control state is recorded during operation.

Recorded information includes:

- Timestamp
- CPU temperature
- GPU temperatures
- Requested fan target
- Actual fan RPM
- Control state
- Fail-safe state

Keeping fan-control telemetry in addition to qualification thermal
telemetry allows the relationship between temperature changes and
cooling response to be analyzed after the experiment.

## Shutdown and SMC Restoration

When custom fan control terminates, fan control is returned to the
MacPro6,1 SMC automatic mode.

At minimum, the following states are checked after qualification:

```text
fan1_manual
fan1_output
fan1_input
```

Successful restoration to automatic SMC fan control was verified after
the MP61-N01 S0 qualification.

The controller is also designed to return the SMC to a safe state
whenever possible if the custom controller terminates unexpectedly.

## Controller Version Used for MP61-N01 S0

MP61-N01 S0 qualification used custom fan controller version 0.2.

SHA-256 of the controller file used for the experiment:

```text
e61f6f447c7e86cf9c8386c8aad28f3519c545a382b2c5a7766b402fe3b465c6
```

This SHA-256 identifies the file used during the experiment.

If a public version of the script is sanitized or modified to remove
environment-specific information, its SHA-256 may differ from the
experimental version.

In that case, the experimental and public versions will be identified
separately.

## Reproducibility

To make results comparable between MacPro6,1 nodes, the project uses
the same fan-control methodology, thermal thresholds, telemetry
intervals, and workload procedures wherever possible.

If the fan-control algorithm is changed in the future, the controller
version and relevant changes will be recorded.

This makes it possible to identify differences in fan-control conditions
when comparing thermal measurements before and after CPU replacement,
memory upgrades, TIM replacement, or other hardware changes.

## Safety Note

This fan-control methodology was developed for experimental use in the
MacPro6,1 Local LLM Lab.

It is not Apple's official fan-control algorithm and does not represent
a method recommended or guaranteed by Apple.

Temperature thresholds, fan-speed targets, and control behavior are
documented as experimental conditions of this project.

## Related Documentation

- [Thermal Qualification Methodology](thermal-qualification.md)
- [MP61-N01 Hardware Profile](../hardware/MP61-N01.md)
- [MP61-N01 S0 Qualification Results](../../results/MP61-N01/S0-as-acquired/qualification-20260927.md)
