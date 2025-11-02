# Development Architecture (Proposed)

## Goals
- Strong separation of concerns (transport, domain, specs, utils)
- Backward compatibility for 0.3.0 via shims
- Clear public API surface and internal boundaries
- Minimal maintenance burden for a public, official SDK

## Source Layout (file tree)
```
pyvyos/
  __init__.py            # public API exports (VyDevice, ApiResponse)
  core/                  # internal, stable layers
    __init__.py
    rest_client.py       # RestClient, ApiResponse (transport layer)
    device.py            # VyDevice (domain layer)
  specs/                 # optional Pydantic models (validation)
    __init__.py
    models.py            # base models (ApiRequest/Response)
    commands/            # split by responsibility
      __init__.py
      configure.py       # set, delete, multiple_op
      retrieve.py        # show_config, return_values
      config_file.py     # save, load (path: [])
      show.py            # show
      generate.py        # generate
      reset.py           # reset
      system.py          # reboot, poweroff
      image.py           # add, delete
  utils/                 # reusable helpers (no side effects)
    __init__.py
    json.py              # safe_json, redact_key
    http.py              # timeouts, retries (future)
    paths.py             # path builder helpers
    ids.py               # request_id helpers
  exceptions.py          # typed exceptions (SDKError, HttpError, ApiError)
  types.py               # public typing aliases if needed
  device.py              # shim re-export (compat)
  rest.py                # shim re-export (compat)
  vyos_api/              # JSON specs (docs/reference, optional at runtime)
```

## Layers & Responsibilities
- Transport (core.rest_client): HTTP, payload assembly, response validation
- Domain (core.device): high-level methods (configure, show, reset, etc.)
- Specs (specs.*): optional Pydantic models to validate requests/answers
- Utils: pure helpers (formatting, ids, path building)
- Shims (device.py, rest.py): ensure 0.3.0 compatibility

## Public API Surface
- `from pyvyos import VyDevice, ApiResponse`
- Stable imports; internal moves hidden by shims

## Compatibility Strategy
- Keep shims until 1.0.0
- Deprecation policy: warn after N minors, remove at next major
- Document migration path (import from `pyvyos.core` for new code)

## Data Validation Flow (optional)
- App builds `path` with utils.paths
- If validation enabled, use `specs.commands.*` models
- RestClient serializes payload and executes request
- Response validated (structure: success/data/error)

## Testing Strategy
- Unit: core.rest_client and core.device isolated via monkeypatch
- Contract: JSON fixtures mirror VyOS responses
- E2E (future): optional with test VyOS VM

## Packaging
- Include `vyos_api/` only if needed at runtime
- Otherwise treat it as docs/reference, not required by the package

## Naming & Conventions
- Use underscores `_` in file and module names
- One responsibility per module (keep files small)
- Typed public APIs, specific exceptions, no prints (only logging)
