#!/usr/bin/env bash

set -u

SSH_KEY="$HOME/.ssh/id_ed25519_macpro_controller"
SSH_USER="${SSH_USER:-user}"
IP="${LAB4_IP:-192.0.2.14}"
OUT="$HOME/kernel-test/lab4-fixed-reference"

mkdir -p "$OUT"

STOP=$(date -d 'today 12:25' +%s)

run=1

while (( $(date +%s) < STOP )); do

    stamp=$(date +%Y%m%d-%H%M%S)
    file="$OUT/${stamp}-run${run}.log"

    echo "[$(date '+%F %T')] LAB4 run=$run start" |
        tee -a "$OUT/summary.log"

    ssh \
      -o BatchMode=yes \
      -o ConnectTimeout=5 \
      -i "$SSH_KEY" \
      "$SSH_USER@$IP" '
        echo "===== HOST ====="
        hostname

        echo "===== KERNEL ====="
        uname -r

        echo "===== UPTIME ====="
        uptime -p

        echo "===== BENCH ====="

        ~/src/llama.cpp/build-vulkan/bin/llama-bench \
          -m ~/models/benchmark/qwen3-8b/Qwen3-8B-Q4_K_M.gguf \
          -dev Vulkan0 \
          -ngl 0 \
          -nopo 0 \
          -nkvo 1 \
          -lzm off \
          -t 4 \
          -p 512 \
          -n 1 \
          -r 10 \
          -b 512 \
          -ub 512
      ' >"$file" 2>&1

    rc=$?

    result=$(grep 'pp512' "$file" | tail -1 || true)

    printf '[%s] run=%s rc=%s %s\n' \
      "$(date '+%F %T')" \
      "$run" \
      "$rc" \
      "$result" |
      tee -a "$OUT/summary.log"

    run=$((run + 1))

    sleep 60
done

echo "[$(date '+%F %T')] LAB4 fixed-reference finished" |
    tee -a "$OUT/summary.log"
