#!/usr/bin/env bash
# pack.sh - create a submission archive for Udacity grader
# Excludes common local artifacts (.venv, chromadb) and includes submission_notes.md

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
OUTFILE="$REPO_ROOT/udaplay-submission.tar.gz"
EXCLUDES=(--exclude='./.venv' --exclude='./chromadb' --exclude='*.pyc' --exclude='__pycache__')

echo "Creating submission archive: $OUTFILE"

tar czf "$OUTFILE" "${EXCLUDES[@]}" -C "$REPO_ROOT" .

echo "Created $OUTFILE"
