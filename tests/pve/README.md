# PVE end-to-end harness

This directory holds a small, opinionated harness to run pyvyos
against a real VyOS VM on a local Proxmox VE host.

It is intentionally **not** part of CI. The unit test suite under
`tests/modules/` is fast, mock-based, and runs on every PR. The
harness here exists for maintainers who want a periodic reality
check — the gap a mock cannot close.

> This harness creates confidence against real VyOS without turning
> the project into a CI of appliances.

## What it gives you

A reproducible flow:

```text
ensure-template.sh   # build a reusable VyOS template once
create-vm.sh         # clone the template into a fresh e2e VM
start-vm.sh          # power it on
run-e2e.sh           # run pytest tests/e2e against it
stop-vm.sh           # power it off
destroy-vm.sh        # purge it
```

The template carries an API key baked at build time via cloud-init.
Clones inherit it, so the e2e VM is reachable as soon as the API is
up.

## Requirements

- a Proxmox VE host you can `ssh` to (preferably via an alias in
  `~/.ssh/config`)
- a VyOS rolling install ISO already on the PVE host, under
  `/var/lib/vz/template/iso/` (download from
  https://github.com/vyos/vyos-nightly-build/releases; this harness
  does **not** download it for you)
- `genisoimage` (or `mkisofs`) installed on the PVE host —
  `apt install genisoimage` once
- Python 3.11+ and `uv` (or `pytest`) on your workstation to run the
  test suite itself

## First-time setup

```bash
cp tests/pve/.env.example tests/pve/.env
$EDITOR tests/pve/.env       # fill in your host, VMIDs, IP, API key
chmod +x tests/pve/*.sh

tests/pve/preflight.sh       # read-only sanity check
tests/pve/ensure-template.sh # phase 1: creates VM with installer
```

The first run of `ensure-template.sh` boots a VM with the VyOS
installer ISO attached and prints instructions:

```text
on the PVE host:
  qm terminal <VMID>           # Ctrl-] exits

inside VyOS:
  login: vyos / vyos
  install image                # accept defaults, set a password
  poweroff
```

Do that once. Then run it again:

```bash
tests/pve/ensure-template.sh  # phase 2: cloud-init applies API key,
                              #          shuts down, flips template flag
```

The script is a state machine on the VMID, so re-running it from any
point is safe.

## Per-run workflow

```bash
tests/pve/create-vm.sh
tests/pve/start-vm.sh
tests/pve/run-e2e.sh
tests/pve/stop-vm.sh
tests/pve/destroy-vm.sh
```

`run-e2e.sh` exports the `VYDEVICE_*` variables from `.env` and runs
`pytest tests/e2e -v` with `PYVYOS_E2E=1`. Without that variable the
e2e tests are skipped automatically.

## Scope

The live suite is intentionally small:

| Test                                 | What it proves                |
| ------------------------------------ | ----------------------------- |
| `test_show_system_image`             | operational API responds      |
| `test_retrieve_show_config_system`   | config retrieval works        |
| `test_configure_set_read_delete...`  | set / read-back / delete loop |
| `test_configure_multiple_op_batch`   | the batch payload is correct  |

Out of scope on purpose: `reboot`, `poweroff`, `image_add`,
`image_delete`, `reset`, `config_file_load`. Those are destructive or
slow; they will get their own opt-in file if anyone needs them.

## Troubleshooting

### Cloud-init did not apply on first boot

VyOS cloud-init handling varies between rolling builds. If the API
key is not active after phase 2, boot the VM, configure the API
manually once, save, poweroff, and rerun `ensure-template.sh`:

```text
configure
set service https api rest
set service https api keys id pyvyos key 'pyvyos-e2e-please-change-me'
set service https listen-address '0.0.0.0'
commit
save
exit
poweroff
```

The `set service https api rest` line is essential. Without it the
HTTPS service only exposes `/info`, and every other endpoint
(`/retrieve`, `/configure`, `/show`, …) responds with `404`. See
the VyOS docs for HTTP API service.

### HTTP 400 "Dummy interface must be named dumN"

The live tests intentionally use interface names like `dum1234` to
match the VyOS naming policy for `dummy` interfaces. If you adapt
the tests, keep that pattern; arbitrary names are rejected by VyOS
config validation with a 400.

### "VMID already exists"

Each script checks before mutating. To start over from scratch:

```bash
tests/pve/destroy-vm.sh                 # clears the e2e VM
ssh $PVE_SSH_TARGET qm destroy $VYOS_TEMPLATE_VMID --purge
tests/pve/ensure-template.sh            # phase 1 again
```

### API key in the template

The key from `tests/pve/.env` is baked into the template. That is
fine for a private lab. **Do not** export this template to a shared
PVE or hand it to other people without rotating the key.

## What this harness is not

- Not Vagrant. `examples/vagrant/` already covers desktop labs.
- Not Docker. VyOS is an appliance OS; real KVM is the honest test.
- Not CI. GitHub Actions cannot run nested KVM cheaply, and a
  scheduled live job on someone else's hardware is not worth the
  operational cost for a thin SDK.
- Not a packaging story. The harness is for maintainers and brave
  users; nothing in `pyvyos/` depends on it.
