# macpro61-local-llm-lab
Reproducible experiments on local and distributed LLM inference using repurposed Apple Mac Pro (Late 2013 / MacPro6,1) systems.

# MacPro6,1 Local LLM Lab

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

Hardware configurations, software versions, benchmark procedures,
scripts, raw measurements, and processed results will be documented
where possible to make experiments reproducible.

## Project Status

**Work in progress**

The hardware platform and experimental methodology are currently
being developed. Results may change as the test environment evolves.

## Planned Repository Structure

```text
hardware/       Hardware inventory and node specifications
benchmarks/     Benchmark definitions and scripts
data/           Experimental measurements
results/        Processed benchmark results
network/        Network and Thunderbolt topology documentation
scripts/        Installation and automation scripts
docs/           Additional documentation
figures/        Diagrams and figures
paper/          Research paper material
