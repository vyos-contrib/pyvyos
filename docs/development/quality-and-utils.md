# Quality, Utils, and Pitfalls

## Goals
- Reduce regressions and supportability burden
- Consistent error handling and logging
- Clear utilities to avoid duplication

## Exceptions (typed)
- `SDKError` (base)
- `HttpError(status, message)`
- `ApiError(message, details=None)`  # when success=False
- `ValidationError(message)`         # client-side validation

## Logging
- Use `logging.getLogger("pyvyos")`
- Include: op, command, status, elapsed_ms, request_id
- Redact secrets (api key) – via `utils.json.redact_key(data, keys=["key"])`
- Default INFO; DEBUG guarded by env `PYVYOS_DEBUG=1`

## Timeouts & Retries
- Default timeout: 10s (configurable)
- No implicit retries by default
- Future: retry idempotent ops only (exponential backoff)

## Security
- `verify=True` by default
- Document `urllib3.disable_warnings()` only for dev
- Never log secrets or full payloads by default

## Utilities (proposal)
- `utils.paths.build(*segments) -> list[str]`
- `utils.ids.request_id() -> str`
- `utils.json.safe_dumps(obj) -> str` (with redaction)
- `utils.http.timeout(seconds) -> int` (normalize)

## Validation (optional)
- `specs.commands.*` Pydantic models validate request structures
- Enforce path rules (e.g., config-file requires `path=[]`)
- Gate behind feature flag or optional dependency group

## Testing
- Unit: small, isolated, no real I/O
- Contract: success/error fixtures per command
- Naming: `test_should_<do>_when_<condition>`
- Use monkeypatch on `_execute_request`

## Documentation
- Keep developer docs scoped and short (≤100 lines)
- Update api-reference and path rules on changes

## Style & Types
- Type hints on public APIs, avoid `Any`
- Early returns, no deep nesting, no bare `except`
- Constants for command/operation strings

## Release Hygiene
- Conventional commits; CHANGELOG generated
- Tag every release; ensure `git push --tags`
- Patch bumps for fixes, minor for features

## Potential Pitfalls & Fixes
- Path handling inconsistencies → centralize in RestClient
- Logging secrets → redact before logging
- Tight coupling device↔transport → maintain clean core boundaries
- Hidden breaking changes → keep shims until 1.0.0
- Non-deterministic tests → remove sleeps, use fixed seeds

## Next Steps (ordered)
1. Introduce `exceptions.py` and wire into RestClient
2. Add `utils/` with `json.py`, `paths.py`, `ids.py`
3. Add optional `specs/` models for high-value commands
4. CI: lint+type-check, codecov, test matrix
