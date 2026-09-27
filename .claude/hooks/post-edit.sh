#!/usr/bin/env bash
# Post-edit hook: auto-format the edited file.
set -euo pipefail

FILE="$(jq -r '.tool_input.file_path // empty')"
if [ "$FILE" = "" ] || [ ! -f "$FILE" ]; then
    exit 0
fi

case "$FILE" in
    *.sh)
        if command -v shellharden > /dev/null 2>&1; then
            shellharden --replace "$FILE" 2> /dev/null || true
        fi
        if head -1 "$FILE" | grep -q '^#!'; then
            chmod +x "$FILE"
        fi
        ;;
    *.md)
        if command -v markdownlint-cli2 > /dev/null 2>&1; then
            markdownlint-cli2 --fix "$FILE" > /dev/null 2>&1 || true
        fi
        ;;
    *.py)
        if command -v ruff > /dev/null 2>&1; then
            ruff format --quiet "$FILE" || true
        fi
        ;;
esac
