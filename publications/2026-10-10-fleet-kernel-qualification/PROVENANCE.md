# Provenance

## Publication identity

Publication:
`2026-10-10-fleet-kernel-qualification`

Purpose:
preserve previously unpublished MacPro6,1 fleet/kernel qualification results from the
2026-10-06 through 2026-10-10 experiment series.

## Source evidence

### K108

Run:
`k108-to1300-retry-20261006-190829`

Final archive:
`macpro-fleet-bench/archives/k108-to1300-retry-20261006-190829/final-20261007-153455`

Confirmed:
5/5 SUCCESS; thermal waits 0.

### K109

Official retry:
`k109-to1300-retry-20261007-162623`

Final archive:
`macpro-fleet-bench/archives/k109-to1300-retry-20261007-162623/final-20261008-130717`

Confirmed:
5/5 SUCCESS; thermal waits 0.

Excluded first attempt:
`k109-to1300-20261007-161325`

Reason:
deadline argument format error (ISO string instead of epoch seconds), causing immediate
deadline termination.

### K110

Run:
`k110-to1300-20261008-170221`

Final archive:
`macpro-fleet-bench/archives/k110-to1300-20261008-170221/final-20261009-130832`

Confirmed:
5/5 SUCCESS; thermal waits 0.

### K111 historical dataset

Source:
`kernel-test/results/20261003-011042`

Historical archive:
`macpro-fleet-bench/archives/k111-historical-20261003/final-20261010-162130`

Archive manifest SHA-256:
`a8e3443296bf60b4fb50056f07bb4bfd0eedc9f326b6960c4ec6657007361da7`

Classification:
historical archival evidence, not a five-node formal K111 soak.

### K112

Run:
`k112-to1300-retry-20261009-162051`

Final archive:
`macpro-fleet-bench/archives/k112-to1300-retry-20261009-162051/final-20261010-155301`

Archive manifest SHA-256:
`e5b4360df613160f65782b2da4d0593a6511934d9358b62a9840900c51542d9f`

Confirmed:
5/5 SUCCESS, 5/5 DEADLINE_REACHED, 0 FAILED, 0 LAUNCH_FAILED.

## Publication policy

This publication does not modify the 2026-10-03 kernel/Vulkan study or the
2026-10-10 thermal-identification study.

Facts, interpretations, limitations, and excluded runs are recorded separately so
that later work can follow the experiment history without silently rewriting prior
publications.

## Sanitization

Public files omit full private addresses and local absolute home-directory paths.
Only compact node suffixes and repository-relative/archive-relative identifiers are
used where needed for reproducibility.
