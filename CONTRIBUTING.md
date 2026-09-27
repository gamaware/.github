# Contributing

These guidelines apply to every public repository under [@gamaware](https://github.com/gamaware) that does not ship
its own `CONTRIBUTING.md`.

## Before you start

- Search open issues and pull requests first.
- For anything larger than a typo or a broken link, open an issue with the suggestion template before writing code.
- Security problems go through private reporting, never a public issue. See [SECURITY.md](SECURITY.md).

## Workflow

1. Fork the repository and create a branch named after the change type, for example `fix/broken-link` or
   `feat/new-check`.
2. Install the hooks once: `pre-commit install --install-hooks` and
   `pre-commit install --hook-type commit-msg`.
3. Make the change and run `make verify`. It runs the same checks as CI.
4. Open a pull request and fill in every section of the template, including the evidence.

## Conventions

- Commit messages and pull request titles follow [Conventional Commits](https://www.conventionalcommits.org/):
  `feat:`, `fix:`, `docs:`, `chore:`, `ci:`, `refactor:`, `test:`.
- Pull requests are squash merged; the title becomes the commit message on `main`.
- Fix lint findings instead of suppressing them. The only accepted exclusions are third-party files whose syntax a
  linter cannot parse.
- Keep content in English, and keep it free of dates, real account IDs, credentials and client names. Fictional data
  uses AWS documentation example account IDs and `example.com` domains.
- Update the README, ADRs and `CHANGELOG.md` in the same pull request when behavior or structure changes.

## Review

Every pull request gets automated reviews plus a review from the code owner. Resolve or answer every comment before
merge. Checks must pass on the latest commit.
