# Rollback Procedures

## Database rollback

### When to roll back the database
- Corrupt schema/data introduced by a failed migration
- Accidental `DELETE`/`UPDATE`/`TRUNCATE` without transaction
- Ransomware / tampering detected

### Procedure

1. **Stop writes** to prevent further damage (put app in maintenance mode).
2. Identify the last known-good backup (newest `OVERALL: PASS` verification report).
3. Take a safety dump of the current (damaged) state for forensics:
   ```bash
   pg_dump -U postgres -Fc appdb > /var/backups/dr/daily/damaged-$(date +%s).dump
   ```
4. Run the restore:
   ```bash
   sudo dr/restore/restore-db.sh --latest daily --force
   ```
   The script itself also takes a pre-restore safety backup
   (`pre-restore-*.dump`) before touching the target database.
5. Validate row counts with `dr/restore/validate-restore.sh`.
6. Resume writes, monitor error rates.

### Roll back the rollback
The restore never destroys data silently: the previous database state is kept
in `daily/pre-restore-<db>-<timestamp>.dump`. To undo a restore:
```bash
sudo dr/restore/restore-db.sh /var/backups/dr/daily/pre-restore-appdb-YYYYMMDD-HHMMSS.dump --force
```

### Point-in-time recovery (if WAL archiving is enabled)
```bash
# 1. restore base backup
# 2. create recovery.signal and set restore_command in postgresql.auto.conf
restore_command = 'cp /var/backups/dr/wal/%f %p'
recovery_target_time = 'YYYY-MM-DD HH:MM:SS'
# 3. start postgres; it replays WAL to the target moment
```

## Code rollback

### Preconditions
- Deployments are git-tagged (deploy pipeline must tag every release).
- Application changes are backward compatible with at least one schema version
  (expand/contract pattern) so code rollback rarely forces a DB rollback.

### Procedure
```bash
# roll back to the previous release
dr/restore/rollback-code.sh --confirm

# or to a specific tag
dr/restore/rollback-code.sh --to release/2025-01-15 --confirm
```

The script:
1. Creates a `pre-rollback/<timestamp>` git tag at the current HEAD.
2. Stashes any local uncommitted changes.
3. `git reset --hard <target>` + `git clean -fd`.
4. Prints the exact undo command.

### Undo a code rollback
```bash
git reset --hard pre-rollback/<timestamp>
git stash pop   # if local changes were stashed
```

## Combined rollback (bad deploy + bad migration)

Order matters:

1. **Code first** (`rollback-code.sh`) so the running app matches the old schema expectations.
2. **Then database** (`restore-db.sh --latest daily --force`) to the last pre-migration backup.
3. Re-run application migrations as needed — the old code must find a compatible schema.
4. Full smoke test before re-opening traffic.

## Decision matrix

| Situation | Rollback type | Command |
|---|---|---|
| Bad code, compatible schema | Code only | `rollback-code.sh --confirm` |
| Bad migration, code fine | DB only | `restore-db.sh --latest daily --force` |
| Bad deploy with destructive migration | Both (code → DB) | both scripts |
| Data corruption only | Targeted scratch restore | `restore-db.sh --scratch <dump>` |
