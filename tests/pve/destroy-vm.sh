#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=_lib.sh
source "$HERE/_lib.sh"
pve_load_env
pve_require_reachable
hdr "Destroy VM $VYOS_E2E_VMID (purge disks)"
pve_ssh "qm status $VYOS_E2E_VMID >/dev/null 2>&1 || { echo 'not present, nothing to do'; exit 0; }"
pve_ssh "qm stop $VYOS_E2E_VMID || true"
pve_ssh "qm destroy $VYOS_E2E_VMID --purge"
hdr "ok"
