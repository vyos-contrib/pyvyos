# Contributing to pyvyos

Thanks for considering a contribution. `pyvyos` is a small library with a
narrow scope, which makes review and maintenance easier when contributions
follow a few simple rules.

## Scope

`pyvyos` is a thin Python wrapper around the VyOS HTTPS API. Changes that
fit naturally into this scope are welcome. Anything that adds a new
dependency, introduces a parallel client (SSH, NETCONF, …), or expands
beyond the HTTPS API surface is best discussed in an issue first.

## Before opening a pull request

1. **Open an issue first** for anything beyond a small fix or a typo. It
   saves everyone time if the direction is agreed before the patch lands.
2. **Keep the diff focused.** One topic per pull request. Refactors and
   bug fixes are easier to review separately.
3. **Do not change HTTP payload generation in passing.** Payload changes
   require a deliberate review pass; they should be their own pull
   request and include tests.
4. **Run the test suite locally:** `uv run pytest`.
5. **Match the existing style.** No formatter is enforced yet; just keep
   diffs minimal and readable.

## Development setup

```bash
git clone https://github.com/vyos-contrib/pyvyos.git
cd pyvyos
uv sync --extra dev
uv run pytest
```

Optional pre-commit hooks (whitespace, EOF, YAML/TOML syntax):

```bash
pip install pre-commit
pre-commit install
```

## Public API stability

The supported public API is:

```python
from pyvyos import VyDevice, ApiResponse
```

Compatibility shims at `pyvyos.device` and `pyvyos.rest` are kept while
the cost is trivial. Anything under `pyvyos.core.*` is internal and may
change between minor releases.

If your change touches the public API surface, please flag it explicitly
in the pull request description.

## Reporting bugs

When reporting a bug, please include:

- The `pyvyos` version (`pip show pyvyos`).
- The Python version.
- The VyOS version of the device.
- A minimal reproducer and the resulting error (or, for behaviour bugs,
  the observed vs expected behaviour).

## License

By contributing you agree that your contribution will be licensed under
the [MIT License](LICENSE).
