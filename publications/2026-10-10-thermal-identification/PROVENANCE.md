# Provenance

## Publication

MacPro6,1 thermal identification under sustained CPU + dual-GPU load

Date: 2026-10-10

## Relationship to previous work

This publication is a follow-up study within the MacPro6,1 Local LLM Lab.

It does not replace or modify the earlier 2026-10-03 Linux kernel /
Vulkan performance study.

Previous work:

- `docs/findings/kernel-vulkan-op-offload-20261003.md`

The earlier kernel study used a fixed Vulkan0 reference benchmark to
investigate kernel-dependent performance behavior.

The present study addresses a different question: thermal response and
fan behavior during sustained simultaneous CPU + dual-GPU workload.

## Historical policy

Published study documents are preserved as historical records.

Later findings should be published as new follow-up studies rather than
silently rewriting earlier reports.

Corrections, reinterpretations, or superseding results should therefore
be recorded in later publications with explicit references to the
earlier work.

## Experimental scope

The thermal study used:

- Apple Mac Pro (Late 2013 / MacPro6,1)
- Debian 13
- Linux 6.12.112-labtest
- CPU stress workload
- Vulkan0 workload
- Vulkan1 workload
- simultaneous CPU + dual-GPU loading
- Apple SMC fan and temperature telemetry

The processed data and analysis script included with this publication
are intended to preserve the evidence used for the reported findings.
