# Toolchain

Every repository in the portfolio uses these versions unless its README states a deviation. The reusable workflows
pin them; callers pass the same values where the input exists.

| Tool | Version | Pinned in |
| --- | --- | --- |
| Terraform (CI) | 1.14.5 | `terraform.yml` input `terraform-version` |
| Terraform constraint | `>= 1.11.0, < 2.0.0` | `required_version` in each root and module |
| TFLint | 0.64.0 | `terraform.yml` input `tflint-version` |
| TFLint AWS ruleset | 0.49.0 | each repository's `.tflint.hcl` |
| Checkov | 3.3.19 | `security.yml` `CHECKOV_VERSION` and each repository's pre-commit config |
| Semgrep | 1.178.0 | `security.yml` `SEMGREP_IMAGE`, pinned by digest |
| Trivy | 0.74.0 | `security.yml` and `container.yml` `TRIVY_VERSION` |
| gitleaks | 8.30.1 | `secrets.yml` `GITLEAKS_VERSION` |
| actionlint | 1.7.12 | `lint-actions.yml` `ACTIONLINT_VERSION` |
| zizmor | 1.30.1 | `lint-actions.yml` input `zizmor-version` |
| Vale | 3.23.0 | `lint-docs.yml` `VALE_VERSION` |
| hadolint | 2.15.1 | `container.yml` `HADOLINT_VERSION` |
| Helm | 4.3.0 | `helm.yml` input `helm-version` |
| kubeconform | 0.8.0 | `helm.yml` `KUBECONFORM_VERSION` |
| Kubernetes schemas | 1.34.0 | `helm.yml` input `kubernetes-version` |
| pandoc (PDF reports) | 3.11 | `report.yml` `PANDOC_IMAGE` (`pandoc/latex`), pinned by digest |
| Python | 3.13 | `actions/setup-python` in each workflow |
| uv | 0.12.19 | `astral-sh/setup-uv` input `version` in callers |
| pre-commit | 4.6.2 | `ci.yml` and `update-pre-commit-hooks.yml` |

Sample reports build to PDF only through `report.yml`. Each sample commits one `report/REPORT.pdf`; there is no
second PDF engine.

Dependabot bumps `uses:` references only. Update the versions above by hand, in the workflow and in this table in the
same pull request.
