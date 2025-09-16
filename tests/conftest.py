import os

import pytest

from pyvyos import VyDevice


@pytest.fixture(scope="module")
def config_device():
    return {
        "hostname": os.getenv("VYDEVICE_HOSTNAME", "localhost"),
        "apikey": os.getenv("VYDEVICE_APIKEY", "api_key"),
        "port": os.getenv("VYDEVICE_PORT", 443),
        "protocol": os.getenv("VYDEVICE_PROTOCOL", "https"),
        "verify": os.getenv("VYDEVICE_VERIFY_SSL", False),
        "timeout": 0,
    }


@pytest.fixture(scope="module")
def test_device(config_device):
    return VyDevice(**config_device)
