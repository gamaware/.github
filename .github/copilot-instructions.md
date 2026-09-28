# Copilot code review instructions

This repository holds reusable GitHub Actions workflows that other repositories call by commit SHA, plus community
health files and a social preview generator. When reviewing pull requests:

- Every `uses:` reference names a full 40-character commit SHA with a version comment.
- Every workflow sets `permissions: {}` at the top level and grants the minimum per job, with a comment for each grant.
- Every job has `timeout-minutes`.
- No `${{ }}` expression appears inside a `run:` block; inputs and event data reach shell steps through `env:`.
- Every downloaded binary passes `sha256sum --check --strict` against a pinned checksum.
- `actions/checkout` uses `persist-credentials: false`.
- Input names, types and defaults in the README table match the workflow files (`docs/workflows.md`).
- No suppressed lint rules, no secrets, no real account IDs, IPs, emails or client names, no dates.
- Conventional commit format in pull request titles.
