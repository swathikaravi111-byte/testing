#!/usr/bin/env bash
# =============================================================================
# Configuration backup automation.
# Archives all CONFIG_SOURCES into a versioned tarball with checksum manifest.
# =============================================================================
set -euo pipefail
DR_ROOT="${DR_ROOT:-/home/user/testing/dr}"
# shellcheck disable=SC1091
source "$DR_ROOT/lib/common.sh"

start_log "config-backup"
acquire_lock "config-backup"

OUT="$CONFIG_DIR/config-${DATE_TAG}-${TIMESTAMP}.tar.gz"
STAGING="$CONFIG_DIR/.staging-$TIMESTAMP"
FAILED=0

mkdir -p "$STAGING"
trap 'rm -rf "$STAGING"' EXIT

info "starting configuration backup"

for src in "${CONFIG_SOURCES[@]}"; do
  if [[ -e "$src" ]]; then
    dest="$STAGING$(dirname "$src")"
    mkdir -p "$dest"
    cp -a "$src" "$dest/" 2>>"$CURRENT_LOG" || {
      warn "could not copy $src"
      FAILED=$((FAILED+1))
      continue
    }
    info "captured $src"
  else
    warn "source does not exist, skipping: $src"
  fi
done

if [[ -z "$(ls -A "$STAGING" 2>/dev/null)" ]]; then
  record_status "config-backup" 1 "no sources found"
  send_alert CRITICAL "Config backup FAILED" "No config sources were captured. Sources: ${CONFIG_SOURCES[*]}"
  exit 1
fi

tar -czf "$OUT" -C "$STAGING" . 2>>"$CURRENT_LOG" || {
  record_status "config-backup" 1 "tar failed"
  send_alert CRITICAL "Config backup FAILED" "tar creation failed. See $CURRENT_LOG"
  exit 1
}

write_manifest "$OUT" || {
  record_status "config-backup" 1 "manifest failed"
  send_alert CRITICAL "Config backup FAILED" "checksum manifest could not be written for $OUT"
  exit 1
}

enforce_retention "$CONFIG_DIR" "$RETENTION_CONFIG" "config-*.tar.gz*"

if [[ $FAILED -gt 0 ]]; then
  record_status "config-backup" 2 "partial ($FAILED sources missing)"
  send_alert WARNING "Config backup partial" "$FAILED config sources were missing; backup completed with the rest."
else
  record_status "config-backup" 0 "OK ($(du -h "$OUT" | cut -f1))"
  info "config backup complete: $OUT"
fi

info "=== config backup finished ==="
