# MP61-N01 S0 Overnight Qualification Data — 2026-09-27

This directory contains the sanitized experimental data from the
MP61-N01 S0 overnight qualification performed on 2026-09-27.

## Qualification Sequence

| Phase | Duration | Result |
|---|---:|---|
| Memory stress | 3 h | PASS |
| Dual GPU stress | 2 h | PASS |
| CPU mixed workload | 1 h | PASS |

Overall qualification result: **PASS**

## Files

- `thermal.csv` — qualification thermal telemetry
- `fan.csv` — fan-controller telemetry
- `fan-console.log` — fan-controller console output
- `memory-3h.log` — memory stress log
- `memory-3h.rc` — memory stress return code
- `gpu-2h.log` — dual-GPU stress log
- `gpu-2h.rc` — GPU stress return code
- `cpu-mixed-1h.log` — CPU mixed-workload log
- `cpu-mixed-1h.rc` — CPU stress return code
- `overnight.log` — qualification orchestration log
- `final-health.txt` — final EDAC and kernel error checks
- `RESULT.txt` — qualification result summary
- `script-sha256.txt` — hashes of scripts used during the experiment
- `SHA256SUMS` — hashes of the sanitized public dataset

## Original Experiment Archive

Original archive:

`MP61-N01-OVERNIGHT-QUAL-001-20260927-003907.tgz`

Original archive SHA-256:

`e352df41230d94a4113259cde59229be6daa5c61987a25047cefbbc4c5a88fa7`

The original archive is retained separately and is not modified.

The files in this public directory are sanitized copies. Therefore,
their hashes are not expected to match files that were modified by
sanitization.

## Sanitization

Environment-specific identifiers were replaced before publication.

Examples:

- Local username/home path → `/home/USER`
- Local hostname → `MP61-N01`

Measurement values, timestamps, workload results, return codes,
temperatures, fan speeds, and other experimental data were not
intentionally modified.

## Telemetry Note

During this qualification run, the two GPU temperature readings were
sorted by temperature before being written to `thermal.csv`.

Therefore, the `gpu0_c` and `gpu1_c` columns do not necessarily
represent stable physical PCI GPU identities.

This limitation does not affect the thermal safety mechanism because
both GPU temperature readings were monitored.

## Related Documentation

- [MP61-N01 Hardware Profile](../../../../docs/hardware/MP61-N01.md)
- [Thermal Qualification Methodology](../../../../docs/methodology/thermal-qualification.md)
- [Fan Control Methodology](../../../../docs/methodology/fan-control.md)
- [MP61-N01 S0 Qualification Results](../../../../results/MP61-N01/S0-as-acquired/qualification-20260927.md)
