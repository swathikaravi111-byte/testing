# Backup & Disaster Recovery System

Comprehensive backup, verification, and disaster-recovery tooling for
PostgreSQL databases, application configuration, and application code.

## Layout

```
dr/
├── lib/common.sh              # shared library: logging, locking, manifests, alerts, retention
├── config/backup.conf         # all tunables (DB connection, sources, retention, alerts)
├── bin/
│   ├── db-backup.sh           # daily|weekly|monthly database dumps
│   ├── config-backup.sh       # config tree snapshots (tarball + checksum)
│   ├── verify-backup.sh       # 3-layer verification: checksums, structure, age
│   ├── monitor-backups.sh     # failure/staleness alerting
│   └── health-check.sh        # human-readable status summary
├── restore/
│   ├── restore-db.sh          # safe DB restore (scratch/overwrite, checksum-gated)
│   ├── validate-restore.sh    # live restore drill + row-level validation
│   └── rollback-code.sh       # reversible git rollback with safety tags
├── cron.d/dr-backups          # full schedule
├── tests/run-tests.sh        # self-contained test suite (25 checks, no real DB needed)
└── docs/
    ├── MASTER-DR-PLAN.md      # master disaster recovery plan
    ├── RUNBOOK.md             # step-by-step incident procedures
    ├── ROLLBACK-PROCEDURES.md # DB & code rollback (incl. undoing a rollback)
    └── RTO-RPO.md             # recovery objectives & budget breakdown
```

## Quick start

1. Edit `config/backup.conf` (DB credentials, config sources, alert channels).
2. Install the schedule: `cp dr/cron.d/dr-backups /etc/cron.d/` (adjust paths/user).
3. Test: `dr/tests/run-tests.sh` — exercises the whole pipeline with stubbed binaries.
4. Verify manually at any time: `dr/bin/verify-backup.sh --full`.

## Objectives

| Tier | RPO | RTO |
|---|---|---|
| Daily | 24 h | 4 h |
| Weekly | 7 d | 8 h |
| Monthly | 31 d | 24 h |

See `docs/RTO-RPO.md` for the full budget breakdown and drill requirements.
