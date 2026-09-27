# Fan Control Methodology

[English](fan-control.md)

## 概要

このドキュメントでは、MacPro6,1 Local LLM Labにおいて
Apple Mac Pro (Late 2013 / MacPro6,1) の長時間負荷試験に使用する
カスタムファン制御方法を記録します。

MacPro6,1はCPUと2基のGPUがThermal Coreを共有し、
筐体下部から上部へ空気を流す単一のメインファンによって冷却されます。

本プロジェクトでは、Debian Linux上から `applesmc` インターフェースを利用し、
CPUおよびGPU温度を監視しながらメインファン回転数を制御します。

この制御の目的は、ベンチマークスコアを最大化することではなく、
長時間Qualification試験において再現可能な熱条件を維持し、
過度な温度上昇に対して保守的に対応することです。

## 対象システム

現在のファン制御方法は以下を対象としています。

| Item | Configuration |
|---|---|
| Platform | Apple Mac Pro (Late 2013) |
| Model Identifier | MacPro6,1 |
| Cooling architecture | Shared Thermal Core |
| Main system fan | Single fan |
| Operating system | Debian Linux |
| Kernel interface | `applesmc` |

MP61-N01では、メインファンについて約790 RPMから1900 RPMまでの
動作範囲を確認しています。

この値は本プロジェクトの実機で確認した値であり、
Appleが公称仕様として定義した制御範囲を意味するものではありません。

## Control Objective

カスタムファンコントローラは、CPUおよびGPU温度の上昇に応じて
メインファン回転数を増加させます。

MacPro6,1ではCPUと2基のGPUが冷却系を共有するため、
単一コンポーネントだけではなくシステム全体の熱状態を考慮します。

主な目的は以下です。

- 長時間負荷試験中の温度上昇を抑制する
- 同一条件でのQualificationを再現しやすくする
- 温度上昇時には素早くファン回転数を上げる
- 温度低下時には急激な回転数変動を避ける
- センサー異常時には安全側へ制御する
- 制御終了時にはSMCの自動ファン制御へ復帰する

## Fan Control Curve

現在の制御では、以下の温度とファン回転数を主要な制御点として使用します。

| Temperature | Fan target |
|---:|---:|
| 50 °C | 900 RPM |
| 55 °C | 1230 RPM |
| 60 °C | 1570 RPM |
| 65 °C | 1900 RPM |

確認済みのおおよそのファン動作範囲：

| State | Fan speed |
|---|---:|
| Automatic / idle region | approximately 790 RPM |
| Qualification maximum | approximately 1900 RPM |

これらの値は本プロジェクトで設定した実験用制御値です。

Apple公式のMacPro6,1ファンカーブを再現したものではありません。

## Fast Attack / Slow Release

ファン制御には **fast attack / slow release** の考え方を採用しています。

温度が上昇した場合は、必要なファン回転数へ速やかに移行します。

一方、温度が低下した場合には、ファン回転数を急激に下げず、
一定の安定性を持たせながら徐々に低下させます。

これにより、温度境界付近でファン回転数が頻繁に上下する
huntingを抑制します。

この非対称制御は、安全側への応答を速くしながら、
冷却能力を早すぎるタイミングで低下させないことを目的としています。

## Shared Thermal Core Consideration

MacPro6,1ではCPUと2基のGPUが独立した冷却システムを持つのではなく、
共通のThermal Coreとメインファンを利用します。

そのため、GPU workloadによってCPU温度が上昇する場合や、
CPU workloadによってシステム全体の熱状態が変化する場合があります。

ファン制御では、CPUまたはGPUの一方だけではなく、
利用可能な複数の温度センサーを監視します。

この設計は、特定デバイスの温度だけを最適化するのではなく、
MacPro6,1全体の熱状態を安定させることを目的としています。

## Fail-safe Behavior

温度センサーの取得に失敗した場合や、
正常な制御判断ができない状態を検出した場合は、
安全側へ制御します。

現在のfail-safe動作では、メインファンを最大制御値である
約1900 RPMへ設定します。

```text
FAILSAFE FAN TARGET = 1900 RPM
```

センサー情報が取得できない状態を「低温」と判断して
ファン回転数を下げることはしません。

長時間の無人Qualificationでは、このfail-safe動作を重要な
安全機構として扱います。

## Singleton Protection

複数のファンコントローラが同時にSMCへ異なる回転数を要求すると、
制御状態が不定になる可能性があります。

そのため、ファンコントローラはsingletonとして動作し、
同時に複数のインスタンスが実行されないようにします。

Qualification開始前にも、以前のファン制御プロセスが
残留していないことを確認します。

## Thermal Safety and Fan Control

ファンコントローラとThermal Qualificationの安全停止機構は、
異なる役割を持ちます。

ファンコントローラは温度に応じて冷却能力を調整します。

Thermal Qualification側では別途、実験用の停止閾値を設定します。

| Device | Qualification stop threshold |
|---|---:|
| CPU | 88 °C |
| GPU | 85 °C |

ファンが最大回転数で動作していても温度が上昇し続け、
これらの閾値へ到達した場合は、Qualificationを停止します。

したがって、ファン制御そのものをthermal safety stopの
代替としては使用しません。

詳細については以下を参照してください。

[Thermal Qualification 試験方法](thermal-qualification.ja.md)

## Telemetry

ファン制御中は、可能な限り制御状態をログへ記録します。

記録対象には以下を含みます。

- Timestamp
- CPU temperature
- GPU temperatures
- Requested fan target
- Actual fan RPM
- Control state
- Fail-safe state

Qualificationのthermal telemetryとは別にファン制御ログを保存することで、
温度変化とファン制御の関係を後から解析できるようにします。

## Shutdown and SMC Restoration

カスタムファン制御終了時には、
MacPro6,1のSMCファン制御を自動モードへ復帰させます。

Qualification終了後には少なくとも以下の状態を確認します。

```text
fan1_manual
fan1_output
fan1_input
```

MP61-N01 S0 Qualification終了時には、
自動制御への正常復帰を確認しました。

カスタムファンコントローラが異常終了した場合についても、
可能な限りSMCを安全な状態へ戻すことを設計上の要件とします。

## Controller Version Used for MP61-N01 S0

MP61-N01 S0 Qualificationでは、
カスタムファンコントローラ v0.2 を使用しました。

実験時に使用したv0.2のSHA-256：

```text
e61f6f447c7e86cf9c8386c8aad28f3519c545a382b2c5a7766b402fe3b465c6
```

このSHA-256は実験時のファイルを識別するためのものです。

公開用スクリプトについて環境依存部分の除去やサニタイズを行った場合、
公開版のSHA-256は実験時のファイルとは異なる可能性があります。

その場合は、実験時のバージョンと公開用バージョンを明確に区別します。

## Reproducibility

異なるMacPro6,1ノード間で比較可能なデータを得るため、
可能な限り同じファン制御方法、温度閾値、測定間隔、
負荷試験方法を使用します。

将来ファン制御アルゴリズムを変更した場合は、
バージョン番号と変更内容を記録し、
異なる制御バージョンで得られた結果を区別します。

これにより、CPU交換、メモリ増設、TIM交換などの前後で得られた
thermal dataを比較する際に、ファン制御条件の違いを追跡できます。

## Safety Note

このファン制御方法はMacPro6,1 Local LLM Labにおける
実験用途のために作成したものです。

Apple公式のファン制御アルゴリズムではなく、
Appleが推奨または保証する方法を示すものでもありません。

温度閾値、ファン回転数、および制御アルゴリズムは、
本プロジェクトの実験条件として記録しています。

## Related Documentation

- [Thermal Qualification 試験方法](thermal-qualification.ja.md)
- [MP61-N01 ハードウェアプロファイル](../hardware/MP61-N01.ja.md)
- [MP61-N01 S0 Qualification結果](../../results/MP61-N01/S0-as-acquired/qualification-20260927.ja.md)
