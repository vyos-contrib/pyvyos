# Refactor Roadmap (Prioritized)

## Priorities
- P0 (now): safety, compatibility, correctness
- P1 (next): validation, observability, developer UX
- P2 (later): performance, async, resiliency

## P0 — Immediate
- Stabilize transport: keep `_get_payload(include_empty_path)`; special-case `config-file`
- Keep shims: `pyvyos/device.py` and `pyvyos/rest.py` re-export from `pyvyos/core/*`
- Typed exceptions: introduce `SDKError`, `HttpError`, `ApiError`, `ValidationError`
- Timeouts: ensure sane defaults, expose in `VyDevice`
- Logging: centralize in transport, structured key fields (op, command, status)
- Tests: payload assertions for `config-file` (path: []), regression for others
- Docs: architecture and path rules (done)

## P1 — Short Term
- Specs (optional): Pydantic models in `pyvyos/specs/commands/*`
- `utils/`: path builders, request_id, safe_json redaction
- Deprecation policy: note in README; warn on internal imports (future only)
- CI: test matrix (Python 3.13), codecov, lint (ruff/flake8), type-check (pyright/mypy)
- Release: conventional commits + CHANGELOG; ensure tags push
- Docs: contributor guide, release playbook (short)

## P2 — Medium Term
- Async client: `AsyncRestClient` (aiohttp/httpx), opt-in
- Retries & backoff: idempotent ops only; circuit-breaker (future)
- Rate limiting: client-side token bucket (opt-in)
- Caching: read-only `show/retrieve` (TTL) optional
- Batch ops: smarter `configure_multiple_op` planning

## Migration & Compatibility
- Public API: `from pyvyos import VyDevice, ApiResponse` (stable)
- Internal: prefer `pyvyos.core.*` for new code
- Shims stay until 1.0.0; removal at next major only

## Testing Plan
- Unit: transport (errors, timeouts), domain (paths)
- Contract: sample JSON fixtures per command
- E2E: optional job against a test VyOS (gated, non-blocking)

## Release Flow (lean)
- Branch: feature → PR → squash merge
- Pre-release (optional): `-rcX` tags
- Tag + publish: GitHub Action (uv build + PyPI publish)

## Risks & Mitigations
- Hidden breakages → keep shims, add regression tests
- API drift (VyOS) → specs folder eases updates
- Logging noise → default INFO; debug gated via env
- Security → default `verify=True`, redact secrets in logs

## Success Criteria
- 0.3.x users unaffected
- New structure adopted by contributors
- Lower maintenance overhead (fewer regressions)
