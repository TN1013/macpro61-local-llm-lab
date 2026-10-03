#!/usr/bin/env bash

set -u

SSH_KEY="$HOME/.ssh/id_ed25519_macpro_controller"
SSH_USER="${SSH_USER:-user}"

OUT="$HOME/kernel-test/results/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT"

HOSTS=(
  "lab1 ${LAB1_IP:-192.0.2.11}"
  "lab2 ${LAB2_IP:-192.0.2.12}"
  "lab3 ${LAB3_IP:-192.0.2.13}"
  "lab5 ${LAB5_IP:-192.0.2.15}"
)

STOP_NEW=$(date -d 'today 12:25' +%s)
RUNS_PER_BOOT=2

log()
{
  printf '[%s] %s\n' \
    "$(date '+%F %T')" "$*" |
    tee -a "$OUT/controller.log"
}

wait_boot()
{
  local name="$1"
  local ip="$2"
  local expected="$3"
  local oldid="$4"

  local deadline=$(( $(date +%s) + 900 ))

  while (( $(date +%s) < deadline )); do
    result=$(
      ssh \
        -o BatchMode=yes \
        -o ConnectTimeout=3 \
        -i "$SSH_KEY" \
        "$SSH_USER@$ip" \
        'printf "%s " "$(cat /proc/sys/kernel/random/boot_id)"; uname -r' \
        2>/dev/null || true
    )

    bootid=$(printf '%s\n' "$result" | awk '{print $1}')
    kernel=$(printf '%s\n' "$result" | awk '{print $2}')

    if [[ -n "$bootid" &&
          "$bootid" != "$oldid" &&
          "$kernel" == "6.12.${expected}+deb13-amd64" ]]
    then
      log "$name UP kernel=$kernel boot_id=$bootid"
      return 0
    fi

    sleep 5
  done

  log "ERROR: $name failed to boot kernel 6.12.$expected"
  return 1
}

boot_all()
{
  local target="$1"
  local stamp
  stamp=$(date +%Y%m%d-%H%M%S)

  declare -A OLDID

  log "Preparing reboot to 6.12.$target"

  for rec in "${HOSTS[@]}"; do
    set -- $rec
    name="$1"
    ip="$2"

    OLDID["$name"]=$(
      ssh \
        -o BatchMode=yes \
        -o ConnectTimeout=5 \
        -i "$SSH_KEY" \
        "$SSH_USER@$ip" \
        'cat /proc/sys/kernel/random/boot_id' \
        2>/dev/null || echo unknown
    )

    log "$name old_boot_id=${OLDID[$name]}"
  done

  for rec in "${HOSTS[@]}"; do
    set -- $rec
    name="$1"
    ip="$2"

    (
      ssh \
        -o BatchMode=yes \
        -o ConnectTimeout=5 \
        -i "$SSH_KEY" \
        "$SSH_USER@$ip" \
        "sudo -n /usr/local/sbin/lab-kernel-boot $target"
    ) >"$OUT/reboot-${stamp}-${name}-to-${target}.log" 2>&1 &
  done

  wait || true

  for rec in "${HOSTS[@]}"; do
    set -- $rec
    name="$1"
    ip="$2"

    wait_boot \
      "$name" \
      "$ip" \
      "$target" \
      "${OLDID[$name]}" || return 1
  done

  return 0
}

bench_all()
{
  local target="$1"
  local cycle="$2"

  for ((run=1; run<=RUNS_PER_BOOT; run++)); do

    stamp=$(date +%Y%m%d-%H%M%S)

    log "BENCH cycle=$cycle kernel=$target run=$run"

    for rec in "${HOSTS[@]}"; do
      set -- $rec
      name="$1"
      ip="$2"

      file="$OUT/${stamp}-cycle${cycle}-k${target}-r${run}-${name}.log"

      (
        timeout 20m ssh \
          -o BatchMode=yes \
          -o ConnectTimeout=5 \
          -i "$SSH_KEY" \
          "$SSH_USER@$ip" '
            echo "===== HOST ====="
            hostname

            echo "===== KERNEL ====="
            uname -r

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
          '

        echo "__SSH_RC=$?"
      ) >"$file" 2>&1 &
    done

    wait

    for rec in "${HOSTS[@]}"; do
      set -- $rec
      name="$1"

      file="$OUT/${stamp}-cycle${cycle}-k${target}-r${run}-${name}.log"

      result=$(grep 'pp512' "$file" | tail -1 || true)

      printf '%s\tcycle=%s\tkernel=%s\trun=%s\t%s\t%s\n' \
        "$(date '+%F %T')" \
        "$cycle" \
        "$target" \
        "$run" \
        "$name" \
        "$result" \
        >> "$OUT/summary.tsv"

      log "$name $result"
    done
  done
}

cycle=1

while (( $(date +%s) < STOP_NEW )); do

  for target in 107 111; do

    if (( $(date +%s) >= STOP_NEW )); then
      break 2
    fi

    log "===== cycle=$cycle target=$target ====="

    if ! boot_all "$target"; then
      log "Stopping experiment because a node failed to reboot correctly"
      break 2
    fi

    bench_all "$target" "$cycle"
  done

  cycle=$((cycle + 1))
done

log "Experiment period finished"
log "Returning all workers to kernel 6.12.107"

boot_all 107 || true

log "===== FINAL STATUS ====="

for rec in "${HOSTS[@]}"; do
  set -- $rec

  ssh \
    -o BatchMode=yes \
    -o ConnectTimeout=5 \
    -i "$SSH_KEY" \
    "$SSH_USER@$2" \
    'hostname; uname -r; uptime -p' \
    >> "$OUT/final-status.txt" 2>&1
done

log "DONE"
log "Results: $OUT"
