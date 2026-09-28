#!/usr/bin/env bash
# Pre-edit hook: block edits to vendored fonts, their licenses and exported diagrams.
set -euo pipefail

FILE="$(jq -r '.tool_input.file_path // empty')"

case "$FILE" in
    */assets/social-preview/fonts/* | */docs/diagrams/*.svg)
        echo "Blocked: $FILE is vendored or generated. Replace fonts from upstream or re-export the diagram." >&2
        exit 2
        ;;
esac
