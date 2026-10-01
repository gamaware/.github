.PHONY: verify vale preview test-helm

# Same command locally and in CI. no-commit-to-branch only guards local commits.
verify:
	SKIP=no-commit-to-branch pre-commit run --all-files --show-diff-on-failure
	@echo "verify: all checks passed"

# Runs the helm.yml lint step against fixture charts. Needs helm and yq.
test-helm:
	tests/helm/test-default-values.sh

vale:
	vale sync
	vale .

preview:
	python3 assets/social-preview/render.py assets/social-preview/examples/github.json assets/social-preview/examples/github.png
