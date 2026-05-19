"""Live VyOS smoke tests for pyvyos.

These are intentionally a small, opinionated subset of the SDK:
just enough to prove that payloads round-trip against a real VyOS
HTTPS API. Destructive operations (reboot/poweroff/image-add/
image-delete/reset/config-file-load) live in a separate file when
they exist; not in scope for v0.4.x.
"""

from __future__ import annotations

import random

from pyvyos import ApiResponse, VyDevice


def _ok(response: ApiResponse) -> None:
    assert response.status == 200, f"status={response.status} error={response.error!r}"
    assert not response.error, f"unexpected error: {response.error!r}"


def _dummy_name() -> str:
    """VyOS requires dummy interfaces to match `dumN`.

    Pick a high random N to avoid collision with anything an operator
    may have created manually.
    """
    return f"dum{random.randint(900, 9999)}"


def test_show_system_image(device: VyDevice) -> None:
    response = device.show(path=["system", "image"])
    _ok(response)
    assert response.result is not None


def test_retrieve_show_config_system(device: VyDevice) -> None:
    response = device.retrieve_show_config(path=["system"])
    _ok(response)
    assert isinstance(response.result, dict)


def test_configure_set_read_delete_dummy_iface(device: VyDevice) -> None:
    name = _dummy_name()
    address = "192.0.2.10/32"
    iface_path = ["interfaces", "dummy", name]

    try:
        set_response = device.configure_set(path=iface_path + ["address", address])
        _ok(set_response)

        read_response = device.retrieve_return_values(path=iface_path + ["address"])
        _ok(read_response)
        # retrieve_return_values returns a list of stringified values.
        assert address in str(read_response.result), read_response.result
    finally:
        cleanup = device.configure_delete(path=iface_path)
        _ok(cleanup)


def test_configure_multiple_op_batch(device: VyDevice) -> None:
    name = _dummy_name()
    iface_path = ["interfaces", "dummy", name]

    response = device.configure_multiple_op(
        op_path=[
            {"op": "set", "path": iface_path + ["address", "192.0.2.11/32"]},
            {"op": "delete", "path": iface_path},
        ]
    )
    _ok(response)
