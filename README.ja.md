# MacPro6,1 Local LLM Lab

[English README](README.md)

## 概要

本プロジェクトでは、Apple Mac Pro (Late 2013 / MacPro6,1) を
Local LLMおよび分散LLM推論用の計算ノードとして再利用する
可能性について実験・検証します。

## 研究目的

中古市場で比較的安価に入手できる旧世代ワークステーションを
LLM推論基盤として再利用した場合について、以下を検証します。

- LLM推論性能
- CPUによる推論
- GPUを利用した推論
- 複数ノードによる分散推論
- Thunderbolt 2ネットワーク
- Ethernetネットワーク
- メモリ容量と帯域
- 消費電力
- 熱特性
- 導入費用
- コスト効率
- スケーリング効率

## 実験規模

以下の構成を段階的に検証する予定です。

- 1ノード：基準性能測定
- 2ノード：初期分散実験
- 4ノード：クラスタ実験
- 最大7ノード：分散LLM実験

## ハードウェア

主な実験対象：

- Apple Mac Pro (Late 2013)
- Model Identifier: MacPro6,1
- Intel Xeon E5
- ECC DDR3メモリ
- AMD FirePro GPU
- Thunderbolt 2
- Gigabit Ethernet

各Mac ProはCPU、メモリ、GPU、ストレージ等の構成が異なるため、
個体ごとの構成を別途記録します。

## 再現性

実験の再現性を確保するため、可能な範囲で以下を公開します。

- ハードウェア構成
- ソフトウェアおよびバージョン
- OS・カーネル
- 設定ファイル
- ベンチマーク手順
- 実験用スクリプト
- 公開可能な生の測定データ
- 処理済みデータ
- グラフ・図表
- 実験時の問題および失敗例

## 現在の進捗

### MP61-N01

最初の実験ノード `MP61-N01` について、購入時構成での
ベースライン測定および長時間Qualificationを完了しました。

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

2026-09-27 に以下の連続試験を実施しました。

| Test | Duration | Result |
| ------------------ | -------: | ------ |
| Memory stress | 3 h | PASS |
| Dual GPU stress | 2 h | PASS |
| CPU mixed workload | 1 h | PASS |

全試験を通して、

- EDAC Correctable Errors: 0
- EDAC Uncorrectable Errors: 0
- Kernel / hardware error log matches: 0
- Thermal safety stop: なし
- Final result: PASS

詳細:

- [MP61-N01 ハードウェア構成](docs/hardware/MP61-N01.md)
- [Qualification結果](results/MP61-N01/S0-as-acquired/qualification-20260927.md)
- [Thermal Qualificationの試験方法](docs/methodology/thermal-qualification.md)
- [ファン制御](docs/methodology/fan-control.md)

### Kernel依存のVulkan op-offload性能差

AMD GFX6 GPUを搭載するMacPro6,1において、llama.cppのVulkan
operation-offload pp512経路にkernel version依存の大きく再現可能な
性能差を確認した。

2026-10-03に完走したA/B試験の最終データセットは576測定である。

| GPU | Linux 6.12.107 | Linux 6.12.111 | 107 / 111 |
|---|---:|---:|---:|
| FirePro D300 / Pitcairn、Lab1-3集約 | 63.031 tok/s | 16.448 tok/s | 3.832x |
| FirePro D500 / Tahiti、Lab5 | 39.433 tok/s | 20.049 tok/s | 1.967x |

Lab1、Lab2、Lab3、Lab5について、各node/kernelの組み合わせには
36 cycle、各boot 2 runによる72測定が含まれる。

別のD300搭載機Lab4はLinux 6.12.107固定referenceとして変更せずに
測定を継続し、255回の測定をすべて正常完了した。平均は
62.431 tok/s、run間の標準偏差は0.432 tok/sであった。

副次的な結果として、Linux 6.12.107上のD500搭載Lab5では
run-order依存が観測された。run 1は平均40.829 tok/s、run 2は
38.036 tok/sで、run 1が7.34%高かった。この副次的現象の原因は
まだ特定していない。

原因となるkernel commitまたはsubsystemは現時点では特定していない。

- [調査報告](docs/findings/kernel-vulkan-op-offload-20261003.ja.md)
- [データセットと集計結果](results/kernel-ab/20261003/README.md)
- [D300 kernel比較](figures/kernel-ab/20261003/d300-kernel-comparison.svg)
- [D500 kernel比較](figures/kernel-ab/20261003/d500-kernel-comparison.svg)
- [Lab4固定reference](figures/kernel-ab/20261003/lab4-fixed-reference.svg)

## リポジトリ構成（予定）

本プロジェクトでは、実験データやドキュメントを以下の構成で
整理していく予定です。

```text
docs/
├── hardware/       ハードウェア台帳および各ノードの仕様
├── methodology/    実験方法および測定手順
└── network/        ネットワークおよびThunderbolt構成資料

benchmarks/          ベンチマーク定義
data/                実験測定データ
results/             処理済みベンチマーク・Qualification結果
scripts/             インストール・測定・自動化スクリプト
figures/             構成図・グラフ・図表
paper/               研究論文・研究報告用資料
