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
