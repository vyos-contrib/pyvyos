#!/usr/bin/env bash
# tests/pve/_lib.sh — source-only helpers for the PVE e2e harness.
#
# Public surface:
#   pve_load_env [path]      load tests/pve/.env (or argument) and validate
#   pve_require_reachable    fail unless `ssh $PVE_SSH_TARGET true` works
#   pve_ssh "cmd..."         run a command on the PVE host
#   pve_qm   args...         shorthand for `pve_ssh qm args...`
#   pve_scp src dst          copy a local file to the PVE host
#   pve_template_phase       echo: missing | running | stopped | template
#   hdr "title"              print a section header to stderr
#
# Refuses direct execution.

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "ERR: tests/pve/_lib.sh is source-only; do not execute it." >&2
  exit 1
fi

set -euo pipefail

PVE_LIB_REQUIRED_VARS=(
  PVE_SSH_TARGET
  PVE_NODE
  PVE_STORAGE
  PVE_BRIDGE
  PVE_IMAGE_DIR
  VYOS_ISO_PATH
  VYOS_TEMPLATE_VMID
  VYOS_TEMPLATE_NAME
  VYOS_E2E_VMID
  VYOS_E2E_VM_NAME
  VYOS_E2E_IP
  VYOS_E2E_CIDR
  VYOS_E2E_GATEWAY
  VYDEVICE_APIKEY
)

pve_load_env() {
  local env_file="${1:-}"
  if [[ -z "$env_file" ]]; then
    env_file="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.env"
  fi
  if [[ ! -f "$env_file" ]]; then
    echo "ERR: missing env file: $env_file" >&2
    echo "     copy tests/pve/.env.example to tests/pve/.env and fill it in." >&2
    return 1
  fi
  set -a
  # shellcheck disable=SC1090
  source "$env_file"
  set +a

  local missing=()
  local v
  for v in "${PVE_LIB_REQUIRED_VARS[@]}"; do
    if [[ -z "${!v:-}" ]]; then
      missing+=("$v")
    fi
  done
  if (( ${#missing[@]} > 0 )); then
    echo "ERR: env file $env_file is missing values for: ${missing[*]}" >&2
    return 1
  fi
}

pve_ssh() {
  # ssh joins remaining args with spaces and hands the result to the
  # remote login shell, so any unquoted `;`, `&`, `|`, `$`, glob, etc.
  # would be re-interpreted there. When the caller passes a single
  # argument we treat it as a verbatim remote script. When several are
  # passed we shell-escape each one with `printf %q` so the remote
  # shell sees exactly one argv per local argv.
  if (( $# == 1 )); then
    ssh -o BatchMode=yes -o ConnectTimeout=10 "$PVE_SSH_TARGET" "$1"
  else
    local cmd
    # shellcheck disable=SC2059
    cmd="$(printf '%q ' "$@")"
    ssh -o BatchMode=yes -o ConnectTimeout=10 "$PVE_SSH_TARGET" "$cmd"
  fi
}

pve_qm() {
  pve_ssh qm "$@"
}

pve_scp() {
  local src="$1" dst="$2"
  scp -o BatchMode=yes -o ConnectTimeout=10 "$src" "$PVE_SSH_TARGET:$dst"
}

pve_require_reachable() {
  if ! pve_ssh true >/dev/null 2>&1; then
    echo "ERR: cannot ssh to PVE host '$PVE_SSH_TARGET'." >&2
    echo "     check ~/.ssh/config, your key, and that the host is up." >&2
    return 1
  fi
}

# Echo one of:
#   missing   — VMID not registered in PVE
#   running   — VM exists and is running
#   stopped   — VM exists, not a template, currently stopped
#   template  — VM exists and is flagged as a template
pve_template_phase() {
  local vmid="$1"
  if ! pve_qm status "$vmid" >/dev/null 2>&1; then
    echo missing
    return
  fi
  if pve_qm config "$vmid" | grep -q '^template: 1'; then
    echo template
    return
  fi
  # `qm status <vmid>` prints e.g. "status: running"
  local s
  s="$(pve_qm status "$vmid" | awk '{print $2}')"
  if [[ "$s" == "running" ]]; then
    echo running
  else
    echo stopped
  fi
}

hdr() {
  printf '\n=== %s ===\n' "$*" >&2
}
