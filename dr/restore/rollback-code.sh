#!/usr/bin/env bash
# =============================================================================
# Application code rollback.
#
#   rollback-code.sh [--to <git-ref>] [--confirm]
#
# Without --to, rolls back to the previous commit (HEAD~1).
# Refuses to run without --confirm unless interactive TTY (asks for 'yes').
# Always creates a safety tag and a code snapshot before rolling back.
# =============================================================================
set -euo pipefail

REPO_DIR="${REPO_DIR:-$(pwd)}"
TARGET_REF="HEAD~1"
CONFIRM=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --to)     shift; TARGET_REF="${1:?}" ;;
    --confirm) CONFIRM=1 ;;
    -h|--help) echo "usage: $0 [--to <git-ref>] [--confirm]"; exit 0 ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac
  shift
done

cd "$REPO_DIR"

[[ -d .git ]] || { echo "ERROR: $REPO_DIR is not a git repository" >&2; exit 1; }
git rev-parse --verify -q "$TARGET_REF" >/dev/null \
  || { echo "ERROR: git ref '$TARGET_REF' not found" >&2; exit 1; }

OLD_SHA=$(git rev-parse HEAD)
NEW_SHA=$(git rev-parse "$TARGET_REF")
echo "Rollback plan:"
echo "  repository : $REPO_DIR"
echo "  current    : $OLD_SHA  ($(git log -1 --format=%s "$OLD_SHA"))"
echo "  target     : $NEW_SHA  ($(git log -1 --format=%s "$NEW_SHA"))"
echo

if [[ $CONFIRM -ne 1 ]]; then
  read -r -p "Proceed with rollback? Type 'yes': " ans
  [[ "$ans" == "yes" ]] || { echo "Aborted."; exit 1; }
fi

# 1. safety tag + snapshot so the rollback itself is reversible
SAFETY_TAG="pre-rollback/$(date +%Y%m%d-%H%M%S)"
git tag "$SAFETY_TAG" "$OLD_SHA"
git stash push -u -m "pre-rollback-stash $SAFETY_TAG" >/dev/null 2>&1 || true
echo "Safety tag created: $SAFETY_TAG (restore with: git reset --hard $SAFETY_TAG)"

# 2. rollback working tree to the target ref
git reset --hard "$NEW_SHA"
git clean -fd

# 3. notes
echo
echo "Rollback complete: HEAD is now $NEW_SHA"
echo "  - to undo this rollback : git reset --hard $SAFETY_TAG"
echo "  - to re-apply stashed local changes: git stash pop"
echo
echo "Next steps:"
echo "  1. Verify the application (deploy/smoke tests)"
echo "  2. If a migration was reverted, restore the DB to the matching backup:"
echo "       $DR_PREFIX restore/restore-db.sh --latest daily --force"
echo "  3. Announce the rollback and root cause in the incident channel"
