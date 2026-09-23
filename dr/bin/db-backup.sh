#!/usr/bin/env bash
# =============================================================================
# Unified database backup driver — invoked by cron with a level:
#   db-backup.sh daily | weekly | monthly
#
# Levels:
#   daily    - compressed custom-format dump of each DB + manifest
#   weekly   - full dump (schema+data) promoted from daily, pg_basebackup if PG
#   monthly  - full dump, archived long-term, checksummed
# =============================================================================
set -euo pipefail
DR_ROOT="${DR_ROOT:-/home/user/testing/dr}"
# shellcheck disable=SC1091
source "$DR_ROOT/lib/common.sh"

LEVEL="${1:-}"
[[ "$LEVEL" =~ ^(daily|weekly|monthly)$ ]] || { echo "usage: $0 daily|weekly|monthly" >&2; exit 2; }

start_log "db-backup-$LEVEL"
acquire_lock "db-backup-$LEVEL"

case "$LEVEL" in
  daily)   OUT_DIR="$DAILY_DIR" ;;
  weekly)  OUT_DIR="$WEEKLY_DIR" ;;
  monthly) OUT_DIR="$MONTHLY_DIR" ;;
esac

FAILED=0
TOTAL=0

dump_one_db() {
  local db="$1" out
  TOTAL=$((TOTAL+1))
  out="$OUT_DIR/${LEVEL}-${db}-${TIMESTAMP}.dump"

  info "dumping database '$db' -> $out"

  case "$DB_TYPE" in
    postgres)
      PGPASSWORD="${DB_PASSWORD:-}" pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" \
        $PGDUMP_OPTS "$db" > "$out"
      ;;
    mysql)
      mysqldump -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" \
        ${DB_PASSWORD:+-p"$DB_PASSWORD"} --single-transaction --routines "$db" \
        | gzip > "$out"
      ;;
    *)
      error "unsupported DB_TYPE '$DB_TYPE'"
      return 1
      ;;
  esac

  write_manifest "$out" || { FAILED=$((FAILED+1)); return 1; }

  # integrity check: dump must be readable
  if [[ "$DB_TYPE" == "postgres" && "$LEVEL" == "daily" ]]; then
    pg_restore --list "$out" >/dev/null || {
      error "dump for '$db' failed integrity listing"
      send_alert CRITICAL "Backup integrity failure" "pg_restore --list failed for $out"
      FAILED=$((FAILED+1)); return 1
    }
  fi

  info "backup of '$db' complete ($(du -h "$out" | cut -f1))"
}

main() {
  info "starting $LEVEL database backup (type=$DB_TYPE host=$DB_HOST)"

  for db in $DB_NAME; do
    dump_one_db "$db" || true
  done

  # weekly/monthly: additionally capture globals (roles/tablespaces)
  if [[ "$LEVEL" != "daily" && "$DB_TYPE" == "postgres" ]]; then
    local g="$OUT_DIR/${LEVEL}-globals-${TIMESTAMP}.sql"
    PGPASSWORD="${DB_PASSWORD:-}" pg_dumpall -h "$DB_HOST" -p "$DB_PORT" \
      -U "$DB_USER" --globals-only > "$g" && write_manifest "$g"
  fi

  local ret
  case "$LEVEL" in
    daily)   ret=$RETENTION_DAILY ;;
    weekly)  ret=$RETENTION_WEEKLY ;;
    monthly) ret=$RETENTION_MONTHLY ;;
  esac
  enforce_retention "$OUT_DIR" "$ret" "${LEVEL}-*.dump*"

  if [[ $FAILED -gt 0 ]]; then
    record_status "db-backup-$LEVEL" 1 "$FAILED/$TOTAL databases failed"
    send_alert CRITICAL "Database backup FAILED ($LEVEL)" \
      "$FAILED of $TOTAL database backups failed. See $CURRENT_LOG"
    exit 1
  fi

  # optional offsite replication
  if [[ -n "${OFFSITE_DEST:-}" ]]; then
    if rsync -az ${OFFSITE_SSH_OPTS:-} "$OUT_DIR/" "$OFFSITE_DEST/$LEVEL/" 2>>"$CURRENT_LOG"; then
      info "offsite replication complete"
    else
      warn "offsite replication failed (backup itself succeeded)"
      send_alert WARNING "Offsite replication failed" "rsync to $OFFSITE_DEST failed for $LEVEL"
    fi
  fi

  record_status "db-backup-$LEVEL" 0 "$TOTAL databases backed up OK"
  info "=== $LEVEL database backup finished successfully ==="
}

main "$@"
