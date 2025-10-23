#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="$ROOT_DIR/venv/bin/python"
if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "Virtual environment not found. Create one with: python3 -m venv venv" >&2
  exit 1
fi

mode="${1:-}"

cd "$ROOT_DIR"

if [[ "$mode" == "--coverage" ]]; then
  COVERAGE_BIN="$ROOT_DIR/venv/bin/coverage"
  if [[ ! -x "$COVERAGE_BIN" ]]; then
    echo "coverage.py not installed; run: $PYTHON_BIN -m pip install coverage" >&2
    exit 1
  fi
  "$COVERAGE_BIN" run --source="$ROOT_DIR/scripts" -m unittest discover -s tests -p 'test_*.py'
  "$COVERAGE_BIN" report -m
else
  "$PYTHON_BIN" -m unittest discover -s tests -p 'test_*.py'
fi
