#!/usr/bin/env bash
# =============================================================================
# Backup failure monitoring & alerting.
# Reads $STATE_DIR/status.tsv, alerts on:
#   - non-zero exit codes
#   - missing recent job completions (staleness)
# Usage: monitor-backups.sh   (run from cron, e.g. every 15 min)
# =============================================================================
set -euo pipefail
DR_ROOT="${DR_ROOT:-/home/user/testing/dr}"
# shellcheck disable=SC1091
source "$DR_ROOT/lib/common.sh"

start_log "monitor-backups"
acquire_lock "monitor-backups"

# job_name:max_age_hours
JOBS=(
  "db-backup-daily:26"
  "config-backup:26"
  "verify-backup:26"
)

# minutes since a timestamp
age_minutes() {
  echo $(( ( $(date +%s) - $(date -d "$1" +%s) ) / 60 ))
}

ISSUES=0

for entry in "${JOBS[@]}"; do
  job="${entry%%:*}"
  max_h="${entry##*:}"

  IFS=$'\t' read -r code ts <<< "$(get_last_status "$job")"

  if [[ -z "${code:-}" ]]; then
    send_alert WARNING "Backup job never ran" "$job has no recorded status yet."
    warn "$job: no status recorded"
    continue
  fi

  if [[ "$code" != "0" ]]; then
    send_alert CRITICAL "Backup job FAILED" "$job exited with code $code at $ts."
    error "$job: last run FAILED (code $code at $ts)"
    ISSUES=$((ISSUES+1))
    continue
  fi

  mins=$(age_minutes "$ts")
  if [[ $mins -gt $((max_h * 60)) ]]; then
    send_alert CRITICAL "Backup job STALE" "$job last succeeded $mins minutes ago (expected within ${max_h}h)."
    error "$job: stale, last success ${mins}m ago"
    ISSUES=$((ISSUES+1))
  else
    info "$job: OK (last success ${mins}m ago)"
  fi
done

record_status "monitor-backups" "$ISSUES" "$ISSUES issue(s) detected"
[[ $ISSUES -eq 0 ]] && info "=== monitoring clean ===" || exit 1
