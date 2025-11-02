# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-01-XX

### Added
- Exception hierarchy (`SDKError`, `HttpError`, `ApiError`, `ValidationError`) in `pyvyos.exceptions`
- Utility functions in `pyvyos.utils`:
  - `json.redact_key()` and `json.safe_dumps()` for secure JSON handling
  - `ids.request_id()` for request tracing
  - `paths.build_path()` for building configuration paths
- Structured logging in `RestClient` with request ID tracking and elapsed time
- Optional Pydantic validation models in `pyvyos.specs.commands.*` for request/response validation
- Development documentation:
  - Architecture guide (`docs/development/architecture.md`)
  - Refactor roadmap (`docs/development/refactor-roadmap.md`)
  - Quality and utils guidelines (`docs/development/quality-and-utils.md`)
- Comprehensive test suite for backward compatibility (19 tests for shims, 16 tests for utils, 6 tests for exceptions)
- `[tool.uv] package = true` in `pyproject.toml` for editable installation via `uv sync`

### Changed
- Moved JSON API specifications from `pyvyos/vyos-api/` to `docs/development/vyos_api/` (reference only)
- Updated `pyproject.toml` to include optional `validation` dependency group for Pydantic
- Enhanced `RestClient` logging with structured fields (request_id, command, op, status, elapsed_ms)
- Refactored internal structure to `pyvyos.core.*` while maintaining full backward compatibility via shims

### Fixed
- **Fixed #25**: `config_file_save()` and `config_file_load()` now correctly include `path: []` in payload as required by VyOS API
- Path parameter handling for `config-file` commands (always includes `path: []`)
- Secret redaction in logs and sanitized payloads

### Security
- API keys are automatically redacted in logs and response payloads

### Notes
- This release maintains 100% backward compatibility with version 0.3.0
- All existing imports and code will continue to work without changes
- New internal structure (`pyvyos.core.*`) is available but not required for existing code

## [0.3.0] - 2024-XX-XX

### Added
- Initial release
- Core functionality for VyOS REST API interaction
- Support for configure, retrieve, show, generate, reset, config-file, reboot, poweroff, and image operations

[Unreleased]: https://github.com/vyos-contrib/pyvyos/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/vyos-contrib/pyvyos/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/vyos-contrib/pyvyos/releases/tag/v0.3.0

