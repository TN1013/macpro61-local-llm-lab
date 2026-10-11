# Linux 6.12.110 → 6.12.111 pp512 Regression Boundary

## D300 fleet mean pp512 throughput

| Kernel | Vulkan0 tok/s | Vulkan1 tok/s |
|---|---:|---:|
| 6.12.108 | 63.2875 | 62.8450 |
| 6.12.109 | 63.1375 | 62.8275 |
| 6.12.110 | 62.9525 | 62.8875 |
| 6.12.111 | 16.4750 | 16.4225 |
| 6.12.112 | 16.4825 | 16.4275 |

## Boundary

- Vulkan0: 6.12.110 62.9525 → 6.12.111 16.4750 tok/s (-73.829%, 3.821x slower).
- Vulkan1: 6.12.110 62.8875 → 6.12.111 16.4225 tok/s (-73.886%, 3.829x slower).

## Persistence

- Vulkan0: 6.12.111 → 6.12.112 changed +0.046%.
- Vulkan1: 6.12.111 → 6.12.112 changed +0.030%.

## Interpretation

Under the controlled cold-test conditions used in this campaign, the pp512 regression boundary lies between Linux 6.12.110 and 6.12.111. Performance remains on the regressed side in 6.12.112.

