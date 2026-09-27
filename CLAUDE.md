# CLAUDE.md

## Overview

`gamaware/.github` is the shared repository for the AWS DevOps portfolio. It provides:

- Community health files (`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORT.md`, `SECURITY.md`, issue forms, pull
  request template) that GitHub applies to every repository without its own copy.
- Reusable workflows in `.github/workflows/` (`lint-docs`, `lint-actions`, `secrets`, `security`, `terraform`,
  `container`, `helm`, `report`) that other repositories call by commit SHA.
- The social preview generator in `assets/social-preview/`.

It is not a profile repository; do not add `profile/README.md`.

## Structure

- `.github/workflows/*.yml`: reusable workflows (`on: workflow_call`) plus this repository's own `ci.yml`,
  `scorecard.yml` and `update-pre-commit-hooks.yml`.
- `assets/social-preview/`: `render.py` (standard library only), vendored OFL fonts, example spec and output.
- `docs/adr/`: decisions in the FoSA2 format with a Compliance section. `docs/diagrams/`: Mermaid source plus SVG.

## Workflow rules

- `permissions: {}` at workflow level; per-job grants with a comment explaining each one.
- Every `uses:` pinned by full commit SHA with a `# vX.Y.Z` comment. Resolve SHAs with
  `git ls-remote https://github.com/<owner>/<repo> 'refs/tags/<tag>^{}'`.
- Tool binaries install from GitHub releases with a `*_VERSION` and `*_SHA256` pair and
  `sha256sum --check --strict`. Update both from the project's published checksum file.
- `timeout-minutes` on every job; `persist-credentials: false` on every checkout.
- No `${{ }}` inside `run:`; pass inputs through `env:` and split lists with `read -ra`.
- No concurrency groups inside reusable workflows: they would use the caller's workflow name and cancel sibling
  calls. Callers set concurrency.
- Keep job names stable; they are the required check names in every caller.
- Any input change updates the README inputs table and `CHANGELOG.md` in the same pull request.

## Git workflow

- Conventional commits; feature branches; squash merge; never commit to `main`.
- Release by tagging `vX.Y.Z` on `main`; callers pin the tag's commit SHA.

## Pre-commit and verification

`make verify` runs `pre-commit run --all-files` with `no-commit-to-branch` skipped, the same command CI runs. Hooks:
pre-commit-hooks, detect-secrets (`.secrets.baseline`), gitleaks, markdownlint-cli2, yamllint, actionlint, zizmor
(pedantic), shellcheck, shellharden, ruff, conventional-pre-commit. `make vale` runs the prose check.

## Claude Code hooks

- `.claude/hooks/post-edit.sh`: formats `.sh` (shellharden), `.md` (markdownlint-cli2) and `.py` (ruff) after edits.
- `.claude/hooks/protect-vendored.sh`: blocks edits to vendored fonts and exported diagram SVGs.

## Linting

Markdown line length 120 with tables exempt. Fix violations; never suppress them.

## CI and code review

`ci.yml` calls this repository's own `lint-actions` (pedantic), `lint-docs` and `secrets` workflows through local
references and runs `make verify`. CodeRabbit (`.coderabbit.yaml`) and Copilot (`.github/copilot-instructions.md`)
review every pull request.

## Content rules

English only, dateless, no AI mentions, no real account IDs, ARNs, IPs, emails or client names.
