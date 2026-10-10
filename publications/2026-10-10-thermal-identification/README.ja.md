# MacPro6,1 CPU＋dual-GPU持続負荷時のthermal identification

**状態:** thermal identification実験完了

**日付:** 2026-10-10

## 概要

MacPro6,1をLocal LLMノードとして研究する過程で、CPU/GPU温度と
メインファンの応答が独立した運用上の研究課題として浮上した。

先行するLinux kernel A/B benchmarkはVulkan0を固定した比較試験である。
一方、今回のthermal実験ではCPUとVulkan0/Vulkan1の両GPUを意図的に
同時負荷した。

目的はproduction用adaptive fan controllerを設計する前に、
MacPro6,1の温度応答とファン応答を実測することである。

## 実験条件

Debian 13を使用するMacPro6,1上で、

- CPU stress
- Vulkan0 workload
- Vulkan1 workload
- CPU + dual-GPU同時負荷
- Apple SMC telemetry
- メインファンRPM
- CPU/GPU温度

を記録した。

kernelはLinux `6.12.112-labtest`を使用した。

## SMC AUTOでの観測

Lab7ではAUTO phaseの約5分間の実負荷区間でも、
メインファンは約790 RPM付近に留まった。

観測された主な値は、

- CPU最高温度：約75°C
- hottest GPU最高温度：約74°C
- 終端CPU温度勾配：+2.464°C/min
- 終端hottest GPU温度勾配：+1.932°C/min

であった。

終端温度勾配が正であるため、この観測区間終了時には
thermal equilibriumへ到達していなかった。

ただしApple SMC AUTOが常に回転数を上げないという意味ではない。
本プロジェクトの別の高温・長時間試験ではAUTO fanの上昇も確認している。

## 固定RPM試験

1100 / 1300 / 1500 / 1700 / 1900 RPMを試験した。

![Lab7 fixed-RPM temperatures](figures/lab7-fixed-rpm-temperature.svg)

Lab7の1100 RPMでは終端でも、

- CPU：+0.810°C/min
- hottest GPU：+0.712°C/min

の温度上昇が残った。

従って1100 RPMを長時間運用に一般化可能な安全値とは判断しない。

1500～1700 RPM付近は今後のcontroller設計に有力な範囲に見えるが、
production fan curveはまだ確定していない。

## Dynamic試験

以下のsequenceも継続負荷中に試験した。

`1100 -> 1500 -> 1900 -> 1500 -> 1100 -> 1900 RPM`

最終目標は単一固定RPMではなく、温度と温度変化率を利用する
adaptive controllerである。

## 先行研究

本研究に先行するkernel性能研究：

[MacPro6,1のkernel-dependent Vulkan op-offload性能 — 2026-10-03](../../docs/findings/kernel-vulkan-op-offload-20261003.md)

## LLM研究との今後の統合

thermal問題はMacPro6,1をLocal LLMノードとして利用する研究の途中で
発見された。

現段階ではkernel性能研究とthermal研究を異なる研究トラックとして
扱うが、最終的には両者を統合する。

実用的なLocal LLMノードではtokens/sだけではなく、CPUと両GPUの性能を
長時間の熱負荷下でも安全に維持できることが必要である。

今後はLocal LLM throughput、dual-GPU利用、Linux kernel、温度、
fan control、thermal throttling、長時間性能を同一workloadで評価する。

## データ

本報告で使用した処理済みthermal dataは以下に収録する。

`data/`
