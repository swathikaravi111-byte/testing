# Master Disaster Recovery Plan

Version 1.0 · Owner: Platform/DevOps Team · Review cadence: quarterly

## 1. Purpose & Scope

This plan covers backup, verification, and recovery for:
- **Databases** (PostgreSQL; MySQL supported by the dump tooling)
- **Application configuration** (nginx, systemd units, environment files, DR config)
- **Application code** (git-based rollback and re-deploy)

Out of scope: end-user device recovery, third-party SaaS internal failures.

## 2. Objectives

| Objective | Target | Source of truth |
|---|---|---|
| Recovery Point Objective (data loss) | 24 h daily / 7 d weekly / 31 d monthly | [RTO-RPO.md](RTO-RPO.md) |
| Recovery Time Objective | 4 h (SEV-1, daily tier) | [RTO-RPO.md](RTO-RPO.md) |

## 3. System architecture

```
                 ┌────────────── cron (dr/cron.d/dr-backups) ──────────────┐
                 │ 01:00 daily DB dump      01:30 config snapshot         │
                 │ 02:00 Sun weekly full    03:00 1st monthly archive     │
                 │ 04:00 verify-backup.sh   05:00 Sun restore drill      │
                 │ */15 monitor-backups.sh   6h  health-check.sh          │
                 └───────────────────────────────────────────────────────┘
                                        │
  pg_dump / tar  ──►  /var/backups/dr/  ├── daily/  (retained 7 d)
                       ├── weekly/  (retained 5)
                       ├── monthly/ (retained 12)
                       ├── config/  (retained 30 d)
                       ├── verify/  (verification reports)
                       ├── logs/    ├── state/ (status.tsv, alerts.log)
                       └── (optional) rsync offsite replica
```

Components (`dr/` directory):

| Path | Purpose |
|---|---|
| `lib/common.sh` | Shared library: logging, locking, manifests, alerts, retention |
| `config/backup.conf` | All tunables (DB conn, sources, retention, webhook/email) |
| `bin/db-backup.sh` | `daily\|weekly\|monthly` database dumps |
| `bin/config-backup.sh` | Config tree snapshots |
| `bin/verify-backup.sh` | Layered verification (checksums, structure, age, optional live restore) |
| `bin/monitor-backups.sh` | Alert on failures & stale jobs |
| `bin/health-check.sh` | Human-readable status summary |
| `restore/restore-db.sh` | Safe DB restore (scratch or overwrite, checksum-gated) |
| `restore/validate-restore.sh` | Live restore + row-level validation into scratch DB |
| `restore/rollback-code.sh` | Safe, reversible git rollback with safety tags |
| `cron.d/dr-backups` | Full schedule |
| `docs/` | This plan, runbook, rollback procedures, RTO/RPO |

## 4. Backup strategy

### Database (3-2-1 inspired: 3 copies, 2 media, 1 offsite)

| Level | When | Contents | Retention |
|---|---|---|---|
| Daily | 01:00 | `pg_dump --format=custom` per DB + globals + SHA-256 manifest | 7 days |
| Weekly | Sun 02:00 | Full dump + `pg_dumpall --globals-only` | 5 weeks |
| Monthly | 1st 03:00 | Full dump, long-term archive | 12 months |
| Offsite | after each job | rsync to `OFFSITE_DEST` (optional, recommended) | mirror |

Every backup gets a `.sha256` manifest at write time; verification is
checksum-gated — a restore refuses to run on a file that fails verification.

### Configuration
- Daily 01:30 tarball of `CONFIG_SOURCES` (nginx, systemd, `.env`, DR config)
- Checksum manifest, 30-day retention, instant single-file recovery.

### Code
- Git is the source of truth; deploy pipeline tags every release.
- `rollback-code.sh` performs reversible rollbacks (safety tag + stash).

## 5. Backup integrity testing (automated)

Three layers, all automated via cron:

1. **Checksum layer (daily 04:00)** — `sha256sum -c` on every backup manifest.
2. **Structural layer (daily 04:00)** — `pg_restore --list` proves the dump is
   parseable and contains table data; gzip validation of config archives;
   **age checks** enforce the RPO (daily must be < 1 day old, etc.).
3. **Live-restore layer (Sunday 05:00 and `--full`)** —
   `validate-restore.sh` restores the newest daily dump into a scratch
   database, counts rows per table, executes sample queries, then drops the
   scratch DB. A backup is only trusted after it passes this drill.

Verification reports live in `/var/backups/dr/verify/verify-*.txt`
(`OVERALL: PASS/FAIL`), status history in `state/status.tsv`.

## 6. Monitoring & alerting

`monitor-backups.sh` runs every 15 minutes and alerts on:
- any job whose last recorded exit code ≠ 0 (**CRITICAL**)
- any job whose last success is older than its threshold (daily jobs: 26 h) (**CRITICAL**)
- config sources silently missing (**WARNING**)
- offsite replication failure (**WARNING**)

Delivery channels (configured in `config/backup.conf`):
- webhook (Slack-compatible JSON) via `ALERT_WEBHOOK_URL`
- email via `ALERT_EMAIL`
- local `state/alerts.log` (always)

## 7. Recovery procedures (summary)

Full step-by-step procedures are in [RUNBOOK.md](RUNBOOK.md):

| Disaster | Procedure | Key command |
|---|---|---|
| DB loss/corruption | Runbook A | `restore/restore-db.sh --latest daily --force` |
| Partial data loss | Runbook B (targeted scratch) | `restore/restore-db.sh --scratch <dump>` |
| Bad deploy | Runbook C | `restore/rollback-code.sh --to <ref> --confirm` |
| Config loss | Runbook D | extract config tarball + reload services |
| Backup system failure | Runbook E | fix cause → `db-backup.sh daily && verify-backup.sh --full` |

Rollback specifics (incl. undoing a rollback): [ROLLBACK-PROCEDURES.md](ROLLBACK-PROCEDURES.md)

## 8. Restore validation as a requirement

A backup is **not considered valid** until:
1. Its checksum manifest verifies, **and**
2. `verify-backup.sh` reported `OVERALL: PASS`, **and**
3. (for drill-tested backups) `validate-restore.sh` completed a live restore
   with non-zero table counts.

Restores in production must always be followed by `validate-restore.sh` and
application smoke tests before reopening traffic.

## 9. Roles, contact & escalation

See RUNBOOK.md §Roles. Escalation ladder:
on-call → team lead → vendor support → executive comms.
RTO breach at +2 h triggers stakeholder notification with revised ETA.

## 10. Drills & maintenance

| Activity | Cadence |
|---|---|
| Automated live-restore drill | Weekly (Sunday 05:00, automated) |
| Full tabletop DR exercise (runbook by hand, timed) | Quarterly |
| Restore-time measurement vs RTO | Quarterly |
| Review of this plan + retention settings | Quarterly |
| Offsite restore test from offsite copy | Semi-annually |

## 11. Installation & operations

```bash
# one-time setup (on the backup host)
chmod +x dr/bin/*.sh dr/restore/*.sh
cp dr/cron.d/dr-backups /etc/cron.d/dr-backups     # adjust paths/user
edit dr/config/backup.conf                          # DB creds, sources, alert channels

# day-to-day operations
dr/bin/health-check.sh                              # status summary
tail /var/backups/dr/state/alerts.log               # recent alerts
dr/bin/verify-backup.sh --full                      # on-demand full verification
```

## 12. Risks & assumptions

- Assumption: backup host is separate from the DB host, or at least offsite
  replication is enabled — otherwise a single-site failure destroys all backups.
- Risk: DB major-version drift between backup and restore host. Mitigation:
  record the postgres version inside `status.tsv` entries and match during DR.
- Risk: credentials in `backup.conf`. Mitigation: file permissions `0600`,
  never commit real secrets (repo copy contains placeholders only).
- Risk: WAL archiving not enabled → 24 h data loss is unavoidable. Accept or
  enable PITR per RTO-RPO.md.
