#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=_lib.sh
source "$HERE/_lib.sh"
pve_load_env
pve_require_reachable
hdr "qm start $VYOS_E2E_VMID"
pve_ssh "qm start $VYOS_E2E_VMID"
hdr "ok"
