# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-11-20

`0.4.0` is a cleanup and consolidation release. It is the first version
since `0.2.2` published to PyPI. The git tag `v0.4.0` previously pointed at
the intermediate refactor commit `6b4e901`; it has been moved to the
release commit that includes the cleanup described below.

This release **does not change HTTP payload generation or request/response
behavior**.

### Added
- `examples/basic.py` — runnable end-to-end usage example using the
  supported public API (`from pyvyos import VyDevice`).
- `pyvyos/py.typed` PEP 561 marker, advertising the package as typed.
- `.pre-commit-config.yaml` with neutral hooks (trailing whitespace,
  end-of-file fixer, YAML/TOML syntax check, large-file guard).
- GitHub Actions ecosystem entry in `.github/dependabot.yml` so workflow
  versions stay current.
- Documented public API stability and deprecation timeline in `README.md`.

### Changed
- `vagrant/` lab setup moved to `examples/vagrant/`.
- `pyvyos.core.*` is now the internal implementation layer; the supported
  public API is `from pyvyos import VyDevice, ApiResponse`. The legacy
  `pyvyos.device` and `pyvyos.rest` shims continue to work without
  warnings.
- `RestClient` logging is now plain and structured: command, op, status,
  elapsed milliseconds. No request-ID field.
- `pyproject.toml`:
  - declared the wheel package explicitly,
  - removed duplicated dependency blocks,
  - dropped the unused `validation` extra,
  - raised the pytest floor for Python 3.13.
- PR validation workflow upgraded to `actions/checkout@v4`,
  `actions/setup-python@v5`, and `astral-sh/setup-uv@v3`.
- `.env.example` default flipped to `VYDEVICE_VERIFY_SSL=true`; commented
  with field descriptions.

### Removed
- Root-level stragglers: `CONTRIB.md` (superseded by `CONTRIBUTING.md`),
  `requirements.txt` (duplicated `[project].dependencies`), `test_quick.py`
  (ad-hoc smoke script, covered by `tests/test_shims.py`), and the
  committed `uv.lock` (not appropriate for a library; now gitignored).
- `pyvyos.specs` package (experimental Pydantic models). It was never
  imported by the runtime and had 0% test coverage. Pydantic is no longer
  an optional dependency.
- `pyvyos.exceptions` module (`SDKError`, `HttpError`, `ApiError`,
  `ValidationError`). The hierarchy was defined but never raised anywhere
  in the codebase. Error reporting continues through `ApiResponse.error`.
- `pyvyos.utils.ids.request_id` helper. The generated UUIDs were attached
  to log records but never propagated to callers — half-implemented
  tracing is worse than none. It will be reintroduced if and when real
  observability hooks land.
- `pyvyos.utils` no longer re-exports `request_id`.
- Obsolete tooling: `Makefile` (hard-coded `env/bin/python`),
  `run_tests.sh`, `run_tests.py`.
- Dead workflow `.github/workflows/python-app.yml` (Python 3.12, only ran
  flake8 with pytest commented out, referenced a non-existent
  `requirements.txt`).
- `sphinx/` source tree and `.readthedocs.yaml`: the RTD configuration
  pointed to `docs/source/conf.py` while the Sphinx tree lived under
  `sphinx/source/`, so the build never worked and no documentation was
  ever published. The hand-written Markdown docs under `docs/` are
  retained.
- Stale development notes under `docs/development/` (architecture,
  refactor roadmap, quality-and-utils) — they described the pre-cleanup
  proposal that included specs/exceptions/request_id.
- Tests for the removed modules (`tests/test_exceptions.py`,
  `tests/utils/test_ids.py`).

### Fixed
- `LICENSE` copyright now reads `2023 GravScale, Roberto Bertó`.

### Compatibility
- Public imports are unchanged:
  - `from pyvyos import VyDevice, ApiResponse`
  - `from pyvyos.device import VyDevice`
  - `from pyvyos.rest import RestClient, ApiResponse`
- HTTP payload generation is unchanged.
- Request and response behaviour is unchanged.
- No compatibility shim has been deprecated in this release.

### Notes
- This release prepares the project for the upcoming `0.5.x` work:
  contract tests for public payloads, fixes to the public method edges
  (`image_add`/`image_delete`, `timeout`, mutable defaults), stdlib-based
  validators, and a tidier internal core.

## [0.3.0] - 2024-XX-XX

Tagged in git but never published to PyPI. Released to PyPI as part of
`0.4.0`.

### Added
- Initial public release of the SDK structure.
- Core functionality for VyOS HTTPS API: configure, retrieve, show,
  generate, reset, config-file, reboot, poweroff, and image operations.

[Unreleased]: https://github.com/vyos-contrib/pyvyos/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/vyos-contrib/pyvyos/compare/v0.2.2...v0.4.0
[0.3.0]: https://github.com/vyos-contrib/pyvyos/releases/tag/v0.3.0
