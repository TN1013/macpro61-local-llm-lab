# MacPro6,1 Linux 6.12.110 → 6.12.111 pp512 Regression Boundary

[English](README.md)

## 状態

2026-10-11 制御条件付きkernel境界試験完了。

## 概要

Mac Pro (Late 2013 / MacPro6,1) 5台を使用し、
Linux 6.12.108、6.12.109、6.12.110、6.12.111、6.12.112を
同一のcold-test protocolで比較しました。

FirePro D300搭載4台では、Vulkan operation-offload pp512 throughputが
Linux 6.12.108〜6.12.110では約63 tok/sで安定していた一方、
Linux 6.12.111で約16.45 tok/sまで急激に低下しました。

Linux 6.12.112でも同じ低性能状態が継続しました。

したがって、本campaignの制御条件下では、
観測されたpp512 performance regressionの境界を

**Linux 6.12.110 → Linux 6.12.111**

の間へ局所化できます。

原因となる正確なupstream kernel commitまたはsubsystemは、
まだ特定していません。

## 過去研究との関係

2026-10-03のkernel / Vulkan研究では、
Linux 6.12.107と6.12.111の間に大きく再現性のあるperformance差が
存在することを確認しました。

ただし、その研究では中間kernelのどこで性能が変化したかまでは
確定していませんでした。

今回の2026-10-11研究は、その既存研究を書き換えたり置き換えたりする
ものではありません。

K108〜K112を同一protocolで連続比較する新しいfollow-up studyとして、
観測された境界を6.12.110→6.12.111まで狭めたものです。

2026-10-10のfleet kernel qualificationおよびthermal identification研究も、
historical publicationとして変更せず保持します。

## 試験fleet

| Label | CPU | GPU |
| --- | --- | --- |
| Lab1 | Xeon E5-1620 v2 | FirePro D300 ×2 |
| Lab2 | Xeon E5-1620 v2 | FirePro D300 ×2 |
| Lab3 | Xeon E5-1620 v2 | FirePro D300 ×2 |
| Legacy18 | Xeon E5-1620 v2 | FirePro D300 ×2 |
| USB2 | Xeon E5-1650 v2 | FirePro D500 ×2 |

`Legacy18`はhistorical fleet nodeです。
後にLab4/USB1となったthermal試験機とは別個体です。

## 試験kernel

今回比較したkernel：

- Linux 6.12.108-labtest
- Linux 6.12.109-labtest
- Linux 6.12.110-labtest
- Linux 6.12.111-labtest
- Linux 6.12.112-labtest

5 kernel × 5 nodeの全試験が正常完了しました。

campaignの最終結果：

`PASS_ALL_KERNELS`

## Benchmark path

canonical cold benchmarkでは、
llama.cppのVulkan operation-offload pp512 pathを使用しました。

主要option：

    -dev Vulkan0 / Vulkan1
    -ngl 0
    -lzm off
    -t 4
    -n 1
    -nopo 0
    -nkvo 1
    -p 512
    -r 5
    -b 512
    -ub 512

`-ngl 0`はGPUへoffloadするmodel layerを0にする指定ですが、
Vulkan operation offload自体は有効です。

したがって、この測定をpure CPU benchmarkとは表現しません。

全nodeでVulkan0とVulkan1を独立して測定しました。

## D300 fleet結果

Lab1、Lab2、Lab3、Legacy18の4台を平均したpp512 throughput：

| Kernel | Vulkan0 tok/s | Vulkan1 tok/s |
| --- | ---: | ---: |
| 6.12.108 | 63.2875 | 62.8450 |
| 6.12.109 | 63.1375 | 62.8275 |
| 6.12.110 | 62.9525 | 62.8875 |
| 6.12.111 | 16.4750 | 16.4225 |
| 6.12.112 | 16.4825 | 16.4275 |

K108、K109、K110は安定した高性能領域を形成しています。

K111、K112も互いにほぼ同一の低性能領域を形成しています。

## K110 → K111境界

Vulkan0：

    62.9525 → 16.4750 tok/s
    変化率: -73.829%
    slowdown: 3.821x

Vulkan1：

    62.8875 → 16.4225 tok/s
    変化率: -73.886%
    slowdown: 3.829x

試験したkernel series内では、
緩やかな性能低下ではなく明瞭なstep changeとして現れました。

## K112でも継続

K111→K112の変化：

    Vulkan0: +0.046%
    Vulkan1: +0.030%

したがって、K111で観測した低性能状態はK112でも継続しています。

## node間の再現性

D300 4台は、回帰側で非常に近い値へ収束しました。

K111：

    Vulkan0: 16.45〜16.49 tok/s
    Vulkan1: 16.41〜16.43 tok/s

K112：

    Vulkan0: 16.45〜16.50 tok/s
    Vulkan1: 16.42〜16.44 tok/s

複数の独立したD300搭載MacPro6,1で同じ挙動が再現しています。

## D500での観測

FirePro D500×2を搭載したUSB2でも低性能側への遷移を確認しました。

K111：

    Vulkan0: 20.06 tok/s
    Vulkan1: 19.99 tok/s

K112：

    Vulkan0: 20.24 tok/s
    Vulkan1: 20.07 tok/s

ただしD300とはeffect sizeが異なるため、
両GPU familyで同一の低下率とは扱いません。

## thermal / execution validity

今回のboundary campaignでは、既に確立したthermal safety controlを
使用しました。

すべてのkernel/node試験について、

- cold benchmark
- recovery check
- fan state restoration
- controller collection
- manifest verification

を正常完了しています。

`PASS_COLD`は試験protocolが正常完了し、
有効な証拠を取得できたことを意味します。

「performance regressionが無かった」という意味ではありません。

## 今回確立したこと

本実験条件では以下を確立しました。

1. Linux 6.12.108〜6.12.110は、D300 fleetにおいて安定した
   high-performance pp512領域を形成する。
2. Linux 6.12.111では6.12.110に対して約74%のpp512 throughput低下が発生する。
3. Linux 6.12.112でも同じ低性能状態が継続する。
4. 観測されたtested-release boundaryはLinux 6.12.110と6.12.111の間にある。
5. この境界は両Vulkan deviceおよび複数のMacPro6,1で再現する。

## 今回確立していないこと

今回の研究だけでは、以下はまだ確立していません。

- 原因となる正確なupstream Linux commit
- 責任を持つkernel subsystem
- `amdgpu`単独が原因であること
- pp512 slowdownを発生させる具体的mechanism
- 他のGFX6 hardwareやLinux distributionでも同じ現象が起きること

これらは次のcommit-level narrowing / bisect研究の対象です。

## Data

`data/`には公開用に正規化した結果を収録しています。

- `kernel-boundary-results.csv`
- `kernel-boundary-results.json`
- `d300-kernel-summary.json`
- `boundary-deltas.json`
- `boundary-summary.md`

正規化datasetは50 measurementです。

    5 kernels × 5 nodes × 2 Vulkan devices

## Provenance

証拠の由来については [PROVENANCE.md](PROVENANCE.md) を参照してください。

publication内ファイルのintegrityは `SHA256SUMS.txt` に保存します。

## 次の研究

release-level boundaryの局所化は完了しました。

次の独立研究として、
Linux 6.12.110と6.12.111の間でcommit-level narrowing / bisectを行い、
原因となるchangeを特定することが次の段階です。

その際も今回と同じbenchmark identity、thermal control、
validation procedureを維持する必要があります。
