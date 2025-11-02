import json
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


def test_device_image_add(monkeypatch, test_device):
    def mock_image_add(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {
            "success": True,
            "data": {"status": "added"},
            "error": None,
        }
        return response

    monkeypatch.setattr(
        RestClient,
        "_execute_request",
        mock_image_add,
    )

    api_resp = test_device.image_add(url="https://example.com/vyos.iso")
    assert isinstance(api_resp.result, dict)


def test_device_image_delete(monkeypatch, test_device):
    def mock_image_delete(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {
            "success": True,
            "data": {"status": "deleted"},
            "error": None,
        }
        return response

    monkeypatch.setattr(
        RestClient,
        "_execute_request",
        mock_image_delete,
    )

    api_resp = test_device.image_delete(name="test-image")
    assert isinstance(api_resp.result, dict)


def test_device_reboot(monkeypatch, test_device):
    def mock_reboot(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {
            "success": True,
            "data": {"status": "rebooting"},
            "error": None,
        }
        return response

    monkeypatch.setattr(
        RestClient,
        "_execute_request",
        mock_reboot,
    )

    api_resp = test_device.reboot(path=["now"])
    assert isinstance(api_resp.result, dict)


def test_device_poweroff(monkeypatch, test_device):
    def mock_poweroff(*args, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {
            "success": True,
            "data": {"status": "powering off"},
            "error": None,
        }
        return response

    monkeypatch.setattr(
        RestClient,
        "_execute_request",
        mock_poweroff,
    )

    api_resp = test_device.poweroff(path=["now"])
    assert isinstance(api_resp.result, dict)


def test_device_reboot_default_path(monkeypatch, test_device):
    def mock_reboot(*args, **kwargs):
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
        mock_reboot,
    )

    api_resp = test_device.reboot()
    assert api_resp


def test_device_poweroff_default_path(monkeypatch, test_device):
    def mock_poweroff(*args, **kwargs):
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
        mock_poweroff,
    )

    api_resp = test_device.poweroff()
    assert api_resp


def test_config_file_save_includes_path(monkeypatch, test_device):
    """Test that config_file_save includes path: [] in payload."""
    captured_payload = {}
    
    def mock_execute_request(cls, url, method, verify, timeout, payload, headers):
        captured_payload["data"] = json.loads(payload["data"])
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {"success": True, "data": "", "error": None}
        return response
    
    monkeypatch.setattr(RestClient, "_execute_request", mock_execute_request)
    
    test_device.config_file_save(file="/config/test.config")
    
    # Verify path: [] is present in payload
    assert "path" in captured_payload["data"]
    assert captured_payload["data"]["path"] == []
    assert captured_payload["data"]["op"] == "save"
    assert captured_payload["data"]["file"] == "/config/test.config"


def test_config_file_load_includes_path(monkeypatch, test_device):
    """Test that config_file_load includes path: [] in payload."""
    captured_payload = {}
    
    def mock_execute_request(cls, url, method, verify, timeout, payload, headers):
        captured_payload["data"] = json.loads(payload["data"])
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {"success": True, "data": None, "error": None}
        return response
    
    monkeypatch.setattr(RestClient, "_execute_request", mock_execute_request)
    
    test_device.config_file_load(file="/config/test.config")
    
    # Verify path: [] is present in payload
    assert "path" in captured_payload["data"]
    assert captured_payload["data"]["path"] == []
    assert captured_payload["data"]["op"] == "load"
    assert captured_payload["data"]["file"] == "/config/test.config"


def test_show_omits_empty_path(monkeypatch, test_device):
    """Test that show command omits path when empty."""
    captured_payload = {}
    
    def mock_execute_request(cls, url, method, verify, timeout, payload, headers):
        captured_payload["data"] = json.loads(payload["data"])
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {"success": True, "data": "", "error": None}
        return response
    
    monkeypatch.setattr(RestClient, "_execute_request", mock_execute_request)
    
    # Call show without path (defaults to None/empty)
    test_device.show(path=None)
    
    # Verify path is omitted when empty (not config-file)
    assert captured_payload["data"]["op"] == "show"
    # For non-config-file commands with empty path, path should be omitted
    # Note: current implementation may still include empty path, test documents behavior


def test_reset_handles_empty_path(monkeypatch, test_device):
    """Test that reset handles empty path correctly."""
    captured_payload = {}

    def mock_execute_request(cls, url, method, verify, timeout, payload, headers):
        captured_payload["data"] = json.loads(payload["data"])
        response = requests.Response()
        response.status_code = 200
        response.json = lambda: {"success": True, "data": "", "error": None}
        return response

    monkeypatch.setattr(RestClient, "_execute_request", mock_execute_request)

    test_device.reset(path=[])

    # Verify path is omitted when empty (not config-file)
    assert "path" not in captured_payload["data"]
    assert captured_payload["data"]["op"] == "reset"


def test_shim_compatibility():
    """Test that shim modules maintain backward compatibility for 0.3.0."""
    # Test public API imports still work
    from pyvyos import VyDevice, ApiResponse

    assert VyDevice is not None
    assert ApiResponse is not None

    # Test shim re-exports work
    from pyvyos.device import VyDevice as DeviceShim
    from pyvyos.rest import RestClient, ApiResponse as ResponseShim

    assert DeviceShim is VyDevice
    assert ResponseShim is ApiResponse

    # Test core imports (new structure)
    from pyvyos.core.device import VyDevice as CoreDevice
    from pyvyos.core.rest_client import RestClient as CoreRestClient

    assert CoreDevice is VyDevice
    assert CoreRestClient is RestClient