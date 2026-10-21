#!/usr/bin/env bash
# Runs the "Lint, template and validate" step of helm.yml against fixture charts.
# Needs helm and yq on PATH; kubeconform is replaced by a stub so the test runs offline.
set -euo pipefail

root="$(cd "$(dirname "$0")/../.." && pwd)"
workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

yq '.jobs.chart.steps[] | select(.name == "Lint, template and validate") | .run' \
  "$root/.github/workflows/helm.yml" >"$workdir/step.sh"
if [ ! -s "$workdir/step.sh" ]; then
  echo "FAIL: step 'Lint, template and validate' not found in helm.yml" >&2
  exit 1
fi

mkdir -p "$workdir/bin"
printf '#!/usr/bin/env bash\ncat >/dev/null\n' >"$workdir/bin/kubeconform"
chmod +x "$workdir/bin/kubeconform"

run_step() {
  CHART="$1" KUBERNETES_VERSION="1.34.0" IGNORE_MISSING_SCHEMAS="false" \
    PATH="$workdir/bin:$PATH" bash "$workdir/step.sh" >"$workdir/out.log" 2>&1
}

# Valid CI values, invalid defaults: the step must check the defaults and fail.
chart="$root/tests/helm/fixtures/defaults-invalid"
if run_step "$chart"; then
  cat "$workdir/out.log" >&2
  echo "FAIL: chart with invalid default values passed" >&2
  exit 1
fi
if ! grep -q '::group::default values' "$workdir/out.log"; then
  cat "$workdir/out.log" >&2
  echo "FAIL: default values were not checked" >&2
  exit 1
fi
echo "ok: invalid default values fail even with ci/*-values.yaml present"

# Same chart with valid defaults: the step checks defaults and every CI values file.
cp -R "$chart" "$workdir/defaults-valid"
printf 'replicaCount: 1\n' >"$workdir/defaults-valid/values.yaml"
if ! run_step "$workdir/defaults-valid"; then
  cat "$workdir/out.log" >&2
  echo "FAIL: chart with valid values failed" >&2
  exit 1
fi
for group in 'default values' 'ci/minimal-values.yaml'; do
  if ! grep -q "::group::.*$group" "$workdir/out.log"; then
    cat "$workdir/out.log" >&2
    echo "FAIL: '$group' was not checked" >&2
    exit 1
  fi
done
echo "ok: valid chart passes with default and CI values"
