# MacPro6,1 Fleet Kernel Qualification — K108 to K112

## 状態

2026-10-10 完了・公開用記録。

本publicationは、MacPro6,1 Local LLM Labで2026-10-06から2026-10-10に
実施した実験のうち、これまで独立した発表として公開していなかった
fleet / kernel qualification結果を保存するものです。

2026-10-03 Linux kernel / Vulkan性能研究、および2026-10-10 Thermal
Identification Studyは変更せず、historical publicationとしてそのまま残します。

## 対象

今回公開する内容：

- K108、K109、K110、K112の5-node公式長時間run
- K107〜K110で確認したpp512性能の安定性
- K110で観測したfleet全体のGPU温度差
- K111 historical datasetの再確認・archive化
- K112 kernel artifactのhashと同一artifactによる5-node配備
- 最初のK109失敗runを公式結果から除外した理由

K111の大幅なperformance regression自体は2026-10-03研究ですでに発表済みです。
今回はhistorical datasetの完全性とprovenanceのみを追加記録します。

## Fleet構成

| Label | CPU | GPU |
| --- | --- | --- |
| Lab1 | Xeon E5-1620 v2 | FirePro D300 ×2 |
| Lab2 | Xeon E5-1620 v2 | FirePro D300 ×2 |
| Lab3 | Xeon E5-1620 v2 | FirePro D300 ×2 |
| old Lab4 | Xeon E5-1620 v2 | FirePro D300 ×2 |
| USB2 | Xeon E5-1650 v2 | FirePro D500 ×2 |

`old Lab4`はhistoricalなfleet個体です。後にLab4/USB1となったthermal試験機とは別個体です。

## 公式fleet run

| Kernel | Official run | Final archive | Result |
| --- | --- | --- | --- |
| K108 | `k108-to1300-retry-20261006-190829` | `final-20261007-153455` | 5/5 SUCCESS |
| K109 | `k109-to1300-retry-20261007-162623` | `final-20261008-130717` | 5/5 SUCCESS |
| K110 | `k110-to1300-20261008-170221` | `final-20261009-130832` | 5/5 SUCCESS |
| K112 | `k112-to1300-retry-20261009-162051` | `final-20261010-155301` | 5/5 SUCCESS |

cycle fieldの意味はrun間で完全には同一ではありません。

- K108 / K109はofficial summaryのreported final cycle
- K110はdeadlineで中断された最終cycleを除くhighest complete cycle
- K112はverified official final cycle

を記録します。

詳細は`data/fleet-runs.tsv`および`data/k110-cycle-coverage.tsv`に収録します。

K108 / K109ではofficial summary上のthermal waitは0です。
K110は5 nodeすべてにSUCCESSおよびDEADLINE_REACHED markerがありますが、
今回確認したfinal archiveから独立したthermal-wait counterは確定できないため、
0とはせず`not established`として扱います。
K112についても本publicationでは独立したthermal-wait countを断定しません。

K109 official summaryでは、Lab1 `c79-cpu`およびUSB2 `c73-nopo1`が
deadline-truncated sampleとしてperformance analysisから除外されています。

## K107〜K110のpp512安定性

K107、K108、K109、K110の比較では、20個すべてのnode/kernel setで
missing RC0 logは0でした。

GPU pp512 median：

- D300 fleet nodes：約 **61.95〜62.56 tok/s**
- USB2 / D500：約 **51.47〜51.55 tok/s**

これは、今回試験したfleetにおいてK107〜K110が安定した高性能reference領域を
形成していたことを示すqualification結果です。

ただし、これだけでK111 regressionの正確な境界commitを特定したとは言えません。
K107↔K111のoperation-offload regressionについては2026-10-03の既存発表を
正式なreportとして維持します。原因となるkernel commit/subsystemは未特定です。

## K108 / K109 thermal maxima

### K108

| Node | Te0 max °C | GPU max °C | CPU max °C |
| --- | ---: | ---: | ---: |
| Lab1 | 78.8 | 75 | 79 |
| Lab2 | 74.8 | 73 | 74 |
| Lab3 | 78.5 | 76 | 79 |
| Lab4 | 75.8 | 80 | 82 |
| USB2 | 83.2 | 75 | 76 |

### K109

| Node | Te0 max °C | GPU max °C | CPU max °C |
| --- | ---: | ---: | ---: |
| Lab1 | 79.2 | 66 | 68 |
| Lab2 | 75.0 | 67 | 65 |
| Lab3 | 78.2 | 69 | 69 |
| Lab4 | 76.2 | 73 | 69 |
| USB2 | 85.2 | 70 | 67 |

これらはfleet run中の観測値であり、一般化した運用上限値ではありません。

## K110 paired GPU温度観測

K110ではsensor output上の2つのAMD GPU PCI function、
`amdgpu-pci-0200`および`amdgpu-pci-0600`について、
paired temperature snapshotを保存しています。

すべての`sensors-cycle-*.txt`相当の利用可能なsnapshotを集計すると、
全nodeで平均`06:00.0 − 02:00.0`温度差は正でした。

| Node | Paired samples | Mean °C | Median °C | Min °C | Max °C | Positive samples |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Lab1 | 78 | +6.64 | +7.00 | -1.00 | +7.00 | 77/78 |
| Lab2 | 75 | +5.64 | +6.00 | -1.00 | +7.00 | 74/75 |
| Lab3 | 76 | +5.71 | +6.00 | 0.00 | +7.00 | 75/76 |
| Lab4 | 75 | +8.63 | +9.00 | +3.00 | +10.00 | 75/75 |
| USB2 | 70 | +4.57 | +5.00 | 0.00 | +6.00 | 69/70 |

論理的なGPU0/GPU1 mappingを仮定せず、測定で直接確認できるPCI function名で
記録します。

これはK110 run内の観測結果です。この結果だけでhardware fault、
MacPro6,1全般の普遍的な物理配置差、あるいは温度差の原因を断定しません。

## K111 historical dataset validation

historical source dataset：

`kernel-test/results/20261003-011042`

確認結果：

- K111 log 288個
- 36 cycle × 2 repeat × 4 label
- Lab1 / Lab2 / Lab3 / Lab5
- kernel `6.12.111+deb13-amd64`
- llama.cpp build `7ac59a6e3 (11207)`
- K107+K111 parser result 576 row
- 576 rowすべてSSH return code 0
- pp512 / tg1 missing 0
- 36 cycle × 2 repeat seriesはすべてcomplete

historical archive：

`macpro-fleet-bench/archives/k111-historical-20261003/final-20261010-162130`

manifest SHA-256：

`a8e3443296bf60b4fb50056f07bb4bfd0eedc9f326b6960c4ec6657007361da7`

このdatasetから得たkernel performance結論は2026-10-03にすでに発表済みであり、
今回の新規発見として再掲しません。

## K112 build / fleet deployment

K112は再現可能なlab artifactとしてbuildし、公式K112 qualification前に
同一artifact setを5台すべてへ導入しました。

| Artifact | SHA-256 |
| --- | --- |
| image package | `d7c102f1b6c7e91b7275f9f5be2e18fd4f497e683a7368f1aa77abe1f8de1102` |
| headers package | `f1f3ecf56a1742474c3c7d0243139a3ae8ecec1f022ce6070ef151a08948215f` |
| `vmlinuz` | `8d1d54d22545f8d160fdc8a12f2c4ae5f381fad99b9994376c333d5b1bd42d69` |
| source tar.xz | `164dc9d1f6c93c61a15e1f071c48379b467f2b17c469cce7223471968208ed03` |

official archive：

`macpro-fleet-bench/archives/k112-to1300-retry-20261009-162051/final-20261010-155301`

final archive manifest SHA-256：

`e5b4360df613160f65782b2da4d0593a6511934d9358b62a9840900c51542d9f`

K112 final summary：

- Lab1: cycle 42
- Lab2: cycle 41
- Lab3: cycle 42
- old Lab4: cycle 41
- USB2: cycle 48
- 5/5 `SUCCESS=yes`
- 5/5 `DEADLINE_REACHED=yes`
- 5/5 `FAILED=no`
- 5/5 `LAUNCH_FAILED=no`

これにより`6.12.112-labtest`について、artifact identityを保存した
5-node fleet qualification pointが得られました。

## 除外したK109 run

最初のK109 attempt：

`k109-to1300-20261007-161325`

は公式seriesから除外します。

deadlineをepoch secondsではなくISO stringで渡したため、
即座にdeadline到達となったautomation errorです。
kernel/nodeの失敗結果とは扱いません。

公式K109 retry：

`k109-to1300-retry-20261007-162623`

を正式結果とします。

## 今回確立したこと

1. K108、K109、K110、K112の公式fleet runは5 nodeすべてSUCCESS。
2. K107〜K110のpp512 medianはD300/D500 reference nodeで狭い高性能領域に留まった。
3. K111 historical datasetは構造的にcompleteでtrace可能。ただし5-node formal soakではない。
4. K112はartifact hashを保存し、同一artifactを5-nodeへ配備した上でqualificationを完了。
5. K110では全5 nodeで平均`06:00.0 − 02:00.0` GPU温度差が正というwithin-run observationが得られた。

## 今回確立していないこと

- K111 regressionを発生させた正確なkernel commit
- K110 PCI GPU温度差がhardware defectであるかどうか
- 異なるofficial runのcycle数をthroughputとして直接比較できるか
- production用thermal policy / fan curve

## Data files

`data/`：

- `fleet-runs.tsv`
- `k108-k109-thermal-maxima.tsv`
- `k110-pci-gpu-temperature-difference.tsv`
- `k110-cycle-coverage.tsv`
- `kernel-throughput-stability.tsv`
- `k111-historical-validation.tsv`
- `k112-artifact-hashes.tsv`

## 関連研究

- 2026-10-03 — Kernel-dependent Vulkan operation-offload performance
- 2026-10-10 — Thermal identification under sustained CPU + dual-GPU load

今回のpublicationは、これら既存研究を変更せず、
未発表だったfleet / kernel qualification記録を追加するものです。
