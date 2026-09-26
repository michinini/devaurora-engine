#!/bin/bash
# Batch deobfuscation runner — runs up to 2 scripts in parallel (2 CPUs available).
# Usage: batch_deobf.sh <input1> <output1> [<input2> <output2> ...]
# Logs per script in /home/z/my-project/engine/test/logs/<name>.log
# Exit code 0 = all OK; otherwise lists failures.

cd /home/z/my-project/engine/Deobfuscator || exit 2
LOGDIR=/home/z/my-project/engine/test/logs
mkdir -p "$LOGDIR"

PIDS=()
NAMES=()
while [ $# -ge 2 ]; do
  IN="$1"; OUT="$2"; shift 2
  NAME=$(basename "$IN" | sed 's/\.[^.]*$//')
  echo "[start $(date +%H:%M:%S)] $NAME"
  ( timeout 560 python3 deobf/deob.py "$IN" -o "$OUT" --timeout 480 > "$LOGDIR/${NAME}.log" 2>&1 ) &
  PIDS+=("$!")
  NAMES+=("$NAME")
done

rc=0
for i in "${!PIDS[@]}"; do
  wait "${PIDS[$i]}"; r=$?
  if [ "$r" -eq 0 ]; then
    echo "[OK $(date +%H:%M:%S)] ${NAMES[$i]}"
  else
    echo "[FAIL rc=$r $(date +%H:%M:%S)] ${NAMES[$i]} — log: $LOGDIR/${NAMES[$i]}.log"
    rc=1
  fi
done
exit $rc
