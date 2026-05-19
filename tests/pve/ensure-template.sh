#!/usr/bin/env bash
# tests/pve/ensure-template.sh — idempotently build the VyOS template.
#
# State machine on $VYOS_TEMPLATE_VMID:
#
#   template -> nothing to do; exit 0.
#
#   missing  -> phase 1:
#               qm create with the install ISO + seed CD + empty disk,
#               boot, print operator instructions, exit 0.
#               You then open the serial console, run `install image`,
#               poweroff, and rerun this script.
#
#   running  -> phase 1 still in progress; print instructions, exit 1.
#
#   stopped  -> phase 2:
#               swap boot order to the installed disk, start, wait for
#               cloud-init to apply the seed (vyos_config_commands sets
#               the HTTPS API key), shutdown, detach the install ISO
#               and the seed, qm template.

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=_lib.sh
source "$HERE/_lib.sh"

pve_load_env
pve_require_reachable

VYOS_CLOUD_INIT_WAIT_SECONDS="${VYOS_CLOUD_INIT_WAIT_SECONDS:-120}"

SEED_ISO_REMOTE="$PVE_IMAGE_DIR/${VYOS_TEMPLATE_NAME}-seed.iso"

render_and_upload_seed() {
  # Generates the NoCloud seed ISO on the PVE host itself. Avoids
  # requiring genisoimage/mkisofs on the workstation, and keeps the
  # rendered API key off the local filesystem.
  hdr "Render and build seed ISO on PVE host"
  pve_ssh "command -v genisoimage >/dev/null 2>&1 || command -v mkisofs >/dev/null 2>&1 || {
    echo 'ERR: PVE host has neither genisoimage nor mkisofs. apt install genisoimage' >&2
    exit 1
  }"

  local user_data meta_data
  user_data="$(sed -e "s|__APIKEY__|$VYDEVICE_APIKEY|g" \
                   -e "s|__HOSTNAME__|$VYOS_TEMPLATE_NAME|g" \
                   "$HERE/cloud-init/user-data.template")"
  meta_data="$(sed -e "s|__INSTANCE_ID__|$VYOS_TEMPLATE_NAME-$(date +%s)|g" \
                   -e "s|__HOSTNAME__|$VYOS_TEMPLATE_NAME|g" \
                   "$HERE/cloud-init/meta-data.template")"

  pve_ssh "set -e
    tmp=\$(mktemp -d)
    trap 'rm -rf \$tmp' EXIT
    cat > \$tmp/user-data <<'PYVYOS_USERDATA_EOF'
$user_data
PYVYOS_USERDATA_EOF
    cat > \$tmp/meta-data <<'PYVYOS_METADATA_EOF'
$meta_data
PYVYOS_METADATA_EOF
    if command -v genisoimage >/dev/null 2>&1; then
      genisoimage -output '$SEED_ISO_REMOTE' -volid cidata -joliet -rock \
                  \$tmp/user-data \$tmp/meta-data >/dev/null 2>&1
    else
      mkisofs -output '$SEED_ISO_REMOTE' -volid cidata -joliet -rock \
              \$tmp/user-data \$tmp/meta-data >/dev/null 2>&1
    fi
  "
  echo "seed ISO at $SEED_ISO_REMOTE" >&2
}

phase1_create_install_vm() {
  hdr "Phase 1: create VM with install ISO and seed"

  if ! pve_ssh "test -s '$VYOS_ISO_PATH'"; then
    echo "ERR: VyOS install ISO not found on PVE host at $VYOS_ISO_PATH" >&2
    echo "     download a rolling build from $VYOS_IMAGE_URL" >&2
    echo "     and place it at that path, or update VYOS_ISO_PATH." >&2
    return 1
  fi

  render_and_upload_seed

  pve_qm create "$VYOS_TEMPLATE_VMID" \
    --name "$VYOS_TEMPLATE_NAME" \
    --memory 1024 --cores 1 \
    --net0 "virtio,bridge=$PVE_BRIDGE" \
    --serial0 socket --vga serial0 \
    --scsihw virtio-scsi-pci \
    --ostype l26 \
    --agent enabled=1

  # 4G disk is plenty for a router appliance.
  pve_qm set "$VYOS_TEMPLATE_VMID" --scsi0 "$PVE_STORAGE:4"

  # ide2 = install ISO (boot here first). ide3 = NoCloud seed.
  pve_qm set "$VYOS_TEMPLATE_VMID" \
    --ide2 "$VYOS_ISO_PATH,media=cdrom" \
    --ide3 "$SEED_ISO_REMOTE,media=cdrom" \
    --boot "order=ide2;scsi0"

  pve_qm start "$VYOS_TEMPLATE_VMID"

  cat >&2 <<EOF

VyOS install VM started. Finish the install manually:

  on the PVE host:
    qm terminal $VYOS_TEMPLATE_VMID            # press Ctrl-] to exit

  inside VyOS:
    login: vyos / vyos
    install image
      (accept defaults; set the new password to whatever you want)
    poweroff

When the VM is powered off, re-run this script to finalize the template.
EOF
}

phase2_finalize_template() {
  hdr "Phase 2: boot installed disk, let cloud-init apply seed, template"

  # Boot from installed disk now (install ISO no longer needed) and
  # keep the seed CD so cloud-init picks it up on first post-install
  # boot. We do NOT detach the install ISO yet; some VyOS rolling
  # builds re-trigger first-boot wizardry from the CD if removed
  # before the installed system has fully run. We detach both at the
  # end, atomically, just before flipping the template flag.
  pve_qm set "$VYOS_TEMPLATE_VMID" --boot "order=scsi0"
  pve_qm start "$VYOS_TEMPLATE_VMID"

  echo "waiting ${VYOS_CLOUD_INIT_WAIT_SECONDS}s for cloud-init to apply..." >&2
  sleep "$VYOS_CLOUD_INIT_WAIT_SECONDS"

  hdr "Shutdown VM"
  pve_qm shutdown "$VYOS_TEMPLATE_VMID" --timeout 60 || pve_qm stop "$VYOS_TEMPLATE_VMID"

  hdr "Detach install ISO and seed, then flip template flag"
  pve_qm set "$VYOS_TEMPLATE_VMID" --delete ide2 || true
  pve_qm set "$VYOS_TEMPLATE_VMID" --delete ide3 || true
  pve_qm template "$VYOS_TEMPLATE_VMID"

  echo "template $VYOS_TEMPLATE_VMID is ready." >&2
  echo "next: tests/pve/create-vm.sh" >&2
}

main() {
  local phase
  phase="$(pve_template_phase "$VYOS_TEMPLATE_VMID")"
  case "$phase" in
    template)
      echo "template VMID $VYOS_TEMPLATE_VMID already exists; nothing to do." >&2
      ;;
    missing)
      phase1_create_install_vm
      ;;
    running)
      echo "ERR: VMID $VYOS_TEMPLATE_VMID is currently running." >&2
      echo "     finish the install in the serial console and poweroff," >&2
      echo "     then rerun this script." >&2
      return 1
      ;;
    stopped)
      phase2_finalize_template
      ;;
    *)
      echo "ERR: unexpected template phase: $phase" >&2
      return 1
      ;;
  esac
}

main "$@"
