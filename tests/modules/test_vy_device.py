import random
import string

import pytest
import requests

from pyvyos import VyDevice
from pyvyos.rest import RestClient


def test_device_invalid_configuration():
    with pytest.raises(ValueError):
        VyDevice(
            "tst",
            "123",
            "123",
            "123",
            2,
        )


def test_device_configuration(test_device):
    assert isinstance(test_device.hostname, str)
    assert isinstance(test_device.apikey, str)
    assert isinstance(test_device.port, int)
    assert isinstance(test_device.protocol, str)
    assert isinstance(test_device.verify, bool)


def test_device_retrieve_show_config(monkeypatch, test_device):
    def mock_retrieve_show_config(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {
            "success": True,
            "data": {
                "config-management": {"commit-revisions": "100"},
                "host-name": "pyvyos-device",
                "name-server": "eth0",
            },
            "error": None,
        }

        return response

    monkeypatch.setattr(
        RestClient,
        "_execute_request",
        mock_retrieve_show_config,
    )

    api_resp = test_device.retrieve_show_config(["system"])
    assert api_resp.result
    assert isinstance(api_resp.result, dict)


def test_device_configure_set(monkeypatch, test_device):
    def mock_configure_set(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {
            "success": True,
            "data": {},
            "error": None,
        }

        return response

    monkeypatch.setattr(
        RestClient,
        "_execute_request",
        mock_configure_set,
    )

    api_resp = test_device.configure_set(
        path=["interfaces", "dummy", "dum1", "address", "192.168.56.100/24"]
    )
    assert isinstance(api_resp.result, dict)


def test_device_retrieve_return_values(monkeypatch, test_device):
    def mock_retrieve_return_values(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {
            "success": True,
            "data": ["192.168.56.100/24"],
            "error": None,
        }

        return response

    monkeypatch.setattr(
        RestClient,
        "_execute_request",
        mock_retrieve_return_values,
    )

    api_resp = test_device.retrieve_return_values(
        path=["interfaces", "dummy", "dum1", "address", "192.168.56.100/24"]
    )
    assert api_resp.result
    assert isinstance(api_resp.result, list)


def test_device_configure_delete(monkeypatch, test_device):
    def mock_configure_delete(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {
            "success": True,
            "data": {},
            "error": None,
        }

        return response

    monkeypatch.setattr(
        RestClient,
        "_execute_request",
        mock_configure_delete,
    )

    api_resp = test_device.configure_delete(path=["interfaces", "dummy", "dum1"])
    assert isinstance(api_resp.result, dict)


def test_device_generate(monkeypatch, test_device):
    def mock_configure_delete(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {
            "success": True,
            "data": f"""'Generating public/private rsa key pair.\n'
                   'Your identification has been saved in '
                   '/tmp/key_{keyrand}\n'
                   'Your public key has been saved in '
                   '/tmp/key_39skBBzxc5NvIfE8GzQ7.pub\n'
                   'The key fingerprint is:\n'
                   'SHA256:7vfukWp093kyngUB+iH6'
                   'root@pyvyos-device\n'
                   "The key's randomart image is:\n"
                   '+---[RSA 3072]----+\n'
                   '|        .   .    |\n'
                   '|       o + . - . |\n'
                   '|      . = = = +  |\n'
                   '|       o + O - o.|\n'
                   '|      . S B . .oo|\n'
                   '|       o *. ..oo.|\n'
                   '|      . ....o. Eo|\n'
                   '|     . +...+ .o+o|\n'
                   '|      ..o=o++.oo.|\n'
                   '+----[SHA256]-----+\n'""",
            "error": None,
        }

        return response

    monkeypatch.setattr(
        RestClient,
        "_execute_request",
        mock_configure_delete,
    )

    randstring = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(20)
    )
    keyrand = f"/tmp/key_{randstring}"

    api_resp = test_device.generate(path=["ssh", "client-key", keyrand])
    assert isinstance(api_resp.result, str)
    assert keyrand in api_resp.result


def test_device_show(monkeypatch, test_device):
    def mock_show(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {
            "success": True,
            "data": """'Name                   Default boot    Running  \n'
                   '------------------------  --------------  --------- \n'
                   '1.5-rolling-202407300021       Yes           Yes    \n'
            """,
            "error": None,
        }
        return response

    monkeypatch.setattr(
        RestClient,
        "_execute_request",
        mock_show,
    )

    api_resp = test_device.show(path=["system", "image"])
    assert isinstance(api_resp.result, str)


def test_device_reset(monkeypatch, test_device):
    def mock_reset(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {
            "success": True,
            "data": """'conntrack-sync is not configured!\n'""",
            "error": None,
        }
        return response

    monkeypatch.setattr(
        RestClient,
        "_execute_request",
        mock_reset,
    )

    api_resp = test_device.reset(path=["system", "image"])
    assert isinstance(api_resp.result, str)


def test_device_config_file_save(monkeypatch, test_device):
    def mock_config_file_save(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {
            "success": True,
            "data": "",
            "error": None,
        }
        return response

    monkeypatch.setattr(
        RestClient,
        "_execute_request",
        mock_config_file_save,
    )

    api_resp = test_device.config_file_save(file="/config/teste.config")
    assert isinstance(api_resp.result, str)


def test_device_config_file_load(monkeypatch, test_device):
    def mock_config_file_save(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {
            "success": True,
            "data": None,
            "error": None,
        }
        return response

    monkeypatch.setattr(
        RestClient,
        "_execute_request",
        mock_config_file_save,
    )

    api_resp = test_device.config_file_load(file="/config/teste.config")
    assert api_resp


def test_device_configure_multiple_op(monkeypatch, test_device):
    def mock_config_file_save(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {
            "success": True,
            "data": None,
            "error": None,
        }
        return response

    monkeypatch.setattr(
        RestClient,
        "_execute_request",
        mock_config_file_save,
    )

    api_resp = test_device.configure_multiple_op(
        op_path=[
            {
                "op": "set",
                "path": ["interfaces", "dummy", "dum1", "address", "192.168.56.100/24"],
            },
            {
                "op": "delete",
                "path": ["interfaces", "dummy", "dum1"],
            },
        ]
    )
    assert api_resp


def test_device_invalid_path_multiple_op(monkeypatch, test_device):
    def mock_configure_set(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {
            "success": True,
            "data": {},
            "error": None,
        }

        return response

    monkeypatch.setattr(
        RestClient,
        "_execute_request",
        mock_configure_set,
    )
    with pytest.raises(ValueError):
        test_device.configure_multiple_op(op_path="interfaces")


def test_device_invalid_request(monkeypatch, test_device):
    def mock_invalid_request(*args, **kwargs):
        response = requests.Response()
        response.status_code = 400
        response.json = lambda: {
            "success": False,
            "data": None,
            "error": "Bad Request",
        }
        return response

    monkeypatch.setattr(
        RestClient,
        "_execute_request",
        mock_invalid_request,
    )

    api_resp = test_device.show(path=["invalid", "path"])
    assert not api_resp.result
    assert api_resp.status == 400
    assert "HTTP Error" in api_resp.error


def test_device_error_json_response(monkeypatch, test_device):
    def mock_error_json_response(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.data = "This is not a JSON response"
        return response

    monkeypatch.setattr(
        RestClient,
        "_execute_request",
        mock_error_json_response,
    )

    api_resp = test_device.show(path=["system", "image"])
    assert not api_resp.result
    assert "Invalid response format" in api_resp.error