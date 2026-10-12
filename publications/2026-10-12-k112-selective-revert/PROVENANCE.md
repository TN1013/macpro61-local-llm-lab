# Provenance

MacPro6,1 Local LLM Lab

Selective-revert validation of Linux 6.12.112 pp512 regression

Research date:

2026-10-12

Test system:

Lab1
MacPro6,1
Xeon E5-1620 v2
FirePro D300 x2
Debian 13
amdgpu

Release-level regression boundary:

Linux 6.12.110 -> Linux 6.12.111

First bad commit:

0af7a28c53f1dab35d74f48966da5651dbde7492
drm/amd/pm/si: Fix updating clock limits from power states

Direct parent:

16052dbffa6647df6f40a4567a3a423ff53676d8

Referenced upstream original commit:

e6c5d36756e7d4d260e2365fc4d01226f1973152

Linux 6.12.112 base commit:

7aba70ab2e8d8ab3cd45abcaa15e1119a00dc42a

Local selective-revert commit:

2ca44dfc8f8bb482311796ab9d295d7219a1874e

Test kernel:

6.12.112-revert-0af7

Kernel config SHA256:

a4c7bb87dd9c51d02875ec2bc6588d63a021694ce1afef296a1c20cc965009e7

Kernel image SHA256:

853b37824e6d3a8df19ec77f6cfc157bae54b4b121eb3ac66d500b8be9b4ca7e

Kernel headers SHA256:

f66a9bd9c68ce48d162348394060f7e1f22a25fb8dc15ee8d12e178c0638d706

Revert patch SHA256:

e34fa6310240be1cd18723fe462d70837f6f9e889e54349f2e07865f6321d07e

Preserved run ID:

k112-revert-0af7-20261012

run-files.sha256 SHA256:

96de4f7dbf33102d3b82035803861cd93d1ff9d65b7145a724643a22120c73b0

build-manifest.txt SHA256:

49f5b07eb5eca883cd360e3a229c7ffa64fe89fdb68cb0415b94121bff348b88

llama.cpp commit:

7ac59a6e3ad851cd41af00f678effab0598ba9a8

llama-bench SHA256:

2735454274bb661268ef9ef8c441f932b59ff6fa548b11c4ffd87ca9d0cb6ed1

Qwen3-8B-Q4_K_M model SHA256:

d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785

Selective-revert result:

Vulkan0 pp512: 63.27 tok/s
Vulkan1 pp512: 62.64 tok/s
Result: PASS_COLD

Interpretation:

The selective revert restores the tested D300 system to the same
approximately 63 tok/s performance region observed before the regression.

Together with the commit-level bisect boundary, this provides strong
causal evidence that the change introduced by commit 0af7a28c53f1 is
responsible for the observed regression under the tested conditions.

The precise DPM/clock mechanism has not yet been established.
