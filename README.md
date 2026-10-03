# MacPro6,1 Local LLM Lab

[日本語 README](README.ja.md)

A reproducible experimental project investigating the feasibility of
repurposing Apple Mac Pro (Late 2013 / MacPro6,1) systems for local
and distributed large language model (LLM) inference.

## Project Goals

This project investigates the performance, scalability, power consumption,
cost efficiency, and practical limitations of using repurposed Mac Pro
(Late 2013) systems as LLM inference nodes.

The project will examine both single-node and multi-node configurations.

## Research Areas

- CPU-based LLM inference
- GPU-assisted LLM inference
- Multi-node distributed inference
- Thunderbolt 2 networking
- Ethernet networking
- Memory capacity and bandwidth
- Power consumption
- Thermal behavior
- Deployment cost
- Cost efficiency
- Scaling efficiency

## Experimental Scale

Planned configurations include:

- 1-node baseline
- 2-node experiments
- 4-node cluster
- Up to 7-node experimental cluster

## Hardware Platform

Primary platform:

- Apple Mac Pro (Late 2013)
- Model Identifier: MacPro6,1
- Intel Xeon E5 processors
- ECC DDR3 memory
- AMD FirePro GPUs
- Thunderbolt 2
- Gigabit Ethernet

Individual node configurations will be documented separately because
CPU, memory, GPU, and storage configurations may differ between systems.

## Reproducibility

To improve experimental reproducibility, the following will be documented
and published where possible:

- Hardware configurations
- Software and version information
- OS and kernel versions
- Configuration files
- Benchmark procedures
- Experimental scripts
- Sanitized raw measurement data
- Processed data
- Graphs and figures
- Experimental issues and failed attempts

## Current Progress

### MP61-N01

Baseline measurements and long-duration qualification testing have been
completed on the first experimental node, `MP61-N01`, in its as-acquired
hardware configuration.

| Component | Configuration |
| --------- | ------------------------------------- |
| Model     | Apple Mac Pro (Late 2013 / MacPro6,1) |
| CPU       | Intel Xeon E5-1620 v2 (4C/8T) |
| Memory    | 12 GB DDR3-1866 ECC |
| GPU       | AMD FirePro D300 2 GB ×2 |
| Storage   | Apple 256 GB SSD |
| OS        | Debian 13 |
| Kernel    | Linux 6.12.107+deb13-amd64 |

### Qualification

On 2026-09-27, the following sequence of extended stress tests was completed.

| Test | Duration | Result |
| ------------------ | -------: | ------ |
| Memory stress | 3 h | PASS |
| Dual GPU stress | 2 h | PASS |
| CPU mixed workload | 1 h | PASS |

Across the complete qualification sequence:

- EDAC Correctable Errors: 0
- EDAC Uncorrectable Errors: 0
- Kernel / hardware error log matches: 0
- Thermal safety stops: None
- Final result: PASS

Details:

- [MP61-N01 hardware](docs/hardware/MP61-N01.md)
- [Qualification results](results/MP61-N01/S0-as-acquired/qualification-20260927.md)
- [Thermal qualification methodology](docs/methodology/thermal-qualification.md)
- [Fan control](docs/methodology/fan-control.md)

### Kernel-dependent Vulkan op-offload performance

A completed 36-cycle A/B study found a large and reproducible
kernel-dependent performance difference on MacPro6,1 systems using AMD
GFX6 GPUs with the llama.cpp Vulkan operation-offload pp512 path.

The final 2026-10-03 dataset contains 576 A/B measurements.

| GPU | Linux 6.12.107 | Linux 6.12.111 | 107 / 111 |
|---|---:|---:|---:|
| FirePro D300 / Pitcairn, Lab1-3 aggregate | 63.031 tok/s | 16.448 tok/s | 3.832x |
| FirePro D500 / Tahiti, Lab5 | 39.433 tok/s | 20.049 tok/s | 1.967x |

For Lab1, Lab2, Lab3, and Lab5, each node/kernel combination contains
72 measurements from 36 cycles with two benchmark runs per boot.

A separate D300 system, Lab4, remained fixed on Linux 6.12.107 and
completed 255 successful reference measurements with a mean of
62.431 tok/s and an across-run standard deviation of 0.432 tok/s.

A secondary run-order effect was observed on Lab5 with the D500 under
Linux 6.12.107: run 1 averaged 40.829 tok/s and run 2 averaged
38.036 tok/s, a 7.34% difference. The cause of this secondary effect is
not yet established.

The exact responsible kernel commit or subsystem has not yet been
identified.

- [Investigation report](docs/findings/kernel-vulkan-op-offload-20261003.md)
- [Dataset and aggregate results](results/kernel-ab/20261003/README.md)
- [D300 kernel comparison](figures/kernel-ab/20261003/d300-kernel-comparison.svg)
- [D500 kernel comparison](figures/kernel-ab/20261003/d500-kernel-comparison.svg)
- [Lab4 fixed reference](figures/kernel-ab/20261003/lab4-fixed-reference.svg)

## Planned Repository Structure

The project repository is planned to use the following structure:

```text
docs/
├── hardware/       Hardware inventory and individual node specifications
├── methodology/    Experimental methods and measurement procedures
└── network/        Network and Thunderbolt topology documentation

benchmarks/          Benchmark definitions
data/                Experimental measurement data
results/             Processed benchmark and qualification results
scripts/             Installation, measurement, and automation scripts
figures/             Diagrams, graphs, and figures
paper/               Research papers and technical report material
