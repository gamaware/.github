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
