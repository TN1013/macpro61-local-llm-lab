#!/usr/bin/env bash

SSH_USER="${SSH_USER:-user}"
SSH_KEY="${SSH_KEY:-$HOME/.ssh/id_ed25519_macpro_controller}"
echo
echo "============================================================"
echo " Mac Pro LLM Lab status"
echo " $(date '+%F %T %Z')"
echo "============================================================"

for x in \
  "lab1 ${LAB1_IP:-192.0.2.11}" \
  "lab2 ${LAB2_IP:-192.0.2.12}" \
  "lab3 ${LAB3_IP:-192.0.2.13}" \
  "lab4 ${LAB4_IP:-192.0.2.14}" \
  "lab5 ${LAB5_IP:-192.0.2.15}"
do
  set -- $x
  name=$1
  ip=$2

  printf "%-5s %-15s : " "$name" "$ip"

  timeout 8s ssh \
    -o BatchMode=yes \
    -o ConnectTimeout=3 \
    -i "$SSH_KEY" \
    "$SSH_USER@$ip" '
      printf "kernel=%s  " "$(uname -r)"
      printf "uptime=%s  " "$(uptime -p)"
      printf "load=%s  " "$(awk "{print \$1,\$2,\$3}" /proc/loadavg)"

      if pgrep -x llama-bench >/dev/null; then
        printf "BENCH=RUNNING pid="
        pgrep -x llama-bench | paste -sd, -
      else
        echo "BENCH=idle"
      fi
    ' 2>/dev/null || echo "SSH DOWN / rebooting"
done

echo
echo "============================================================"
echo " Lab1/2/3/5 automatic 107 <-> 111 A/B"
echo "============================================================"

if [ -f ~/kernel-test/overnight-runner.pid ]; then
  pid=$(cat ~/kernel-test/overnight-runner.pid)

  if ps -p "$pid" >/dev/null 2>&1; then
    ps -p "$pid" -o pid,etime,stat,%cpu,%mem,cmd
  else
    echo "runner: FINISHED / not running"
  fi
fi

echo
echo "--- latest A/B runner log ---"
tail -n 16 ~/kernel-test/overnight-runner.log 2>/dev/null

echo
echo "--- latest A/B measurements ---"
LATEST_RESULT=$(ls -1dt ~/kernel-test/results/* 2>/dev/null | head -1)

if [ -n "$LATEST_RESULT" ] && [ -f "$LATEST_RESULT/summary.tsv" ]; then
  tail -n 16 "$LATEST_RESULT/summary.tsv"
else
  echo "no summary yet"
fi

echo
echo "============================================================"
echo " Lab4 fixed kernel 6.12.107 reference"
echo "============================================================"

if [ -f ~/kernel-test/lab4-fixed-reference.pid ]; then
  pid=$(cat ~/kernel-test/lab4-fixed-reference.pid)

  if ps -p "$pid" >/dev/null 2>&1; then
    ps -p "$pid" -o pid,etime,stat,%cpu,%mem,cmd
  else
    echo "runner: FINISHED / not running"
  fi
fi

echo
tail -n 8 ~/kernel-test/lab4-fixed-reference/summary.log 2>/dev/null

echo
echo "============================================================"
echo " Kernel 6.12.108 / 109 / 110 build"
echo "============================================================"

if [ -f ~/kernel-test/build-108-110.pid ]; then
  pid=$(cat ~/kernel-test/build-108-110.pid)

  if ps -p "$pid" >/dev/null 2>&1; then
    ps -p "$pid" -o pid,etime,stat,%cpu,%mem,cmd
  else
    echo "builder: FINISHED / not running"
  fi
fi

echo
echo "--- build runner ---"
tail -n 10 ~/kernel-test/build-108-110.out 2>/dev/null

echo
echo "--- latest compiler log ---"
LATEST_BUILD=$(
  ls -1t ~/kernel-test/build-logs/linux-6.12.*.log \
    2>/dev/null | head -1
)

if [ -n "$LATEST_BUILD" ]; then
  echo "$LATEST_BUILD"
  tail -n 12 "$LATEST_BUILD"
else
  echo "no build log"
fi

echo
echo "--- completed .deb files ---"
find ~/kernel-test/debs \
  -type f \
  -name '*.deb' \
  -printf '%TY-%Tm-%Td %TH:%TM  %p\n' \
  2>/dev/null

echo
echo "--- controller disk space ---"
df -h ~ | tail -1

echo
echo "============================================================"
