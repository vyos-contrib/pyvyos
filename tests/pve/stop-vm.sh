#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=_lib.sh
source "$HERE/_lib.sh"
pve_load_env
pve_require_reachable
hdr "qm shutdown $VYOS_E2E_VMID (60s timeout, then stop)"
pve_ssh "qm shutdown $VYOS_E2E_VMID --timeout 60 || qm stop $VYOS_E2E_VMID"
hdr "ok"
