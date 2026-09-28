# Security policy

## Reporting a vulnerability

Report vulnerabilities privately through GitHub:

1. Open the **Security** tab of the affected repository.
2. Select **Report a vulnerability** to create a private security advisory.
3. Include the affected file or workflow, steps to reproduce and the impact you expect.

## Scope

- Reusable workflows in [gamaware/.github](https://github.com/gamaware/.github) and every repository that calls them.
- Scripts, infrastructure code and pipelines in the portfolio repositories.

Intentionally insecure fixtures in sample deliverables and labs are out of scope. Each repository marks them and
asserts them as expected findings.

## Supported versions

Support covers only the latest commit on `main`. Callers pin reusable workflows by commit SHA, so fixes reach them
through a Dependabot update.
