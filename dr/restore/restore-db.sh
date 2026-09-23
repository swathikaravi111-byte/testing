#!/usr/bin/env bash
# =============================================================================
# Database restore / rollback script.
#
# Modes:
#   restore-db.sh <dumpfile>                 restore dump into DB_NAME
#   restore-db.sh --scratch <dumpfile>       restore into scratch DB (validation)
#   restore-db.sh --latest daily|weekly|monthly
#                                            restore newest backup of a level
#
# Safety:
#   - refuses to overwrite a non-empty target DB unless --force
#   - verifies checksum manifest before restoring
#   - creates a pre-restore safety backup
# =============================================================================
set -euo pipefail
DR_ROOT="${DR_ROOT:-/home/user/testing/dr}"
# shellcheck disable=SC1091
source "$DR_ROOT/lib/common.sh"

usage() {
  cat >&2 <<EOF
usage: $0 [options] <dumpfile | --latest daily|weekly|monthly>
  --scratch        restore into scratch validation DB instead of $DB_NAME
  --force          skip the non-empty-target safety check
EOF
  exit 2
}

SCRATCH=0; FORCE=0; DUMP=""; LATEST_LEVEL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --scratch) SCRATCH=1 ;;
    --force)   FORCE=1 ;;
    --latest)  shift; LATEST_LEVEL="${1:?}" ;;
    -h|--help) usage ;;
    *) DUMP="$1" ;;
  esac
  shift
done

if [[ -n "$LATEST_LEVEL" ]]; then
  case "$LATEST_LEVEL" in
    daily)   DIR="$DAILY_DIR" ;;
    weekly)  DIR="$WEEKLY_DIR" ;;
    monthly) DIR="$MONTHLY_DIR" ;;
    *) echo "invalid --latest level: $LATEST_LEVEL" >&2; exit 2 ;;
  esac
  DUMP="$(ls -1t "$DIR"/*.dump 2>/dev/null | head -n1 || true)"
  [[ -n "$DUMP" ]] || { error "no backups found in $DIR"; exit 1; }
fi

[[ -n "$DUMP" && -f "$DUMP" ]] || usage
start_log "restore-db"
acquire_lock "restore-db"

TARGET="$DB_NAME"
[[ $SCRATCH -eq 1 ]] && TARGET="$VERIFY_SCRATCH_DB"

info "restoring $DUMP -> $TARGET on $DB_HOST:$DB_PORT"

# --- 1. verify integrity first ------------------------------------------------
verify_manifest "$DUMP" || {
  send_alert CRITICAL "Restore ABORTED — checksum failure" "$DUMP failed checksum verification."
  exit 1
}
info "checksum OK"

# --- 2. safety backup of current target (non-scratch only) ---------------------
if [[ $SCRATCH -eq 0 ]]; then
  SAFETY="$DAILY_DIR/pre-restore-${TARGET}-${TIMESTAMP}.dump"
  if PGPASSWORD="${DB_PASSWORD:-}" pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" \
       $PGDUMP_OPTS "$TARGET" > "$SAFETY" 2>>"$CURRENT_LOG"; then
    write_manifest "$SAFETY"
    info "pre-restore safety backup: $SAFETY"
  else
    warn "pre-restore safety backup failed — continuing only with --force"
    [[ $FORCE -eq 1 ]] || exit 1
  fi
fi

# --- 3. recreate target ---------------------------------------------------------
if [[ "$DB_TYPE" == "postgres" ]]; then
  psql_cmd=(psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d postgres)

  psql=("${psql_cmd[@]}")
  [[ $FORCE -eq 1 ]] && psql+=(--set=ON_ERROR_STOP=0)

  # create scratch DB if needed
  if [[ $SCRATCH -eq 1 ]]; then
    "${psql_cmd[@]}" -qc "DROP DATABASE IF EXISTS $VERIFY_SCRATCH_DB;" >>"$CURRENT_LOG" 2>&1
    "${psql_cmd[@]}" -qc "CREATE DATABASE $VERIFY_SCRATCH_DB;" >>"$CURRENT_LOG" 2>&1
  else
    # check target non-empty
    N=$(PGPASSWORD="${DB_PASSWORD:-}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" \
        -d "$TARGET" -tAc \
        "SELECT count(*) FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');" 2>/dev/null || echo 0)
    if [[ "$N" -gt 0 && $FORCE -eq 0 ]]; then
      error "target DB '$TARGET' is non-empty ($N tables). Re-run with --force to overwrite."
      exit 1
    fi
    "${psql_cmd[@]}" -qc "DROP DATABASE IF EXISTS $TARGET;" >>"$CURRENT_LOG" 2>&1
    "${psql_cmd[@]}" -qc "CREATE DATABASE $TARGET;" >>"$CURRENT_LOG" 2>&1
  fi

  # --- 4. restore --------------------------------------------------------------
  PGPASSWORD="${DB_PASSWORD:-}" pg_restore -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" \
    -d "$TARGET" --no-owner $([[ $FORCE -eq 1 ]] || echo --exit-on-error) "$DUMP" \
    >>"$CURRENT_LOG" 2>&1

  # --- 5. validate -------------------------------------------------------------
  N=$(PGPASSWORD="${DB_PASSWORD:-}" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" \
      -d "$TARGET" -tAc \
      "SELECT count(*) FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema');")
  info "restored $N tables into '$TARGET'"

  # cleanup scratch DB after successful validation restore
  if [[ $SCRATCH -eq 1 ]]; then
    "${psql_cmd[@]}" -qc "DROP DATABASE IF EXISTS $VERIFY_SCRATCH_DB;" >>"$CURRENT_LOG" 2>&1
    info "scratch DB dropped"
  fi
else
  error "restore for DB_TYPE=$DB_TYPE not implemented in this script yet"
  exit 1
fi

record_status "restore-db" 0 "restored $(basename "$DUMP") -> $TARGET ($N tables)"
info "=== restore complete ==="
