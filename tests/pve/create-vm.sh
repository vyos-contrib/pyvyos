#!/usr/bin/env bash
# tests/pve/create-vm.sh — clone the template into a fresh e2e VM.
#
# Refuses to overwrite an existing VMID. Use destroy-vm.sh first if
# the e2e VMID is already taken.

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=_lib.sh
source "$HERE/_lib.sh"

pve_load_env
pve_require_reachable

hdr "Check e2e VMID $VYOS_E2E_VMID is free"
if pve_qm status "$VYOS_E2E_VMID" >/dev/null 2>&1; then
  echo "ERR: VMID $VYOS_E2E_VMID already exists." >&2
  echo "     run tests/pve/destroy-vm.sh first, or pick a different VYOS_E2E_VMID." >&2
  exit 1
fi

hdr "Check template $VYOS_TEMPLATE_VMID exists"
if ! pve_qm config "$VYOS_TEMPLATE_VMID" | grep -q '^template: 1'; then
  echo "ERR: template VMID $VYOS_TEMPLATE_VMID not found." >&2
  echo "     run tests/pve/ensure-template.sh first." >&2
  exit 1
fi

hdr "qm clone $VYOS_TEMPLATE_VMID -> $VYOS_E2E_VMID"
pve_qm clone "$VYOS_TEMPLATE_VMID" "$VYOS_E2E_VMID" \
  --name "$VYOS_E2E_VM_NAME" --full true

hdr "qm set memory/cores/static-ip"
# The template already carries the HTTPS API key (baked by cloud-init
# at template-build time), so this clone does not need another seed.
# We only override the static IP via PVE's ipconfig drive.
pve_qm set "$VYOS_E2E_VMID" \
  --memory "$VYOS_E2E_MEMORY" --cores "$VYOS_E2E_CORES" \
  --ipconfig0 "ip=$VYOS_E2E_IP/$VYOS_E2E_CIDR,gw=$VYOS_E2E_GATEWAY"

echo "ok: VM $VYOS_E2E_VMID created (not started). Next: tests/pve/start-vm.sh" >&2
