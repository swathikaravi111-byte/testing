#!/usr/bin/env bash
# =============================================================================
# Common library for backup & disaster recovery scripts.
# Sourced by all backup/restore/verify scripts.
# =============================================================================
set -o pipefail

# --- Locations ---------------------------------------------------------------
DR_ROOT="${DR_ROOT:-/home/user/testing/dr}"
BACKUP_ROOT="${BACKUP_ROOT:-/var/backups/dr}"
LOG_DIR="${LOG_DIR:-$BACKUP_ROOT/logs}"
STATE_DIR="${STATE_DIR:-$BACKUP_ROOT/state}"
LOCK_DIR="/tmp/dr-locks"

DAILY_DIR="$BACKUP_ROOT/daily"
WEEKLY_DIR="$BACKUP_ROOT/weekly"
MONTHLY_DIR="$BACKUP_ROOT/monthly"
CONFIG_DIR="$BACKUP_ROOT/config"
VERIFY_DIR="$BACKUP_ROOT/verify"

RETENTION_DAILY="${RETENTION_DAILY:-7}"
RETENTION_WEEKLY="${RETENTION_WEEKLY:-5}"
RETENTION_MONTHLY="${RETENTION_MONTHLY:-12}"
RETENTION_CONFIG="${RETENTION_CONFIG:-30}"
RETENTION_VERIFY="${RETENTION_VERIFY:-14}"

# --- Load config file (may override DB_* variables) --------------------------
if [[ -f "$DR_ROOT/config/backup.conf" ]]; then
  # shellcheck disable=SC1091
  source "$DR_ROOT/config/backup.conf"
fi

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${DB_USER:-postgres}"
DB_NAME="${DB_NAME:-appdb}"
DB_TYPE="${DB_TYPE:-postgres}"

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
DATE_TAG="$(date +%Y%m%d)"

mkdir -p "$LOG_DIR" "$STATE_DIR" "$LOCK_DIR" "$DAILY_DIR" "$WEEKLY_DIR" \
         "$MONTHLY_DIR" "$CONFIG_DIR" "$VERIFY_DIR" 2>/dev/null || true

# --- Logging -----------------------------------------------------------------
log()   { echo "[$(date '+%F %T')] [$1] ${2:-}" | tee -a "${CURRENT_LOG:-/dev/null}"; }
info()  { log "INFO" "$*"; }
warn()  { log "WARN" "$*"; }
error() { log "ERROR" "$*" >&2; }

start_log() {
  CURRENT_LOG="$LOG_DIR/${1:-script}-$TIMESTAMP.log"
  : > "$CURRENT_LOG" 2>/dev/null || CURRENT_LOG=/dev/null
  info "=== $1 started (pid $$) ==="
}

# --- Locking (prevent concurrent runs of the same job) -----------------------
acquire_lock() {
  DR_LOCK_FILE="$LOCK_DIR/${1}.lock"
  if [[ -f "$DR_LOCK_FILE" ]] && kill -0 "$(cat "$DR_LOCK_FILE")" 2>/dev/null; then
    error "Another instance of '$1' is already running (pid $(cat "$DR_LOCK_FILE"))."
    exit 1
  fi
  echo $$ > "$DR_LOCK_FILE"
  trap 'rm -f "$DR_LOCK_FILE"' EXIT
}

# --- Exit code tracking for monitoring ----------------------------------------
record_status() { # job_name exit_code details
  printf '%s\t%s\t%s\t%s\n' "$(date -Iseconds)" "$1" "$2" "$3" >> "$STATE_DIR/status.tsv"
}
get_last_status() { # job_name -> "exit_code<TAB>timestamp"
  tail -n 200 "$STATE_DIR/status.tsv" 2>/dev/null | awk -F'\t' -v j="$1" '$2==j{c=$3;t=$1} END{print c"\t"t}'
}

# --- Notifications ------------------------------------------------------------
send_alert() { # severity subject body
  local severity="$1" subject="$2" body="$3"
  local line="[$severity] $subject -- $body ($(date -Iseconds))"
  echo "$line" >> "$STATE_DIR/alerts.log"
  # Webhook notification (Slack-compatible) if configured
  if [[ -n "${ALERT_WEBHOOK_URL:-}" ]]; then
    local payload
    payload=$(printf '{"text":"%s"}' "$line" | sed 's/"/\\"/g')
    curl -sf -m 10 -X POST -H 'Content-Type: application/json' \
         -d "$payload" "$ALERT_WEBHOOK_URL" >/dev/null 2>&1 || true
  fi
  # Email notification if configured
  if [[ -n "${ALERT_EMAIL:-}" ]] && command -v mail >/dev/null 2>&1; then
    echo "$body" | mail -s "[$severity] $subject" "$ALERT_EMAIL"
  fi
}

# --- Retention (delete old files matching a pattern) --------------------------
enforce_retention() { # directory retention_days pattern
  local dir="$1" days="$2" pattern="${3:-*}"
  [[ -d "$dir" ]] || return 0
  find "$dir" -maxdepth 1 -name "$pattern" -mtime +"$days" -print -delete 2>/dev/null \
    | while read -r f; do info "retention: removed $f"; done
}

# --- Checksum manifest ---------------------------------------------------------
manifest_path() { echo "$1.sha256"; }

write_manifest() { # backup_file
  ( cd "$(dirname "$1")" && sha256sum "$(basename "$1")" > "$(basename "$1").sha256" ) \
    && info "manifest written: $(manifest_path "$1")" \
    || { error "failed to write manifest for $1"; return 1; }
}

verify_manifest() { # backup_file -> 0 ok
  local f="$1" m
  m="$(manifest_path "$f")"
  [[ -f "$m" ]] || { error "missing manifest: $m"; return 1; }
  ( cd "$(dirname "$f")" && sha256sum -c "$(basename "$m")" --quiet ) \
    || { error "CHECKSUM MISMATCH for $f"; return 1; }
  return 0
}
