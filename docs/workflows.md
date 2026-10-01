# Reusable workflows

Each workflow runs on `workflow_call` only. Job names are the check names callers see;
[`toolchain.md`](toolchain.md) lists the tool versions.

| Workflow | Jobs (check names) | Inputs (type, default) |
| --- | --- | --- |
| `lint-docs.yml` | `markdownlint`, `links`, `vale` | `markdown-globs` (string, `**/*.md` + `#node_modules`), `run-links` (bool, true), `lychee-args` (string, `--no-progress --max-retries 3 --accept 200..=299,403,429 --exclude-path node_modules './**/*.md'`), `run-vale` (bool, true), `vale-paths` (string, `.`) |
| `lint-actions.yml` | `actionlint`, `zizmor` | `zizmor-persona` (string, `regular`), `zizmor-min-severity` (string, `low`), `zizmor-version` (string, `1.30.1`) |
| `secrets.yml` | `gitleaks` | `scan-history` (bool, true), `gitleaks-config` (string, empty: `.gitleaks.toml` if present) |
| `security.yml` | `semgrep`, `trivy`, `checkov` | `run-semgrep` (bool, true), `semgrep-config` (string, `p/default`), `run-trivy` (bool, true), `trivy-severity` (string, `HIGH,CRITICAL`), `trivy-skip-dirs` (string, empty), `run-checkov` (bool, true), `checkov-config` (string, `.checkov.yaml`) |
| `terraform.yml` | `fmt`, `validate (<dir>)` | `working-directories` (JSON array string, `["."]`), `terraform-version` (string, `1.14.5`), `tflint-version` (string, `v0.64.0`), `run-tests` (bool, true) |
| `container.yml` | `hadolint`, `build-scan` | `context` (string, `.`), `dockerfile` (string, `Dockerfile`), `image-name` (string, `app`), `trivy-severity` (string, `HIGH,CRITICAL`), `trivy-ignore-unfixed` (bool, true) |
| `helm.yml` | `chart (<dir>)` | `charts` (JSON array string, `["charts"]`), `helm-version` (string, `v4.3.0`), `kubernetes-version` (string, `1.34.0`), `ignore-missing-schemas` (bool, false) |
| `report.yml` | `pdf`, `evidence` | `report-path` (string, `report/REPORT.md`), `pandoc-args` (string, `--pdf-engine=xelatex -V geometry:margin=2.2cm --toc`), `artifact-name` (string, `report-pdf`), `evidence-command` (string, empty skips), `evidence-path` (string, `evidence`), `python-version` (string, `3.13`) |

Behavior worth knowing before calling them:

- `lint-docs` reads the caller's `.markdownlint.yaml` and `.vale.ini`; `run-vale: true` fails when `.vale.ini` is
  missing.
- `security` runs Checkov with `--config-file` when `checkov-config` exists and scans the `directory` or `file` it
  sets; a config that sets neither gets `--directory .`. Without a config, Checkov scans the whole repository.
  Trivy honors the caller's `.trivyignore`. Declare intentional fixtures there or in the Checkov config; never skip
  them wholesale.
- `terraform` runs `init -backend=false`, so it never needs cloud credentials. `terraform test` runs only in
  directories with `*.tftest.hcl` files; use mock providers for them. TFLint reads `.tflint.hcl` from the root.
- `container` builds with `load: true` and never pushes. Hadolint reads the caller's `.hadolint.yaml`.
- `helm` adds the HTTP repositories listed under `dependencies` in `Chart.yaml`, builds dependencies, then lints and
  renders each chart once with its default values and once per `ci/*-values.yaml` file for `kubernetes-version`, and
  validates the output with kubeconform in strict mode.
- `report` builds the PDF with the `pandoc/latex` image pinned by digest and uploads it as an artifact. With
  `evidence-command` set, it reruns that command and fails if `evidence-path` differs from the commit.

## Call a workflow from another repository

Reference a full commit SHA of this repository, never a branch or a bare tag, and grant only `contents: read`:

```yaml
name: ci

on:
  pull_request:
  push:
    branches: [main]

permissions: {}

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint-docs:
    uses: gamaware/.github/.github/workflows/lint-docs.yml@<full-40-character-sha> # v1.0.0
    permissions:
      contents: read

  secrets:
    uses: gamaware/.github/.github/workflows/secrets.yml@<full-40-character-sha> # v1.0.0
    permissions:
      contents: read

  terraform:
    uses: gamaware/.github/.github/workflows/terraform.yml@<full-40-character-sha> # v1.0.0
    permissions:
      contents: read
    with:
      working-directories: '["modules/network", "envs/dev"]'
```

Pin the commit of a release tag and keep the tag as a trailing comment. Find the SHA with
`git ls-remote https://github.com/gamaware/.github 'refs/tags/v1.0.0*'`: for an annotated tag use the `^{}` line,
which names the commit; a lightweight tag has only the plain line. Dependabot's `github-actions` ecosystem
reads the comment and bumps both the SHA and the comment when a new tag appears. Keep caller job keys stable
(`lint-docs`, `lint-actions`, `secrets`, `security`, `terraform`, `container`, `helm`, `report`) so required check
names such as `lint-docs / markdownlint` are identical across repositories.

Do not pass `secrets: inherit`; none of these workflows needs a secret.

## Maintainer setup

- Create the `automation` environment with deployment branches limited to `main`, and store `PRE_COMMIT_PAT` there
  as a fine-grained token scoped to this repository with contents and pull request write access only.
- Tag releases as `vX.Y.Z` on `main`; callers pin the tag's commit SHA.
