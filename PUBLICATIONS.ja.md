# MacPro6,1 Local LLM Lab — 研究成果と研究履歴

[English](PUBLICATIONS.md)

このファイルは、MacPro6,1 Local LLM Labで公開した研究成果を
時系列で記録する追記型のインデックスです。

公開済みの研究文書は、その時点における実験結果・方法・解釈を残す
歴史的記録として保存します。
後続の研究によって過去の成果を黙って書き換えるのではなく、
新しいpublicationとして追加していきます。

## 2026-10-03 — Linux kernel / Vulkan性能研究

**MacPro6,1におけるkernel依存のVulkan op-offload性能**

MacPro6,1上でLinux 6.12.107と6.12.111を比較した、
再現可能なA/B performance studyです。

主な内容：

- 36回のA/B cycle
- 合計576 measurement
- Vulkan operation-offloadを使用したpp512 path
- kernel versionに依存する大きなperformance差を観測
- 原因となった正確なkernel changeは現時点では未特定

Publication：

- [Kernel-dependent Vulkan op-offload performance](docs/findings/kernel-vulkan-op-offload-20261003.md)

この文書は、この実験についてのhistorical reportとして保持します。
後述のthermal studyによって置き換えられるものではありません。

---

## 2026-10-10 — Thermal identification study

**CPU + dual-GPU継続負荷下におけるMacPro6,1のthermal identification**

CPUと2基のGPUを同時に使用する継続負荷のもとで、
MacPro6,1のthermal behavior、Apple SMCによるautomatic fan response、
固定fan speed、およびfan speedを動的に変更した場合の挙動を調査した
follow-up studyです。

Publication：

- [English](publications/2026-10-10-thermal-identification/README.md)
- [日本語](publications/2026-10-10-thermal-identification/README.ja.md)

実験データおよび再現性確認用の資料は、
publication directory内に収録しています。

kernel-performance研究とthermal-control研究は、
現在のところ独立した研究系列として扱っています。

今後は、LLM throughput、dual-GPU utilization、kernel behavior、
thermal behavior、adaptive fan controlを、
同一の継続負荷条件のもとで組み合わせて検証することを想定しています。

---

## 2026-10-10 — Fleet kernel qualification study

**MacPro6,1 fleet kernel qualification — K108からK112まで**

2026年10月6日から10月10日にかけて実施した、
これまで独立したpublicationとして未公開だった
5-node fleet / kernel qualificationの研究記録を保存する
follow-up publicationです。

主な内容：

- K108 / K109 / K110 / K112の公式fleet runは5台すべてSUCCESS
- D300およびD500 nodeにおいてK107〜K110のpp512 reference regionが安定
- K110でPCI GPU間の温度差を観測
- K111 historical datasetの完全性を再検証し、provenanceを含めてarchive
- K112では同一artifactを5台へ配備し、SHA-256 hashを保存
- 最初のK109 attemptはautomationのdeadline-format errorによるものとして公式結果から明示的に除外

### 日本語概要

2026年10月6日から10月10日にかけて、
Mac Pro (Late 2013 / MacPro6,1) 5台を使用し、
Linux kernelおよびLocal LLMの長時間fleet検証を実施しました。

主な検証内容は以下の通りです。

- K108 / K109 / K110 / K112の公式fleet runは5台すべてSUCCESS
- K107〜K110ではpp512 performanceが安定
- K108 / K109の温度最大値を記録
- K110では2基のAMD GPU間の温度差を観測
- K111 historical datasetを再検証
- K112では同一artifact setを5台へ配備してqualificationを実施

詳細な日本語本文はこちらです。

- [日本語版](publications/2026-10-10-fleet-kernel-qualification/README.ja.md)

Publication：

- [English](publications/2026-10-10-fleet-kernel-qualification/README.md)
- [日本語](publications/2026-10-10-fleet-kernel-qualification/README.ja.md)

このpublicationは、
これまで未公開だったfleet / kernel qualificationの研究記録を追加するものであり、
先に公開したkernel / Vulkan研究やthermal-identification研究を
変更または置き換えるものではありません。

---

## 2026-10-11 — Linux 6.12.110 → 6.12.111 regression-boundary study

**MacPro6,1 Linux 6.12.110 → 6.12.111 pp512 regression boundary**

K108〜K112を5台のMacPro6,1で同一条件比較し、
Vulkan operation-offload pp512のperformance regression境界を
局所化したfollow-up studyです。

主な結果：

- D300 fleetではLinux 6.12.110まで約63 tok/sを維持
- Linux 6.12.111で約16.45 tok/sへ低下
- K110 → K111で約74%のthroughput低下
- Linux 6.12.112でも回帰側性能が継続
- 両Vulkan deviceで同じ境界を再現
- D500でもK111から低性能状態を確認
- 原因となる正確なkernel commit/subsystemは未特定

Publication：

- [English](publications/2026-10-11-kernel-regression-boundary/README.md)
- [日本語](publications/2026-10-11-kernel-regression-boundary/README.ja.md)

これは新しいfollow-up publicationです。
既存のkernel/Vulkan研究、thermal研究、fleet qualification研究は変更しません。

---

## Publication policy — 公開方針

今後の研究成果は、日付を明示した新しいpublicationとして追加していきます。

過去に公開したpublicationは原則として変更せず、
プロジェクトの発展、実験方法、解釈、
および後から行われた訂正を時系列で追跡できるように保持します。

過去の結論について、後から訂正または再解釈が必要になった場合は、
元のpublicationを直接書き換えるのではなく、
その文書を明示的に参照した新しいfollow-up publicationとして記録します。
