# MacPro6,1 Linux 6.12.112 Selective-Revert Validation

[English](README.md)

## 状態

2026-10-12 commit-level bisectおよびselective-revert検証完了。

## 概要

前回の制御条件付きkernel境界研究では、MacPro6,1 / FirePro D300の
Vulkan pp512 performance regressionがLinux 6.12.110から6.12.111への
移行区間で発生することを確認しました。

その後git bisectを実施し、first bad commitを次のcommitまで局所化しました。

`0af7a28c53f1dab35d74f48966da5651dbde7492`

`drm/amd/pm/si: Fix updating clock limits from power states`

direct parent:

`16052dbffa6647df6f40a4567a3a423ff53676d8`

はhigh-performance側に残っていました。

Lab1での直接境界測定：

| Commit | Vulkan0 pp512 | Vulkan1 pp512 | 判定 |
| --- | ---: | ---: | --- |
| parent `16052dbf` | 63.18 | 63.07 | GOOD |
| first bad `0af7a28c` | 16.45 | 16.48 | BAD |

bisect判定とは独立して因果性を確認するため、
Linux 6.12.112からこのcommitだけをselective revertしたkernelを作成しました。

kernel:

`6.12.112-revert-0af7`

同じcanonical cold benchmarkをLab1で実行した結果：

| Kernel | Vulkan0 pp512 | Vulkan1 pp512 |
| --- | ---: | ---: |
| Linux 6.12.112 D300 fleet平均 | 16.4825 | 16.4275 |
| Linux 6.12.112 selective revert / Lab1 | 63.27 | 62.64 |

selective revertによってD300のperformanceは、
回帰以前と同じ約63 tok/sの領域まで復帰しました。

## 前回publicationとの関係

本publicationは次の研究のfollow-upです。

[Linux 6.12.110 → 6.12.111 regression boundary](../2026-10-11-kernel-regression-boundary/README.ja.md)

前回の研究成果はrelease-level boundaryを記録するhistorical publicationとして
変更せず保持します。

前回は原因commitをまだ特定していませんでした。
今回はその次段階であるcommit-level narrowingとselective-revert検証です。

## First bad commit

first bad commit:

`0af7a28c53f1dab35d74f48966da5651dbde7492`

subject:

`drm/amd/pm/si: Fix updating clock limits from power states`

direct parent:

`16052dbffa6647df6f40a4567a3a423ff53676d8`

対象file:

`drivers/gpu/drm/amd/pm/legacy-dpm/si_dpm.c`

このchangeはSouthern Islands legacy DPMのclock limit処理を変更します。

## Selective-revert kernel

Linux 6.12.112 base:

`7aba70ab2e8d8ab3cd45abcaa15e1119a00dc42a`

local revert commit:

`2ca44dfc8f8bb482311796ab9d295d7219a1874e`

kernel release:

`6.12.112-revert-0af7`

生成されたconfigはvanilla `6.12.112-labtest` とbyte-identicalです。

config SHA256:

`a4c7bb87dd9c51d02875ec2bc6588d63a021694ce1afef296a1c20cc965009e7`

kernel image SHA256:

`853b37824e6d3a8df19ec77f6cfc157bae54b4b121eb3ac66d500b8be9b4ca7e`

revert patch SHA256:

`e34fa6310240be1cd18723fe462d70837f6f9e889e54349f2e07865f6321d07e`

## Benchmark identity

前回のrelease-boundary研究と同じcanonical operation-offload benchmarkを
維持しました。

llama.cpp:

`7ac59a6e3ad851cd41af00f678effab0598ba9a8`

llama-bench SHA256:

`2735454274bb661268ef9ef8c441f932b59ff6fa548b11c4ffd87ca9d0cb6ed1`

model:

`Qwen3-8B-Q4_K_M.gguf`

model SHA256:

`d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785`

主要option:

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

`-ngl 0`でもVulkan operation offloadは有効であるため、
pure CPU benchmarkとは扱いません。

## 結果

selective-revert run:

`PASS_COLD`

Vulkan0:

`63.27 tok/s`

Vulkan1:

`62.64 tok/s`

これはK108〜K110で観測した回帰前のperformance領域とほぼ同等です。

参考となるD300 fleet平均：

| Kernel | Vulkan0 | Vulkan1 |
| --- | ---: | ---: |
| 6.12.110 | 62.9525 | 62.8875 |
| 6.12.112 vanilla | 16.4825 | 16.4275 |

## 今回確立したこと

本研究条件では以下を確立しました。

1. release-level regression boundaryはLinux 6.12.110と6.12.111の間にある。
2. git bisectで`0af7a28c53f1`がfirst bad commitとして特定された。
3. そのdirect parentはhigh-performance側にある。
4. first bad commitではLab1がlow-performance側へ遷移する。
5. Linux 6.12.112から同commitだけをrevertすると約63 tok/sへ復帰する。
6. bisectとselective revertを組み合わせた結果から、
   tested D300 MacPro6,1におけるperformance regressionは
   `0af7a28c53f1`が導入したchangeによるものだという強い因果的証拠が得られた。

## 今回まだ確立していないこと

まだ確立していない事項：

- slowdownを発生させる具体的なDPM / clock-state mechanism
- 全GFX6 / Southern Islands hardwareで同一現象になるか
- FirePro D500でもselective revertによって同様に復旧するか
- このrevert自体が一般的なupstream fixとして適切か

commit内容からlegacy SI DPM clock-limit処理との関係は非常に強いですが、
具体的mechanismはruntime telemetryによる確認が必要です。

## D500と次の研究

前回のrelease-level campaignでは、USB2のFirePro D500でも
K111/K112で低性能側への遷移を既に観測しています。

ただしD500で`6.12.112-revert-0af7`を試す検証はまだ実施していません。

次は全く同じkernel binaryを、

- USB2 — FirePro D500 x2
- Lab7 — FirePro D500 x2

で試します。

またvanilla K112とselective-revert K112について、
同じVulkan負荷中のDPM / clock telemetryを比較し、
約3.8倍のperformance差を生む具体的mechanismを調査します。

## Evidence

再現性・integrity確認に必要な小さなartifactは`evidence/`へ保存しています。

正規化した結果は`data/`へ保存しています。

hashおよび実験identityは[PROVENANCE.md](PROVENANCE.md)を参照してください。
