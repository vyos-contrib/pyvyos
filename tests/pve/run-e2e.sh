#!/usr/bin/env bash
# tests/pve/run-e2e.sh — run the live pyvyos tests against the VM.
#
# Assumes the VM is already running and the HTTPS API is reachable.
# Use start-vm.sh first (and create-vm.sh before that, if needed).

set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=_lib.sh
source "$HERE/_lib.sh"

pve_load_env

REPO_ROOT="$(cd "$HERE/../.." && pwd)"
cd "$REPO_ROOT"

export PYVYOS_E2E=1
export VYDEVICE_HOSTNAME VYDEVICE_PORT VYDEVICE_PROTOCOL
export VYDEVICE_VERIFY_SSL VYDEVICE_APIKEY

hdr "pytest tests/e2e (PYVYOS_E2E=1)"
if command -v uv >/dev/null 2>&1; then
  uv run pytest tests/e2e -v
else
  pytest tests/e2e -v
fi
