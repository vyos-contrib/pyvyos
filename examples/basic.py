"""Basic read-only pyvyos usage example.

Run with environment variables loaded from a .env file or exported in your
shell:

    VYDEVICE_HOSTNAME=192.0.2.1 \\
    VYDEVICE_APIKEY=secret \\
    python examples/basic.py

This example only runs read-only commands.
"""

import os
import pprint

from dotenv import load_dotenv

from pyvyos import ApiResponse, VyDevice

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


def print_response(label: str, response: ApiResponse) -> None:
    print(f"\n== {label} ==")
    if response.error:
        print(f"Error {response.status}: {response.error}")
        return

    pprint.pprint(response.result)


def main() -> None:
    device = make_device()

    print_response(
        "Running system configuration",
        device.retrieve_show_config(path=["system"]),
    )

    print_response(
        "System images",
        device.show(path=["system", "image"]),
    )

    print_response(
        "Interface address values",
        device.retrieve_return_values(path=["interfaces"]),
    )


if __name__ == "__main__":
    main()
