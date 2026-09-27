# 0001. Share CI through reusable workflows pinned by commit SHA

## Status

Accepted

## Context

About a dozen portfolio repositories need the same documentation, workflow, secret and security checks, and many
share a stack (Terraform, containers, Helm, generated reports). Copying workflow files into each repository lets them
drift: versions diverge, one repository loses a hardening setting, and required check names stop matching. GitHub
offers two sharing mechanisms: composite actions (steps inside the caller's job) and reusable workflows (whole jobs
with their own runners, permissions and timeouts).

A reference to shared CI code is also a supply-chain entry point. A branch or tag reference can move after review; a
full commit SHA cannot.

## Decision

Publish the shared checks as reusable workflows (`on: workflow_call`) in `gamaware/.github`, one file per concern:
`lint-docs`, `lint-actions`, `secrets`, `security`, `terraform`, `container`, `helm` and `report`. Each exposes typed
inputs with safe defaults. Callers reference them by full commit SHA with the release tag as a trailing comment, grant
`contents: read` and pass no secrets.

## Consequences

- One fix or version bump reaches every repository through a Dependabot pull request that the caller still reviews.
- Check names are identical across repositories (`<caller job> / <job>`), so the same branch protection settings
  apply everywhere.
- Jobs defined here decide their own permissions and timeouts; a caller cannot widen them without forking the file.
- Callers depend on this repository staying public and on its tags; a breaking input change needs a new major tag.
- A caller cannot add extra steps to a job that a reusable workflow defines. Repository-specific steps go in separate
  caller jobs.

## Compliance

- `lint-actions` runs zizmor with the `unpinned-uses` audit in every caller; a branch or tag reference fails it.
- `make verify` in this repository runs actionlint and zizmor (pedantic) on every workflow before merge.
- Reviewers check that caller jobs grant only `contents: read` and never use `secrets: inherit`.

## Notes

- Related: [0002](0002-checksum-verified-tool-binaries.md).
