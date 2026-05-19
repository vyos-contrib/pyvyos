"""Integration smoke test for pyvyos.

This script changes configuration on the target VyOS device and should only
be used against a disposable lab device, such as the one provided by
``examples/vagrant/``.

It may create and delete dummy interfaces, generate temporary files on the
device, and save/load configuration files.

Run only against a lab device::

    PYVYOS_ALLOW_MUTATING_EXAMPLE=1 \\
    VYDEVICE_HOSTNAME=127.0.0.1 \\
    VYDEVICE_APIKEY=secret \\
    python examples/integration_smoke.py
"""

import os
import pprint
import random
import string
import sys

from dotenv import load_dotenv

from pyvyos import VyDevice

load_dotenv()


def env_bool(name: str, default: str = "true") -> bool:
    return os.environ.get(name, default).lower() in ("1", "true", "yes")


def make_device() -> VyDevice:
    return VyDevice(
        hostname=os.environ["VYDEVICE_HOSTNAME"],
        apikey=os.environ["VYDEVICE_APIKEY"],
        port=int(os.environ.get("VYDEVICE_PORT", "443")),
        protocol=os.environ.get("VYDEVICE_PROTOCOL", "https"),
        verify=env_bool("VYDEVICE_VERIFY_SSL"),
        timeout=int(os.environ.get("VYDEVICE_TIMEOUT", "60")),
    )


def main() -> None:
    if os.environ.get("PYVYOS_ALLOW_MUTATING_EXAMPLE") != "1":
        sys.exit(
            "This example mutates the target device. "
            "Set PYVYOS_ALLOW_MUTATING_EXAMPLE=1 to run it."
        )

    device = make_device()

    # Retrieve the running configuration for the system tree.
    pprint.pprint(device.retrieve_show_config(path=["system"]))

    # Configure a dummy interface, read it back, then delete it.
    pprint.pprint(
        device.configure_set(
            path=["interfaces", "dummy", "dum1", "address", "192.168.56.100/24"]
        )
    )
    pprint.pprint(
        device.retrieve_return_values(
            path=["interfaces", "dummy", "dum1", "address"]
        )
    )
    pprint.pprint(device.configure_delete(path=["interfaces", "dummy", "dum1"]))

    # Generate a one-shot SSH client key.
    randstring = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(20)
    )
    pprint.pprint(
        device.generate(path=["ssh", "client-key", f"/tmp/key_{randstring}"])
    )

    # Operational commands.
    pprint.pprint(device.show(path=["system", "image"]))
    pprint.pprint(device.reset(path=["conntrack-sync", "internal-cache"]))

    # Save and reload the running configuration to/from a file on the device.
    pprint.pprint(device.config_file_save(file="/config/test300.config"))
    pprint.pprint(device.config_file_load(file="/config/test300.config"))

    # Batch multiple configuration operations in a single request.
    pprint.pprint(
        device.configure_multiple_op(
            op_path=[
                {
                    "op": "set",
                    "path": [
                        "interfaces", "dummy", "dum1", "address",
                        "192.168.56.100/24",
                    ],
                },
                {"op": "delete", "path": ["interfaces", "dummy", "dum1"]},
            ]
        )
    )


if __name__ == "__main__":
    main()
