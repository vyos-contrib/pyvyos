"""Shared fixtures for pyvyos live end-to-end tests.

These tests run only when PYVYOS_E2E=1 is set in the environment.
They expect a VyOS HTTPS API reachable at VYDEVICE_HOSTNAME with the
key in VYDEVICE_APIKEY. The harness under tests/pve/ provides one
way to stand up such a VM on a local Proxmox host, but any VyOS
instance you can reach works.
"""

from __future__ import annotations

import os
import time

import pytest

from pyvyos import VyDevice


E2E_ENABLED = os.environ.get("PYVYOS_E2E") == "1"


def _env_bool(name: str, default: str = "false") -> bool:
    return os.environ.get(name, default).lower() in {"1", "true", "yes"}


@pytest.fixture(scope="session")
def device() -> VyDevice:
    """A VyDevice pointed at the live VyOS under test.

    Session-scoped because the device is stateless on the client side
    and reusing it keeps the suite fast.
    """
    missing = [
        v for v in ("VYDEVICE_HOSTNAME", "VYDEVICE_APIKEY") if not os.environ.get(v)
    ]
    if missing:
        pytest.fail(
            f"missing required environment variables: {missing}. "
            "See tests/pve/.env.example for the full set."
        )

    return VyDevice(
        hostname=os.environ["VYDEVICE_HOSTNAME"],
        apikey=os.environ["VYDEVICE_APIKEY"],
        protocol=os.environ.get("VYDEVICE_PROTOCOL", "https"),
        port=int(os.environ.get("VYDEVICE_PORT", "443")),
        verify=_env_bool("VYDEVICE_VERIFY_SSL"),
        timeout=10,
    )


@pytest.fixture(scope="session", autouse=True)
def _wait_for_api(device: VyDevice) -> None:
    """Block the suite until the HTTPS API answers, or fail loudly.

    A freshly cloned VM may need a moment after `qm start` before the
    HTTPS service binds. We retry a cheap read for up to two minutes.
    """
    if not E2E_ENABLED:
        return

    deadline = time.time() + 120
    last_error: str | None = None
    while time.time() < deadline:
        try:
            response = device.show(path=["system", "image"])
            if not response.error:
                return
            last_error = response.error
        except Exception as exc:  # noqa: BLE001 — broad on purpose, we retry
            last_error = repr(exc)
        time.sleep(3)

    pytest.fail(
        f"VyOS HTTPS API at {os.environ.get('VYDEVICE_HOSTNAME')} did not become "
        f"ready within 120s. Last error: {last_error}"
    )


def pytest_collection_modifyitems(config, items) -> None:
    """Skip only e2e tests unless PYVYOS_E2E=1.

    This conftest is auto-discovered by pytest at the session level,
    so the hook sees every collected item in the run. Filter by path
    to avoid skipping the unit suite under tests/modules/.
    """
    if E2E_ENABLED:
        return
    skip = pytest.mark.skip(
        reason="set PYVYOS_E2E=1 to run live VyOS end-to-end tests"
    )
    e2e_dir = os.path.join("tests", "e2e") + os.sep
    for item in items:
        if e2e_dir in str(item.fspath):
            item.add_marker(skip)
