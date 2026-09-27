# Thermal Qualification 試験方法

[English](thermal-qualification.md)

## 概要

このドキュメントでは、MacPro6,1 Local LLM Labで使用する
Mac Pro (Late 2013 / MacPro6,1) ノードの長時間Qualification試験方法を記録します。

目的は、CPU、メモリ、GPUなどのアップグレード前後に、
各ノードの安定性、熱特性、およびハードウェアエラーの有無を
再現可能な方法で評価することです。

個々のノードの測定結果は `results/` 以下に記録し、
このドキュメントでは共通の試験方法を記録します。

## 基本方針

Qualificationでは、単一の最大負荷試験だけではなく、
異なるハードウェア領域に対する複数の長時間負荷試験を連続して実施します。

現在のQualification sequenceは以下です。

| Phase | Duration | Primary target |
|---|---:|---|
| Memory stress | 3 h | System memory / memory subsystem |
| Dual GPU stress | 2 h | Both FirePro GPUs |
| CPU mixed workload | 1 h | CPU |

各フェーズの間には温度状態を確認し、
必要に応じてcooldownを実施します。

## Pre-flight Checks

Qualification開始前に以下を確認します。

- 以前の試験プロセスが残っていないこと
- SMCファン制御状態
- CPUおよびGPU温度センサー
- EDAC状態
- 十分なディスク空き容量
- Qualification用スクリプトの存在
- ファンコントローラの状態

先行する試験が実行中の場合は、その試験が終了してから
Qualificationを開始します。

## Thermal Telemetry

試験中はCPU、2基のGPU、およびメインファンの状態を継続的に記録します。

主な記録項目：

- Timestamp
- Test phase
- CPU temperature
- GPU temperature ×2
- Main fan RPM

現在のQualificationスクリプトでは、通常5秒間隔で
thermal telemetryを記録します。

## Thermal Safety Limits

長時間の無人試験を安全に停止できるよう、
ソフトウェアによるthermal safety limitを設定します。

現在のQualification設定：

| Device | Stop threshold |
|---|---:|
| CPU | 88 °C |
| GPU | 85 °C |

これらは、このプロジェクトで実験上設定している停止閾値です。

AppleがMacPro6,1について規定した公式最大安全温度を
意味するものではありません。

閾値に到達した場合、Qualificationを停止し、
thermal stopとして記録します。

## Fan Control

Qualification中はLinux `applesmc` インターフェースを利用した
カスタムファンコントローラを使用します。

ファン制御はCPUおよびGPU温度を監視し、
温度上昇に応じてMacPro6,1のメインファン回転数を調整します。

現在確認しているメインファンのおおよその範囲：

| State | Fan speed |
|---|---:|
| Minimum | 790 RPM |
| Maximum | 1900 RPM |

ファン制御の詳細については以下を参照してください。

[ファン制御方法](fan-control.ja.md)

## Memory Qualification

メモリ試験には `stress-ng` を使用します。

MP61-N01 S0 Qualificationで使用した試験形式：

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
