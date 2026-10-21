# Changelog

This file records all notable changes to this repository. The format follows
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/). Callers pin release tags by commit SHA.

## [Unreleased]

### Added

- Community health files: contributing guide, Contributor Covenant 2.1, support, security policy, issue forms and a
  pull request template.
- Reusable workflows: `lint-docs`, `lint-actions`, `secrets`, `security`, `terraform`, `container`, `helm` and
  `report`.
- Social preview generator for 1280x640 previews with vendored OFL fonts.
- Repository CI (actionlint, zizmor, markdownlint, lychee, Vale, gitleaks, `make verify`), OpenSSF Scorecard and a
  weekly pre-commit hook update.
- Toolchain table (`docs/toolchain.md`) with the tool versions every portfolio repository uses.

### Fixed

- `helm`: charts with `ci/*-values.yaml` files are also linted and validated with their default values, so a chart
  whose own `values.yaml` breaks fails the check. `make test-helm` and the `test-helm` CI job cover it with a fixture
  chart.
- `report`: the evidence check compares against `HEAD`, so evidence the command staged still fails the check.
- `security`: a Checkov config file with no `directory` or `file` key scans the repository instead of nothing.
- `terraform`: `terraform test` runs when test files exist where Terraform loads them (the root or `tests/`).
- Social preview generator: renders to a temporary file with a timeout and replaces the output only on success.
