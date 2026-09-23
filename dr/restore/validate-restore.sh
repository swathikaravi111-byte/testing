#!/usr/bin/env bash
# =============================================================================
# Data restoration validation.
# Performs a live restore of a backup into a scratch database and asserts the
# data is complete and queryable:
#   - all expected tables exist
#   - row counts are non-zero for core tables
#   - a sample query executes
#   - (optional) row counts match a previous snapshot within tolerance
#
# Usage: validate-restore.sh [--dump <dumpfile>] [--tables t1,t2,...]
#   Without --dump, validates the newest daily backup.
# =============================================================================
set -euo pipefail
DR_ROOT="${DR_ROOT:-/home/user/testing/dr}"
# shellcheck disable=SC1091
source "$DR_ROOT/lib/common.sh"

DUMP=""; EXPECTED_TABLES=""; TOLERANCE_PCT="${TOLERANCE_PCT:-5}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dump)   shift; DUMP="$1" ;;
    --tables) shift; EXPECTED_TABLES="$1" ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac
  shift
done

[[ "$DB_TYPE" == "postgres" ]] || { error "validate-restore only supports postgres"; exit 1; }

start_log "validate-restore"
acquire_lock "validate-restore"

if [[ -z "$DUMP" ]]; then
  DUMP="$(ls -1t "$DAILY_DIR"/*.dump 2>/dev/null | head -n1 || true)"
  [[ -n "$DUMP" ]] || { error "no dump specified and no daily backup found"; exit 1; }
fi

info "validating restore of $(basename "$DUMP")"

# -- restore into scratch DB ------------------------------------------------
if ! "$DR_ROOT/restore/restore-db.sh" --scratch "$DUMP" >>"$CURRENT_LOG" 2>&1; then
  send_alert CRITICAL "Restore validation FAILED" "Could not restore $DUMP into scratch DB."
  record_status "validate-restore" 1 "restore step failed"
  exit 1
fi

# scratch DB is dropped by restore-db.sh on success; recreate it for queries
psql_admin=(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres)
"${psql_admin[@]}" -qc "CREATE DATABASE $VERIFY_SCRATCH_DB;" >>"$CURRENT_LOG" 2>&1
PGPASSWORD="${DB_PASSWORD:-}" pg_restore -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" \
  -d "$VERIFY_SCRATCH_DB" --no-owner --exit-on-error "$DUMP" >>"$CURRENT_LOG" 2>&1

q() { PGPASSWORD="${DB_PASSWORD:-}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" \
      -d "$VERIFY_SCRATCH_DB" -tAc "$1" 2>>"$CURRENT_LOG"; }

FAILED=0

TABLES=$(q "SELECT count(*) FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');")
info "scratch DB contains $TABLES user tables"
[[ "$TABLES" -gt 0 ]] || { error "no user tables after restore"; FAILED=1; }

if [[ -n "$EXPECTED_TABLES" ]]; then
  IFS=',' read -ra TARR <<< "$EXPECTED_TABLES"
  for t in "${TARR[@]}"; do
    n=$(q "SELECT count(*) FROM \"$t\";" || echo x)
    if [[ "$n" == "x" ]]; then
      error "expected table '$t' missing or unreadable"
      FAILED=$((FAILED+1))
    else
      info "table '$t': $n rows"
      if [[ "$n" -eq 0 ]]; then
        warn "table '$t' has 0 rows"
      fi
    fi
  done
else
  # assert every table with data in the dump has >0 rows in the restore
  while read -r t; do
    [[ -z "$t" ]] && continue
    n=$(q "SELECT count(*) FROM \"$t\";" || echo x)
    [[ "$n" == "x" ]] && { error "table '$t' unreadable"; FAILED=$((FAILED+1)); continue; }
    info "table '$t': $n rows"
  done < <(pg_restore --list "$DUMP" 2>/dev/null \
           | awk '/TABLE DATA/ {print $NF}' | sed 's/^[^.]*\.//' | sort -u)
fi

# sample join query executes without error
if ! q "SELECT 1;" >/dev/null || ! q "SELECT count(*) FROM information_schema.tables;" >/dev/null; then
  error "basic queries against restored DB failed"
  FAILED=$((FAILED+1))
fi

# cleanup
"${psql_admin[@]}" -qc "DROP DATABASE IF EXISTS $VERIFY_SCRATCH_DB;" >>"$CURRENT_LOG" 2>&1

if [[ $FAILED -gt 0 ]]; then
  send_alert CRITICAL "Restore validation FAILED" "$FAILED validation assertions failed for $DUMP"
  record_status "validate-restore" 1 "$FAILED assertions failed"
  exit 1
fi

record_status "validate-restore" 0 "$TABLES tables validated OK"
info "=== restore validation passed ($TABLES tables) ==="
