#!/usr/bin/env bash
# =============================================================================
# Test suite for the DR system. Uses a sandbox BACKUP_ROOT and stub
# pg_dump/pg_restore/psql binaries so no real database is required.
# Run: dr/tests/run-tests.sh
# =============================================================================
set -uo pipefail

DR_ROOT="/home/user/testing/dr"
TEST_ROOT="$(mktemp -d /tmp/dr-tests.XXXXXX)"
export BACKUP_ROOT="$TEST_ROOT/backups"
export DB_TYPE=postgres
export DB_NAME=appdb
export DB_USER=postgres
mkdir -p "$BACKUP_ROOT" "$TEST_ROOT/bin"

PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "  ✔ $1"; }
bad() { FAIL=$((FAIL+1)); echo "  ✘ $1"; }
check() { # desc condition
  if eval "${2:-false}"; then ok "$1"; else bad "$1"; fi
}

# --- stub binaries -----------------------------------------------------------
mkdir -p "$TEST_ROOT/bin"
cat > "$TEST_ROOT/bin/pg_dump" <<'EOF'
#!/usr/bin/env bash
# stub: emit a valid-looking custom dump marker to stdout
echo "PGDMP-STUB $(date +%s) $*"
EOF
cat > "$TEST_ROOT/bin/pg_restore" <<'EOF'
#!/usr/bin/env bash
if [[ "$1" == "--list" ]]; then
  f="${@: -1}"
  grep -q "PGDMP-STUB" "$f" 2>/dev/null || exit 1
  echo "TABLE DATA public users"
  echo "TABLE DATA public orders"
  exit 0
fi
exit 0
EOF
cat > "$TEST_ROOT/bin/psql" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
chmod +x "$TEST_ROOT/bin/"*
export PATH="$TEST_ROOT/bin:$PATH"

echo "=== DR system test suite (sandbox: $TEST_ROOT) ==="

# --- 1. library loads ---------------------------------------------------------
echo "[1] common library"
OUT=$(bash -c "source $DR_ROOT/lib/common.sh && echo lib-ok" 2>&1)
check "common.sh sources without error" "[[ '$OUT' == lib-ok ]]"
check "directories created" "[[ -d '$BACKUP_ROOT/daily' && -d '$BACKUP_ROOT/state' ]]"

# --- 2. daily database backup -------------------------------------------------
echo "[2] database backup (daily)"
OUT=$("$DR_ROOT/bin/db-backup.sh" daily 2>&1); RC=$?
check "db-backup daily exits 0" "[[ $RC == 0 ]]"
DUMP=$(ls "$BACKUP_ROOT/daily/"daily-appdb-*.dump 2>/dev/null | head -n1)
check "dump file created" "[[ -n '$DUMP' ]]"
check "sha256 manifest created" "[[ -f '${DUMP}.sha256' ]]"
check "status recorded as success" "grep -qP $'db-backup-daily\t0\t' '$BACKUP_ROOT/state/status.tsv'"

# --- 3. weekly backup + globals -------------------------------------------------
echo "[3] database backup (weekly)"
OUT=$("$DR_ROOT/bin/db-backup.sh" weekly 2>&1); RC=$?
check "db-backup weekly exits 0" "[[ $RC == 0 ]]"
check "globals captured" "[[ -n \"\$(ls '$BACKUP_ROOT/weekly/'weekly-globals-*.sql 2>/dev/null)\" ]]"

# --- 4. config backup -----------------------------------------------------------
echo "[4] config backup"
mkdir -p "$TEST_ROOT/fake-etc"
echo "server {}" > "$TEST_ROOT/fake-etc/nginx.conf"
# point CONFIG_SOURCES at the fake dir via an env-driven subshell invocation
OUT=$(BACKUP_ROOT="$BACKUP_ROOT" bash -c "
  set -a
  source '$DR_ROOT/config/backup.conf' >/dev/null 2>&1 || true
  CONFIG_SOURCES=(\"$TEST_ROOT/fake-etc\")
  export CONFIG_SOURCES
  '$DR_ROOT/bin/config-backup.sh'
" 2>&1); RC=$?
check "config-backup exits 0" "[[ $RC == 0 ]]"
CFG=$(ls "$BACKUP_ROOT/config/"config-*.tar.gz 2>/dev/null | head -n1)
check "config tarball created" "[[ -n '$CFG' ]]"
check "config manifest created" "[[ -f '${CFG}.sha256' ]]"

# --- 5. checksum verification ----------------------------------------------------
echo "[5] verify-backup (checksums, structure, age)"
OUT=$("$DR_ROOT/bin/verify-backup.sh" 2>&1); RC=$?
echo "$OUT" | sed 's/^/      /'
check "verify-backup passes on good backups" "[[ $RC == 0 ]]"
REPORT=$(ls -t "$BACKUP_ROOT/verify/"verify-*.txt 2>/dev/null | head -n1)
check "verification report written" "[[ -n '$REPORT' ]]"
grep -q "OVERALL: PASS" "$REPORT" && ok "report says OVERALL: PASS" || bad "report says OVERALL: PASS"

# --- 6. corruption detection -------------------------------------------------------
echo "[6] corruption detection"
CORRUPT="$BACKUP_ROOT/daily/$(basename "$DUMP")"
echo "tampered" >> "$CORRUPT"
OUT=$("$DR_ROOT/bin/verify-backup.sh" 2>&1); RC=$?
check "verify-backup FAILS on corrupted backup" "[[ $RC != 0 ]]"
check "corruption failure recorded" "grep -qP $'verify-backup\t1\t' '$BACKUP_ROOT/state/status.tsv'"
check "alert logged" "grep -q 'Backup verification FAILED' '$BACKUP_ROOT/state/alerts.log'"
# restore the file's integrity( cd "$(dirname "$DUMP")" && sha256sum "$(basename "$DUMP")" > "$(basename "$DUMP").sha256" )
"$DR_ROOT/bin/verify-backup.sh" >/dev/null 2>&1

# --- 7. monitoring -------------------------------------------------------------------
echo "[7] monitor-backups"
# all jobs succeeded recently -> should be clean except jobs never ran
OUT=$("$DR_ROOT/bin/monitor-backups.sh" 2>&1); RC=$?
check "monitor runs and reports (exit reflects issues)" "[[ \$OUT == *monitor-backups* ]]"
check "monitor status recorded" "grep -q monitor-backups '$BACKUP_ROOT/state/status.tsv'"

# --- 8. retention ----------------------------------------------------------------------
echo "[8] retention enforcement"
OLD="$BACKUP_ROOT/daily/daily-appdb-19990101-000000.dump"
echo "old" > "$OLD"
touch -d "1999-01-01" "$OLD" 2>/dev/null || true
source "$DR_ROOT/lib/common.sh" >/dev/null 2>&1 || true
enforce_retention "$BACKUP_ROOT/daily" 7 "daily-*.dump" >/dev/null 2>&1
check "retention removes backup older than threshold" "[[ ! -f '$OLD' ]]"

# --- 9. restore (stubbed) ---------------------------------------------------------------
echo "[9] restore-db against stubs"
# recreate a clean dump+manifest (retention test may have removed the original)
"$DR_ROOT/bin/db-backup.sh" daily >/dev/null 2>&1 || true
DUMP=$(ls -t "$BACKUP_ROOT/daily/"daily-appdb-*.dump 2>/dev/null | grep -v pre-restore | head -n1)
# pg_restore stub accepts anything; psql stub exits 0 -> restore should pass
OUT=$(PATH="$TEST_ROOT/bin:$PATH" BACKUP_ROOT="$BACKUP_ROOT" \
      "$DR_ROOT/restore/restore-db.sh" --scratch "$DUMP" 2>&1); RC=$?
check "scratch restore exits 0" "[[ $RC == 0 ]]"
check "restore status recorded" "grep -qP $'restore-db\t0\t' '$BACKUP_ROOT/state/status.tsv'"

# restore must refuse a corrupted file
TAMPER="$TEST_ROOT/tampered.dump"
cp "$DUMP" "$TAMPER"; echo "x" >> "$TAMPER"
cp "${DUMP}.sha256" "${TAMPER}.sha256" 2>/dev/null
OUT=$(PATH="$TEST_ROOT/bin:$PATH" BACKUP_ROOT="$BACKUP_ROOT" \
      "$DR_ROOT/restore/restore-db.sh" --scratch "$TAMPER" 2>&1); RC=$?
check "restore refuses checksum-failed dump" "[[ $RC != 0 ]]"

# --- 10. code rollback -------------------------------------------------------------------
echo "[10] code rollback"
TESTREPO="$TEST_ROOT/repo"
git init -q "$TESTREPO" -b main
( cd "$TESTREPO" && echo one > f.txt && git add . && git -c user.email=t@t -c user.name=t commit -qm v1 \
  && echo two > f.txt && git add . && git -c user.email=t@t -c user.name=t commit -qm v2 )
OUT=$("$DR_ROOT/restore/rollback-code.sh" --confirm --to HEAD~1 2>&1) \
  || OUT=$( cd "$TESTREPO" && REPO_DIR="$TESTREPO" "$DR_ROOT/restore/rollback-code.sh" --to HEAD~1 --confirm 2>&1 )
check "rollback restored previous content" "[[ \$(cat '$TESTREPO/f.txt') == one ]]"
check "safety tag created" "[[ -n \"\$(cd '$TESTREPO' && git tag | grep pre-rollback)\" ]]"

# --- summary ------------------------------------------------------------------------------
echo
echo "================ RESULTS: $PASS passed, $FAIL failed ================"
[[ $FAIL -eq 0 ]]
