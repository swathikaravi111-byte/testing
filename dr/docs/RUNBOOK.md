# Disaster Recovery Runbook

> Operational, step-by-step procedures for responding to failures.
> Keep a printed/offline copy — during a DR event the wiki may be down.

## Roles

| Role | Responsibility |
|---|---|
| Incident Commander | Declares disaster, coordinates recovery, tracks RTO clock |
| DBA / Ops on-call | Executes database restore, verifies integrity |
| App Lead | Executes code rollback, application smoke tests |
| Comms Lead | Status updates to stakeholders every 30 min |

## Severity Levels

- **SEV-1**: Full data loss / primary site down → invoke this runbook, declare disaster.
- **SEV-2**: Partial data loss (single DB / table corruption) → targeted restore.
- **SEV-3**: Bad deploy, no data loss → code rollback only.

## Scenario A — Full database restore (server loss / corruption)

1. **Declare incident**, note the timestamp (the RTO clock starts).
2. Identify the best backup:
   ```bash
   ls -lt /var/backups/dr/daily /var/backups/dr/weekly /var/backups/dr/monthly
   ```
   Prefer the newest **verified** backup (check `status.tsv` and the newest
   `verify-*.txt` report: `OVERALL: PASS`).
3. Prepare the target server (fresh PostgreSQL instance, matching major version).
4. Restore:
   ```bash
   sudo dr/restore/restore-db.sh --latest daily --force
   # or a specific file:
   sudo dr/restore/restore-db.sh /var/backups/dr/daily/daily-appdb-YYYYMMDD-HHMMSS.dump --force
   ```
   The script verifies the checksum, takes a pre-restore safety backup, recreates
   the DB, restores, and reports the restored table count.
5. Restore roles/tablespaces if the loss included the whole cluster:
   ```bash
   psql -U postgres -f /var/backups/dr/weekly/weekly-globals-*.sql
   ```
6. Validate:
   ```bash
   dr/restore/validate-restore.sh --dump <the dump you used>
   ```
7. Point the application at the restored DB, run smoke tests.
8. Announce recovery, write incident report.

**Data loss expectation:** up to 24h (daily RPO). See RTO/RPO document.

## Scenario B — Corrupt / accidental deletion of specific data

1. Do **not** write to the affected table.
2. Restore the latest good dump into a **scratch** database:
   ```bash
   dr/restore/restore-db.sh --scratch <dumpfile>
   ```
3. Extract the missing rows from scratch and re-insert / merge into production.
4. Drop the scratch DB.

## Scenario C — Bad deployment (no data loss)

1. Roll back code:
   ```bash
   dr/restore/rollback-code.sh --to <previous-tag-or-sha> --confirm
   ```
2. If the deploy ran destructive migrations, also restore the pre-migration
   backup taken by the deploy pipeline, or:
   ```bash
   sudo dr/restore/restore-db.sh --latest daily --force
   ```
3. Run application smoke tests; monitor error rates for 30 min.

## Scenario D — Configuration loss (server rebuilt, nginx/systemd/env lost)

1. Locate the newest config archive:
   ```bash
   ls -lt /var/backups/dr/config/
   ```
2. Restore:
   ```bash
   sha256sum -c config-YYYYMMDD-HHMMSS.tar.gz.sha256   # verify first
   mkdir -p /tmp/cfg && tar -xzf config-YYYYMMDD-HHMMSS.tar.gz -C /tmp/cfg
   sudo cp -a /tmp/cfg/etc/nginx /etc/       # review diffs before overwriting!
   ```
3. Reload affected services (`systemctl reload nginx` etc.).
4. Re-run `dr/bin/config-backup.sh` to snapshot the recovered state.

## Scenario E — Backup system itself failing

Symptoms: `monitor-backups.sh` alerts, verification reports `FAIL`.
1. Do not delete anything — backups are your only recovery path.
2. Check the newest log: `ls -lt /var/backups/dr/logs | head; tail -50 <newest>`.
3. Common causes: disk full (`df -h $BACKUP_ROOT`), DB credentials expired,
   postgres down, offsite rsync key expired.
4. After fixing, force a fresh backup and verify:
   ```bash
   dr/bin/db-backup.sh daily && dr/bin/verify-backup.sh --full
   ```

## Escalation

- Restore fails on primary backups → try weekly, then monthly tier.
- All local backups unusable → restore from offsite replica (`OFFSITE_DEST`).
- Still blocked after 2h → escalate to vendor support; communicate revised RTO.
