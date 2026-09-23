#!/usr/bin/env bash
# =============================================================================
# Automated backup verification — run daily after backups.
#
# Layer 1: checksum validation (sha256 manifest)
# Layer 2: structural validation (pg_restore --list / gzip -t)
# Layer 3: full restore test into a scratch database + row-count sampling
#
# Usage: verify-backup.sh [--full]
#   --full  also perform the Layer 3 live restore test
# =============================================================================
set -euo pipefail
DR_ROOT="${DR_ROOT:-/home/user/testing/dr}"
# shellcheck disable=SC1091
source "$DR_ROOT/lib/common.sh"

FULL=0
[[ "${1:-}" == "--full" ]] && FULL=1

start_log "verify-backup"
acquire_lock "verify-backup"

REPORT="$VERIFY_DIR/verify-$TIMESTAMP.txt"
: > "$REPORT"
FAILED=0
CHECKED=0

pass() { CHECKED=$((CHECKED+1)); echo "PASS  $1" >> "$REPORT"; info "PASS  $1"; }
fail() { FAILED=$((FAILED+1)); echo "FAIL  $1" >> "$REPORT"; error "FAIL  $1"; }

newest() { ls -1t "$1"/${2:-*}.dump 2>/dev/null | head -n1; }

# ---------------------------------------------------------------------------
# Layer 1: checksums for every backup present
# ---------------------------------------------------------------------------
for f in "$DAILY_DIR"/*.dump "$WEEKLY_DIR"/*.dump "$MONTHLY_DIR"/*.dump \
         "$CONFIG_DIR"/*.tar.gz; do
  [[ -f "$f" ]] || continue
  verify_manifest "$f" && pass "checksum: $(basename "$f")" \
                       || fail "checksum: $(basename "$f")"
done

# ---------------------------------------------------------------------------
# Layer 2: structural validation of newest daily DB backup
# ---------------------------------------------------------------------------
LATEST="$(newest "$DAILY_DIR")"
if [[ -z "$LATEST" ]]; then
  fail "no daily database backup found in $DAILY_DIR"
elif [[ "$DB_TYPE" == "postgres" ]]; then
  if pg_restore --list "$LATEST" >/dev/null 2>&1; then
    pass "structure: $(basename "$LATEST") readable by pg_restore"
    TABLES=$(pg_restore --list "$LATEST" 2>/dev/null | grep -c 'TABLE DATA' || true)
    pass "structure: dump contains $TABLES table-data entries"
    [[ "$TABLES" -gt 0 ]] || fail "structure: dump contains no table data"
  else
    fail "structure: $(basename "$LATEST") NOT readable by pg_restore"
  fi
else
  gzip -t "$LATEST" 2>/dev/null && pass "structure: $(basename "$LATEST") gzip valid" \
                                || fail "structure: $(basename "$LATEST") gzip corrupt"
fi

# newest config backup
CFG="$(ls -1t "$CONFIG_DIR"/config-*.tar.gz 2>/dev/null | head -n1 || true)"
if [[ -n "$CFG" ]]; then
  gzip -t "$CFG" 2>/dev/null && pass "structure: config archive $(basename "$CFG") valid" \
                               || fail "structure: config archive $(basename "$CFG") corrupt"
else
  fail "no config backup found in $CONFIG_DIR"
fi

# ---------------------------------------------------------------------------
# Layer 3: full restore test into scratch DB (weekly or --full)
# ---------------------------------------------------------------------------
if [[ $FULL -eq 1 && -n "${LATEST:-}" && "$DB_TYPE" == "postgres" ]]; then
  info "performing full restore test of $LATEST"
  if "$DR_ROOT/restore/restore-db.sh" --scratch "$LATEST" >>"$CURRENT_LOG" 2>&1; then
    pass "restore test: $LATEST restored into scratch DB '$VERIFY_SCRATCH_DB'"
  else
    fail "restore test: could not restore $LATEST into scratch DB"
  fi
fi

# ---------------------------------------------------------------------------
# Age check: backups must be recent
# ---------------------------------------------------------------------------
for level in daily weekly monthly; do
  dir_var="${level^^}_DIR"
  case $level in
    daily) max_age=1 ;; weekly) max_age=8 ;; monthly) max_age=32 ;;
  esac
  latest_for_level="$(ls -1t "${!dir_var}"/*.dump 2>/dev/null | head -n1 || true)"
  if [[ -z "$latest_for_level" ]]; then
    # monthly/weekly may legitimately not exist yet on a young install;
    # only daily is mandatory
    [[ "$level" == "daily" ]] && fail "age: no daily backup exists yet" \
                              || warn "no $level backup on record yet"
  else
    age=$(( ( $(date +%s) - $(stat -c %Y "$latest_for_level") ) / 86400 ))
    if [[ $age -gt $max_age ]]; then
      fail "age: newest $level backup is $age days old (max $max_age)"
    else
      pass "age: newest $level backup is $age day(s) old"
    fi
  fi
done

# ---------------------------------------------------------------------------
enforce_retention "$VERIFY_DIR" "$RETENTION_VERIFY" "verify-*"

{
  echo "=============================================="
  echo " Backup Verification Report — $(date -Iseconds)"
  echo "=============================================="
  echo "Checked: $CHECKED   Failed: $FAILED"
  [[ $FAILED -eq 0 ]] && echo "OVERALL: PASS" || echo "OVERALL: FAIL"
} >> "$REPORT"

if [[ $FAILED -gt 0 ]]; then
  record_status "verify-backup" 1 "$FAILED failures"
  send_alert CRITICAL "Backup verification FAILED" "$FAILED of $CHECKED verification checks failed. Report: $REPORT"
  exit 1
fi

record_status "verify-backup" 0 "all $CHECKED checks passed"
info "=== verification complete: $CHECKED checks, 0 failures ==="
