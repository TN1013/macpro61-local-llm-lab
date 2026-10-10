# 週間研究総括 — 2026-10-10

本書は、今週並行して進めた3つの研究トラックを接続する総括です。

## 1. Kernel / Vulkan性能

既発表の2026-10-03 A/B研究では、MacPro6,1のllama.cpp Vulkan
operation-offload pp512経路において、Linux 6.12.107と6.12.111の間に
大きく再現可能なkernel依存性能差を確認しました。

この既発表reportは変更しません。

今週はK111 historical datasetを再検証し、provenanceを付けてarchive化しました。
K111 log 288個、K107+K111 combined 576 row、pp512/tg1 missing 0を確認しています。

## 2. Fleet kernel qualification

K108、K109、K110、K112の公式fleet runは、いずれも5 nodeすべてSUCCESSでした。

K107〜K110のpp512 medianは、試験したD300/D500 reference nodeで狭い
高性能領域に留まりました。K112ではbuild artifact hashを保存し、
同一artifactを5台へ配備した上で長時間qualificationを完了しました。

これは、これまで独立publicationとして未発表だったfleet-levelの再現性と
長時間qualificationを記録するものです。

## 3. Thermal / SMC / fan control

別途公開した2026-10-10 thermal-identification研究では、CPU + dual-GPU
持続負荷、Apple SMC AUTO、固定fan speed、dynamic fan-speed responseを
調査しました。

このthermal研究も独立したhistorical publicationとして維持します。

## 総合的な意味

今週の研究では、相互に補完する3点が明確になりました。

- kernel behaviorによってperformanceが大きく変わり得ること
- fleet-levelの再現性には同一artifactと長時間multi-node qualificationが必要なこと
- 持続Local LLM workloadにはthermal behaviorの明示的評価が必要なこと

次の段階では、同一のcontrolled Local LLM workloadの下で、
throughput、両GPU、kernel version、fan response、temperature、
sustained stabilityを同時測定する統合研究へ進めるべきです。

現時点では、K111 regressionの正確なcommit、production fan curve、
K110で観測したPCI GPU温度差の普遍的原因は確定していません。
