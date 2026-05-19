# pyvyos

[![PyPI version](https://img.shields.io/pypi/v/pyvyos.svg)](https://pypi.org/project/pyvyos/)
[![Python versions](https://img.shields.io/pypi/pyversions/pyvyos.svg)](https://pypi.org/project/pyvyos/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![PR Validation](https://github.com/vyos-contrib/pyvyos/actions/workflows/python-pr-validation.yml/badge.svg)](https://github.com/vyos-contrib/pyvyos/actions/workflows/python-pr-validation.yml)

Python SDK for the [VyOS](https://vyos.io/) HTTPS API.

`pyvyos` is a small, focused library that wraps the VyOS HTTPS API in an
idiomatic Python interface. It is intended for automation scripts, internal
tooling, and integrations with configuration management systems.

## Installation

```bash
pip install pyvyos
```

Requires **Python 3.13 or newer**.

## Quick start

Enable the HTTPS API on the VyOS device and create an API key:

```text
set service https api keys id my-key key 'your-secret-key'
commit
```

Then, from Python:

```python
import os
from pyvyos import VyDevice

device = VyDevice(
    hostname=os.environ["VYDEVICE_HOSTNAME"],
    apikey=os.environ["VYDEVICE_APIKEY"],
    port=int(os.environ.get("VYDEVICE_PORT", "443")),
    protocol=os.environ.get("VYDEVICE_PROTOCOL", "https"),
    verify=os.environ.get("VYDEVICE_VERIFY_SSL", "true").lower() in ("1", "true", "yes"),
)

response = device.show(path=["system", "image"])
if response.error:
    print(f"Error {response.status}: {response.error}")
else:
    print(response.result)
```

If you use self-signed certificates, set `verify=False` **only in lab
environments** and silence the urllib3 warning explicitly:

```python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

## Environment variables

A `.env.example` is shipped with the project. The recognised variables are:

| Variable               | Default | Purpose                                            |
| ---------------------- | ------- | -------------------------------------------------- |
| `VYDEVICE_HOSTNAME`    | —       | Hostname or IP address of the VyOS device.         |
| `VYDEVICE_APIKEY`      | —       | API key configured on the device.                  |
| `VYDEVICE_PORT`        | `443`   | HTTPS port of the VyOS API.                        |
| `VYDEVICE_PROTOCOL`    | `https` | `https` (recommended) or `http`.                   |
| `VYDEVICE_VERIFY_SSL`  | `true`  | Verify the TLS certificate of the device.          |

`pyvyos` does not read these variables on its own — your application is
responsible for loading them (for example with `python-dotenv`) and passing
the values to `VyDevice`.

## API overview

All methods return an `ApiResponse` dataclass with four fields:

```python
@dataclass
class ApiResponse:
    status: int                       # HTTP status code
    request: dict                     # the request payload (API key redacted)
    result: dict | list | str | None  # parsed `data` field from the response
    error: str | bool                 # error message, or False on success
```

`result` varies per endpoint: configuration retrieval returns a `dict` or
`list`, operational commands like `show`/`generate` often return a `str`,
and some endpoints return `None`.

The recommended usage pattern is:

```python
response = device.retrieve_show_config(path=["interfaces"])
if response.error:
    raise RuntimeError(response.error)
do_something_with(response.result)
```

### Configuration

```python
device.configure_set(path=["interfaces", "ethernet", "eth0", "address", "192.0.2.1/24"])
device.configure_delete(path=["interfaces", "dummy", "dum1"])
device.configure_multiple_op(op_path=[
    {"op": "set",    "path": ["interfaces", "dummy", "dum2", "address", "203.0.113.1/24"]},
    {"op": "delete", "path": ["interfaces", "dummy", "dum1"]},
])
```

### Retrieval

```python
device.retrieve_show_config(path=["system"])
device.retrieve_return_values(path=["interfaces", "dummy", "dum1", "address"])
```

### Operational

```python
device.show(path=["system", "image"])
device.generate(path=["ssh", "client-key", "/tmp/key"])
device.reset(path=["conntrack-sync", "internal-cache"])
```

### Configuration files

```python
device.config_file_save()                                # default location
device.config_file_save(file="/config/backup.config")
device.config_file_load(file="/config/backup.config")
```

### System control

```python
device.reboot()      # equivalent to device.reboot(path=["now"])
device.poweroff()    # equivalent to device.poweroff(path=["now"])
```

### Image management

```python
device.image_add(url="https://downloads.vyos.io/.../vyos-1.4-image.iso")
device.image_delete(name="1.4-rolling-...")
```

## Public API stability

The supported public API of pyvyos is:

```python
from pyvyos import VyDevice, ApiResponse
```

These compatibility imports continue to work without warnings and will be
kept while the migration cost remains trivial:

```python
from pyvyos.device import VyDevice
from pyvyos.rest import RestClient, ApiResponse
```

Anything under `pyvyos.core.*` is internal implementation detail and may
change between minor releases.

The deprecation timeline is:

| Release | Status                                                            |
| ------- | ----------------------------------------------------------------- |
| `0.4.x` | Compatibility shims work without warnings.                        |
| `0.5.x` | Internal solidity work; shims still silent.                       |
| `0.6.x` | Compatibility shims emit a `DeprecationWarning`.                  |
| `1.0.0` | Final shim behaviour decided before release, based on observed usage and maintenance cost. |

## Examples

- [`examples/basic.py`](examples/basic.py) — read-only end-to-end usage
  example. Safe to run against any reachable device.
- [`examples/integration_smoke.py`](examples/integration_smoke.py) —
  exercises mutating operations (`configure_set/delete`, `generate`,
  `config_file_save/load`). Intended for a disposable lab; guarded by the
  `PYVYOS_ALLOW_MUTATING_EXAMPLE=1` environment variable.
- [`examples/vagrant/`](examples/vagrant/) — Vagrant-based VyOS lab for
  local development and integration testing.

## Logging

`pyvyos` uses the standard `logging` module under the `pyvyos` namespace.
To see request/response activity, configure the logger in your application:

```python
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("pyvyos").setLevel(logging.DEBUG)
```

Log records contain structural fields only (`command`, `op`, `status`,
`elapsed_ms`) and never include the request payload or the API key.

The request payload returned via `ApiResponse.request` is sanitised — the
`key` field is replaced with `***REDACTED***` before the response is
handed back to the caller.

## VyOS compatibility

Tested against:

- VyOS 1.4 LTS (stable)
- VyOS 1.5 rolling

The library only depends on the HTTPS API surface, so versions that expose
the same endpoints should work without changes.

## Development

The project uses [uv](https://docs.astral.sh/uv/) for environment
management:

```bash
uv sync --extra dev
uv run pytest
```

Optional code-style hooks:

```bash
pip install pre-commit
pre-commit install
```

## Contributing

Bug reports and pull requests are welcome. Please open an issue first to
discuss anything beyond a small fix, and keep changes focused — payload and
public-API changes go through a separate review cycle.

## License

MIT — see [LICENSE](LICENSE).
