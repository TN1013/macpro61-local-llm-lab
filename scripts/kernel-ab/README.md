# Kernel A/B experiment scripts

These scripts were used for the MacPro6,1 Linux kernel performance
comparison performed on 2026-10-03.

## Scripts

- `overnight-kernel-ab.sh`
  - alternates worker nodes between Linux 6.12.107 and 6.12.111
  - waits for reboot completion
  - verifies the running kernel
  - executes the same llama.cpp benchmark on each node
  - stores raw logs and a TSV summary

- `lab4-fixed-reference.sh`
  - repeatedly benchmarks an unchanged Linux 6.12.107 reference node
  - does not modify GRUB or reboot the reference node

- `status-all.sh`
  - displays node, runner, benchmark, and kernel-build status

- `analyze-results.py`
  - converts raw experiment summaries into machine-readable CSV
  - calculates grouped run-level statistics

- `plot-results.py`
  - generates publication-ready SVG figures directly from the CSV data
  - uses only the Python standard library and requires no plotting package

## Local configuration

The published scripts use RFC 5737 TEST-NET addresses by default.

Set the real addresses through environment variables:

```bash
export SSH_USER=user
export LAB1_IP=192.0.2.11
export LAB2_IP=192.0.2.12
export LAB3_IP=192.0.2.13
export LAB4_IP=192.0.2.14
export LAB5_IP=192.0.2.15
```

Do not commit SSH private keys, credentials, public IP addresses, or
machine-specific secrets.

## Important

The A/B runner requires a separately configured, narrowly scoped
passwordless helper for selecting known kernel entries and rebooting.

Do not grant general passwordless sudo access merely to run this test.
