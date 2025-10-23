#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INDEX_FILE="$ROOT_DIR/samples/INDEX.md"
VISITOR_SCRIPT="$ROOT_DIR/scripts/yaml_visitor.py"
OUTPUT_ROOT="$ROOT_DIR/output"

if [[ -n "${PYTHON_BIN:-}" ]]; then
  PYTHON_CMD="$PYTHON_BIN"
elif [[ -x "$ROOT_DIR/venv/bin/python" ]]; then
  PYTHON_CMD="$ROOT_DIR/venv/bin/python"
else
  PYTHON_CMD="$(command -v python3)"
fi

if [[ -z "$PYTHON_CMD" ]]; then
  echo "Unable to locate python interpreter. Set PYTHON_BIN environment variable." >&2
  exit 1
fi

if [[ ! -f "$INDEX_FILE" ]]; then
  echo "Index file not found: $INDEX_FILE" >&2
  exit 1
fi

if [[ ! -f "$VISITOR_SCRIPT" ]]; then
  echo "Visitor script not found: $VISITOR_SCRIPT" >&2
  exit 1
fi

trim() {
  local value="$1"
  value="${value#"${value%%[![:space:]]*}"}"
  value="${value%"${value##*[![:space:]]}"}"
  printf '%s' "$value"
}

generate_outputs_for_pair() {
  local schema_rel="$1"
  local model_rel="$2"

  local schema_path="$ROOT_DIR/samples/$schema_rel"
  local model_path="$ROOT_DIR/samples/$model_rel"

  if [[ ! -f "$schema_path" ]]; then
    echo "Skipping (schema missing): $schema_rel" >&2
    return
  fi
  if [[ ! -f "$model_path" ]]; then
    echo "Skipping (model missing): $model_rel" >&2
    return
  fi

  local model_dir
  model_dir="$(dirname "$model_rel")"
  local model_base
  model_base="$(basename "$model_rel" .yaml)"
  local output_dir="$OUTPUT_ROOT/$model_dir"
  mkdir -p "$output_dir"

  for ext in html md; do
    local output_file="$output_dir/${model_base}.${ext}"
    echo "Generating $output_file from $schema_rel + $model_rel"
    "$PYTHON_CMD" "$VISITOR_SCRIPT" "$schema_path" "$model_path" "$output_file" > /dev/null
  done
}

while IFS='|' read -r _ schema_cell model_cell _; do
  schema_cell="$(trim "$schema_cell")"
  model_cell="$(trim "$model_cell")"

  if [[ "$schema_cell" == '' || "$schema_cell" == 'Schema' || "$schema_cell" == '---' ]]; then
    continue
  fi

  schema_rel="${schema_cell//\`/}"
  model_rel="${model_cell//\`/}"

  generate_outputs_for_pair "$schema_rel" "$model_rel"
done < "$INDEX_FILE"

echo "All sample outputs generated under $OUTPUT_ROOT."
