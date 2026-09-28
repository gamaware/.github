# 0002. Install scanners as checksum-verified release binaries

## Status

Accepted

## Context

The workflows run gitleaks, Trivy, Vale, actionlint, hadolint and kubeconform. Each project also ships a GitHub
Action wrapper. Wrappers add a second codebase to trust, often fetch the latest tool version at runtime, and some
require extra permissions or licenses. Scanner wrappers have been a real attack path: when a release tag of a popular
scanner action is force-pushed, every workflow that references the tag runs the replaced code.

Pinning the wrapper by SHA fixes the wrapper code but not always the tool binary it downloads.

## Decision

Install these tools directly from their GitHub releases at a fixed version and verify each archive against a SHA-256
checksum stored in the workflow (`sha256sum --check --strict`) before extracting it. Use actions only where they add
setup logic that is hard to reproduce (checkout, setup-terraform, setup-tflint, setup-helm, Buildx, build-push,
markdownlint-cli2, lychee, zizmor, upload-artifact), and pin those by full SHA. Run Semgrep and pandoc from container
images pinned by digest.

## Consequences

- A tampered or replaced release asset fails the install step instead of running.
- Tool versions are explicit and identical across callers.
- Dependabot does not update versions and checksums held in `env:` blocks; they need a manual pull request that
  updates both values from the project's published checksum file.
- The workflows support only Linux x86-64 runners, the platform the checksums cover.
- Python tools (Checkov, pre-commit) install from PyPI pinned by version but not by hash; this decision does not
  cover them.

## Compliance

- Every install step in `.github/workflows/*.yml` pairs a `*_VERSION` with a `*_SHA256` variable and runs
  `sha256sum --check --strict`; reviewers reject install steps without it.
- zizmor flags unpinned `uses:` references, and the container images carry `@sha256:` digests.

## Notes

- Related: [0001](0001-reusable-workflows-pinned-by-sha.md).
