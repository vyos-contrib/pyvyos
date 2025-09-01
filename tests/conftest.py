import os

import pytest

from pyvyos import VyDevice


@pytest.fixture(scope="module")
def config_device():
    return {
        "hostname": os.getenv("VYDEVICE_HOSTNAME"),
        "apikey": os.getenv("VYDEVICE_APIKEY"),
        "port": os.getenv("VYDEVICE_PORT"),
        "protocol": os.getenv("VYDEVICE_PROTOCOL"),
        "verify": os.getenv("VYDEVICE_VERIFY_SSL"),
        "timeout": 0,
    }


@pytest.fixture(scope="module")
def test_device(config_device):
    return VyDevice(**config_device)
