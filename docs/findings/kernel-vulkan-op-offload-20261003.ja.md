# MacPro6,1におけるカーネル依存のVulkan op-offload性能差

**状態:** 再現性を確認したA/B試験完了成果

**日付:** 2026-10-03

## 概要

複数のApple Mac Pro (Late 2013 / MacPro6,1)でLLMベンチマークを
行ったところ、AMD GFX6 GPUを使用するllama.cppのVulkan
operation-offload pp512経路において、Debian Linux 6.12.107-1と
6.12.111-1の間に大きく再現性のある性能差を確認した。

完走したA/B試験は36 cycle、合計576測定である。

原因となるupstream Linux kernelのcommitまたはsubsystemは
現時点では特定していない。

## 最初の観測

D300を2基搭載するMacPro6,1のうち、後にLab4とした個体だけが
pp512で約62 tokens/sを示した一方、他のD300個体は約16 tokens/s
であった。

Lab4はLinux 6.12.107を使用し、遅い個体は6.12.111を使用していた。

Lab4の環境は意図的に変更せず、その後は固定referenceとして
使用した。

## ベンチマーク条件の重要点

診断用ベンチマークの主要条件は以下である。

    -dev Vulkan0
    -ngl 0
    -nopo 0
    -nkvo 1
    -lzm off
    -t 4
    -p 512
    -n 1
    -r 10
    -b 512
    -ub 512

重要な点として、`-ngl 0`はGPUへoffloadするモデルlayerを0にする
指定であり、Vulkan operation offload自体を無効にする指定ではない。

したがって、本測定をpure CPU benchmarkとは表現しない。

`-nopo 1`でoperation offloadを無効化すると、大きなkernel依存の
pp512性能差は消失した。KV offloadではこの差を説明できなかった。

## 同一個体でのkernel A/B/A

Lab2の同一ハードウェア上でkernelだけを切り替えた結果、

    Linux 6.12.111 -> 約16.46 tok/s
    Linux 6.12.107 -> 約62.09 tok/s
    Linux 6.12.111 -> 約16.43 tok/s

となった。

ハードウェア、モデル、userspaceのbenchmark binaryは変更していない。

## 36-cycle A/B試験

Lab1、Lab2、Lab3、Lab5をLinux 6.12.107と6.12.111の間で
36 cycle切り替えた。

各kernel bootごとにpp512 benchmarkを2回実行した。

測定構成は以下である。

    36 cycle
    4 tested nodes
    2 kernels
    2 runs per boot
    576 total A/B measurements

したがって、各node/kernelの組み合わせには72測定が含まれる。

最終集計は以下の通りである。

| Node | GPU | Kernel | n | Mean tok/s | Run間SD |
|---|---|---:|---:|---:|---:|
| Lab1 | D300 / Pitcairn | 6.12.107 | 72 | 63.167 | 0.657 |
| Lab1 | D300 / Pitcairn | 6.12.111 | 72 | 16.454 | 0.043 |
| Lab2 | D300 / Pitcairn | 6.12.107 | 72 | 62.983 | 0.769 |
| Lab2 | D300 / Pitcairn | 6.12.111 | 72 | 16.445 | 0.050 |
| Lab3 | D300 / Pitcairn | 6.12.107 | 72 | 62.942 | 0.735 |
| Lab3 | D300 / Pitcairn | 6.12.111 | 72 | 16.446 | 0.044 |
| Lab5 | D500 / Tahiti | 6.12.107 | 72 | 39.433 | 1.408 |
| Lab5 | D500 / Tahiti | 6.12.111 | 72 | 20.049 | 0.062 |

## D300 / Pitcairn集約

Lab1、Lab2、Lab3をまとめると、

    Linux 6.12.107 -> 63.031 tok/s
    Linux 6.12.111 -> 16.448 tok/s
    ratio           -> 3.832x

となった。

D300の結果は3台の独立したnodeすべてで再現した。

## D500 / Tahiti

D500搭載のLab5でもkernel依存の性能差を確認した。

    Linux 6.12.107 -> 39.433 tok/s
    Linux 6.12.111 -> 20.049 tok/s
    ratio           -> 1.967x

D300とは差の大きさが大きく異なるため、両GPU構成で同一の
effect sizeが発生しているとは扱わない。

## Linux 6.12.107におけるD500のrun-order effect

副次的な結果として、D500搭載Lab5のLinux 6.12.107では、
非常に再現性の高いrun-order effectを確認した。

36 cycleの平均は、

    run 1 -> 40.829 tok/s
    run 2 -> 38.036 tok/s
    difference -> 2.793 tok/s
    run 1 versus run 2 -> +7.34%

であった。

cycle間の標準偏差は小さい。

    run 1 -> 0.085 tok/s
    run 2 -> 0.056 tok/s

一方、`llama-bench`が各benchmark invocation内部で報告した
標準偏差の平均は大きく異なった。

    run 1 mean reported SD -> 5.725 tok/s
    run 2 mean reported SD -> 0.131 tok/s

これは6.12.107でbootしたD500個体において、1回目と2回目の
benchmark invocationの間に再現性のある状態差が存在することを
示している。

ただし、その機構は今回のデータからは特定できない。GPU power
state、clock state、driver state、cache state、Vulkan execution
stateなどは候補仮説であり、本試験によって確定したものではない。

Lab5の6.12.111、およびD300個体では同程度のrun-order effectは
観測していない。

## 固定reference Lab4

Lab4はLinux 6.12.107の既存環境を変更せず、kernel A/B切替の対象
から除外した。

255回のreference測定をすべて正常に完了した。

    n    -> 255
    mean -> 62.431 tok/s
    SD   -> 0.432 tok/s

長時間測定を通して、6.12.111のD300個体で見られた約16.45 tok/s
付近への同程度の性能低下は観測されなかった。

Lab4はストレージとOSの履歴が他個体と異なるため、純粋なkernel
A/B比較ではなく、変更しない固定referenceとして扱う。

## 現時点で確認した項目

これまでの調査では以下を確認、または単純原因として除外した。

- 同一D300個体のGPU0/GPU1はいずれも同様のnode-level挙動を示す
- 単一GPU故障では説明できない
- 比較したD300機のPCIe linkは8.0 GT/s x16
- 確認した主要Vulkan、Mesa、libdrm runtime componentは一致
- 確認したPitcairn firmware fileは一致
- CPU model、thread設定、確認したpower policyでは説明できない
- KV offloadでは大きな性能差を説明できない
- Vulkan operation offloadを無効にすると大きな性能差は消える

ただし、あらゆるuserspaceまたはhardware要素が完全に同一である
ことを証明したものではない。

## 現時点で言えること

完走した実験結果は、次の記述を支持する。

> AMD GFX6 GPUを搭載する今回のMacPro6,1環境において、
> llama.cpp Vulkan operation-offload pp512経路では、Debian
> kernel 6.12.107-1と6.12.111-1の間に大きく再現性のある
> kernel依存の性能差が存在する。

測定した差は、D300 3台で約3.832倍、D500 1台で約1.967倍である。

## まだ言えないこと

現時点では以下は未確定である。

- 原因となるupstream Linux commit
- amdgpu単独が原因であること
- 性能差が変化する正確なupstream release境界
- Debian固有のpatch、config、build条件がendpoint差へ寄与する可能性
- D500 / 6.12.107のrun-order effectの機構
- 他のGFX6システムやLinux distributionでも再現するか

## 中間kernel build

follow-up試験用としてupstream Linux 6.12.108、6.12.109、
6.12.110のbuildはすべて正常完了した。

これらのcustom kernelはDebian 6.12.111のconfigを基にした共通configと
同じlocal build手順を使用している。

したがって、完走したA/B試験で使用したDebian package版
6.12.107および6.12.111とはprovenanceが完全には一致しない。

6.12.108から6.12.110のどこかで鋭い性能変化が見つかった場合でも、
それだけで原因となる境界がupstream stable releaseであることや、
特定commitが原因であることを証明するものではない。

より強い境界試験には、upstream 6.12.107から6.12.111を同一config、
toolchain、build手順でbuildして比較するか、Debian source packageを
一貫した条件で比較する必要がある。

## 次の試験

次のcontrolled testでは、すでにbuild済みのupstream Linux
6.12.108、6.12.109、6.12.110をまず単一test nodeで評価し、
その後必要に応じて他nodeへ展開する。

性能が変化する境界が確認できれば、stable kernelの変更単位、
必要に応じて特定commitのrevertまで進めて原因範囲を絞る。

今後はXeon CPU換装、メモリ容量と帯域、Thunderbolt 2を利用した
複数node分散推論についても検証する。
