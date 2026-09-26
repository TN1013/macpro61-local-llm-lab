# MP61-N01 S0 Qualification結果 — 2026-09-27

[English](qualification-20260927.md)

## 概要

`MP61-N01` のS0購入時構成について、
長時間Qualification試験を実施しました。

この試験の目的は、今後予定しているCPU・メモリ等の
アップグレードを行う前に、購入時状態での安定性および
熱特性のベースラインを記録することです。

## システム構成

| Component | Configuration |
|---|---|
| Node | MP61-N01 |
| Stage | S0 — As Acquired |
| Model | Apple Mac Pro (Late 2013 / MacPro6,1) |
| CPU | Intel Xeon E5-1620 v2 (4C/8T) |
| Memory | 12 GB DDR3-1866 ECC |
| GPU | AMD FirePro D300 2 GB ×2 |
| OS | Debian 13 |
| Kernel | Linux 6.12.107+deb13-amd64 |

## Qualification Sequence

2026-09-27に以下の連続試験を実施しました。

| Phase | Duration | Result |
|---|---:|---|
| Memory stress | 3 h | PASS |
| Dual GPU stress | 2 h | PASS |
| CPU mixed workload | 1 h | PASS |

総合結果：

**PASS**

Thermal safety stopは発生しませんでした。

## Thermal Summary

測定サンプル数：

**4304 samples**

### Peak Values

| Metric | Peak | Phase |
|---|---:|---|
| CPU | 68.0 °C | Dual GPU stress |
| GPU0 | 65.0 °C | Dual GPU stress |
| GPU1 | 65.0 °C | Dual GPU stress |
| Main fan | 1901 RPM | Dual GPU stress |

### Phase Averages

| Phase | Samples | CPU Avg | GPU0 Avg | GPU1 Avg | Fan Avg |
|---|---:|---:|---:|---:|---:|
| Memory stress | 2150 | 49.2 °C | 39.7 °C | 40.6 °C | 1019.3 RPM |
| Dual GPU stress | 1434 | 61.6 °C | 62.5 °C | 63.2 °C | 1842.1 RPM |
| CPU mixed workload | 716 | 53.7 °C | 39.5 °C | 40.5 °C | 1410.5 RPM |

## Reliability

試験終了時の確認結果：

| Check | Result |
|---|---|
| EDAC Correctable Errors | 0 |
| EDAC Uncorrectable Errors | 0 |
| Kernel / hardware error log matches | 0 |
| Thermal safety stop | None |
| Residual test processes | None |
| Overall qualification | PASS |

## Final Fan / SMC State

Qualification終了後、カスタムファン制御を終了し、
SMC制御が自動モードへ復帰していることを確認しました。

```text
manual=0
output=790
input=789 RPM
