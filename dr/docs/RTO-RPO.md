# Recovery Time & Recovery Point Objectives

## Definitions

- **RPO (Recovery Point Objective)** — maximum tolerable data loss, measured in
  time between the last good backup and the failure.
- **RTO (Recovery Time Objective)** — maximum tolerable time from disaster
  declaration to service restoration.

## Objectives per tier

| Tier | Backup cadence | RPO | RTO | Basis |
|---|---|---|---|---|
| Daily (hot) | 01:00 every day | **24 h** | **4 h** | Nightly dump; fastest restore |
| Weekly (warm) | Sunday 02:00 | **7 d** | 8 h | Weekly full + globals |
| Monthly (cold) | 1st of month | **31 d** | 24 h | Long-term archive |
| Config | Daily | **24 h** | 1 h | Small tarballs, instant restore |
| Offsite replica | After each job | 24 h (+transfer lag) | +2 h shipping time | Worst case when local backups lost |

## RTO budget breakdown (SEV-1, daily tier)

| Step | Target | Notes |
|---|---|---|
| Detect & declare | 30 min | Monitoring `monitor-backups.sh` + app alerts |
| Provision/prepare host | 30 min | Spare/rebuilt VM, postgres installed |
| Select & verify backup | 15 min | Checksums + latest PASS report |
| Restore database | 2 h | `restore-db.sh --latest daily --force` |
| Restore config | 15 min | Config archive + service reloads |
| Application deploy + smoke tests | 30 min | Standard pipeline |
| **Total** | **≤ 4 h** | |

## RPO justification

- Backups run at 01:00; verification at 04:00 confirms restorability daily.
- Worst-case loss window = 24 h minus time-of-failure.
- If sub-hour RPO is required for specific tables, enable PostgreSQL WAL
  archiving + point-in-time recovery (see Rollback Procedures) or streaming
  replication to a standby — targets **~5 min RPO**.

## Verification of objectives

- **RPO proof**: every backup timestamped + age-checked by `verify-backup.sh`
  (daily backup must be ≤ 1 day old or a CRITICAL alert fires).
- **RTO proof**: weekly live restore drill (`validate-restore.sh` via cron)
  measures actual restore duration; the runbook drill should be executed
  quarterly with the clock recorded in the drill report.

## Escalation thresholds

| Elapsed | Action |
|---|---|
| > 2 h without a working restore path | Escalate to vendor, notify stakeholders of revised RTO |
| > 4 h (RTO exceeded) | Comms must state new ETA; IC re-plans from weekly tier |
| > 24 h | Full DR invocation from offsite replica |
