#!/usr/bin/env bash
# tests/pve/preflight.sh — read-only sanity check on the PVE host.
#
# Verifies the host is reachable, has the tools the other scripts use,
# and reports the current state of the template VMID and the e2e VMID
# so you know whether ensure-template.sh / create-vm.sh have work to
# do. Mutates nothing.

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=_lib.sh
source "$HERE/_lib.sh"

pve_load_env
pve_require_reachable

hdr "PVE identity"
pve_ssh 'hostname; pveversion'

hdr "Required tools (qm, pvesm, ip, curl, sha256sum)"
pve_ssh 'for c in qm pvesm ip curl sha256sum; do
  if command -v "$c" >/dev/null 2>&1; then
    printf "  ok      %s\n" "$c"
  else
    printf "  MISSING %s\n" "$c"
  fi
done'

hdr "Storage and bridge"
pve_ssh "pvesm status; ip -br link show $PVE_BRIDGE 2>/dev/null || echo 'bridge $PVE_BRIDGE not found'"

hdr "Image directory"
pve_ssh "ls -la $PVE_IMAGE_DIR 2>/dev/null | head -20 || echo 'directory missing: $PVE_IMAGE_DIR'"

hdr "Template VMID $VYOS_TEMPLATE_VMID"
pve_ssh "qm status $VYOS_TEMPLATE_VMID 2>/dev/null \
  && qm config $VYOS_TEMPLATE_VMID | grep -E '^(name|template|ostype|net0):' \
  || echo 'template VMID $VYOS_TEMPLATE_VMID does not exist (ensure-template.sh will create it)'"

hdr "e2e VMID $VYOS_E2E_VMID"
pve_ssh "qm status $VYOS_E2E_VMID 2>/dev/null \
  || echo 'e2e VMID $VYOS_E2E_VMID is free (create-vm.sh will clone it)'"

hdr "ok"
