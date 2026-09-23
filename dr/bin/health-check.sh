#!/usr/bin/env bash
# =============================================================================
# Read-only health summary of the backup estate. Never fails, never alerts.
# =============================================================================
set -euo pipefail
DR_ROOT="${DR_ROOT:-/home/user/testing/dr}"
# shellcheck disable=SC1091
source "$DR_ROOT/lib/common.sh"

start_log "health-check"
acquire_lock "health-check"

latest_in() { ls -1t "$1"/* 2>/dev/null | grep -v '\.sha256' | head -n1; }

echo "================ BACKUP HEALTH SUMMARY $(date -Iseconds) ================"
for d in DAILY WEEKLY MONTHLY CONFIG; do
  dir="${d}_DIR"; dir="${!dir}"
  f="$(latest_in "$dir")"
  n=$(ls -1 "$dir" 2>/dev/null | grep -vc '\.sha256' || true)
  if [[ -n "$f" ]]; then
    age=$(( ( $(date +%s) - $(stat -c %Y "$f") ) / 3600 ))
    size=$(du -h "$f" | cut -f1)
    printf '  %-8s %2s file(s) | newest: %s (%s, %sh ago)\n' \
      "${d,,}" "$n" "$(basename "$f")" "$size" "$age"
  else
    printf '  %-8s  0 file(s) | (empty)\n' "${d,,}"
  fi
done
echo "  ----------------------------------------------------------------------------"
echo "  Job statuses (newest last):"
tail -n 10 "$STATE_DIR/status.tsv" 2>/dev/null | column -t -s$'\t' || echo "    (none recorded)"
echo "  ----------------------------------------------------------------------------"
echo "  Alerts log:"
tail -n 5 "$STATE_DIR/alerts.log" 2>/dev/null || echo "    (no alerts — healthy)"
echo "=========================================================================="
