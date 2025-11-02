"""Comprehensive tests for backward compatibility shims.

These tests ensure that all import paths from version 0.3.0 continue to work
after the internal refactoring to pyvyos.core structure.
"""

import pytest

from pyvyos import VyDevice, ApiResponse


class TestPublicAPIImports:
    """Test public API imports (from pyvyos import ...)."""

    def test_public_vydevice_import(self):
        """Test that VyDevice can be imported from pyvyos."""
        from pyvyos import VyDevice

        assert VyDevice is not None
        assert callable(VyDevice)

    def test_public_apiresponse_import(self):
        """Test that ApiResponse can be imported from pyvyos."""
        from pyvyos import ApiResponse

        assert ApiResponse is not None

    def test_public_both_imports(self):
        """Test importing both classes together."""
        from pyvyos import VyDevice, ApiResponse

        assert VyDevice is not None
        assert ApiResponse is not None


class TestShimModuleImports:
    """Test direct imports from shim modules (backward compatibility)."""

    def test_device_shim_vydevice(self):
        """Test importing VyDevice from pyvyos.device shim."""
        from pyvyos.device import VyDevice as DeviceShim
        from pyvyos import VyDevice

        assert DeviceShim is VyDevice
        assert DeviceShim is not None

    def test_device_shim_apiresponse(self):
        """Test importing ApiResponse from pyvyos.device shim."""
        from pyvyos.device import ApiResponse as ResponseShim
        from pyvyos import ApiResponse

        assert ResponseShim is ApiResponse

    def test_rest_shim_apiresponse(self):
        """Test importing ApiResponse from pyvyos.rest shim."""
        from pyvyos.rest import ApiResponse as RestResponseShim
        from pyvyos import ApiResponse

        assert RestResponseShim is ApiResponse

    def test_rest_shim_restclient(self):
        """Test importing RestClient from pyvyos.rest shim."""
        from pyvyos.rest import RestClient
        from pyvyos.core.rest_client import RestClient as CoreRestClient

        assert RestClient is CoreRestClient
        assert RestClient is not None


class TestCoreModuleImports:
    """Test imports from new core structure."""

    def test_core_device_import(self):
        """Test importing VyDevice from pyvyos.core.device."""
        from pyvyos.core.device import VyDevice as CoreDevice
        from pyvyos import VyDevice

        assert CoreDevice is VyDevice

    def test_core_rest_client_imports(self):
        """Test importing from pyvyos.core.rest_client."""
        from pyvyos.core.rest_client import RestClient, ApiResponse
        from pyvyos import ApiResponse as PublicResponse
        from pyvyos.rest import RestClient as ShimRestClient

        assert ApiResponse is PublicResponse
        assert RestClient is ShimRestClient


class TestShimIdentity:
    """Test that shims are identical objects, not copies."""

    def test_device_shim_identity(self):
        """Test that pyvyos.device.VyDevice is the same object as pyvyos.VyDevice."""
        from pyvyos import VyDevice
        from pyvyos.device import VyDevice as DeviceShim

        assert DeviceShim is VyDevice
        assert id(DeviceShim) == id(VyDevice)

    def test_rest_shim_identity(self):
        """Test that pyvyos.rest.RestClient is the same object as pyvyos.core.rest_client.RestClient."""
        from pyvyos.core.rest_client import RestClient as CoreRestClient
        from pyvyos.rest import RestClient

        assert RestClient is CoreRestClient
        assert id(RestClient) == id(CoreRestClient)

    def test_api_response_identity_across_modules(self):
        """Test that ApiResponse is the same object across all import paths."""
        from pyvyos import ApiResponse
        from pyvyos.device import ApiResponse as DeviceResponse
        from pyvyos.rest import ApiResponse as RestResponse
        from pyvyos.core.rest_client import ApiResponse as CoreResponse

        assert DeviceResponse is ApiResponse
        assert RestResponse is ApiResponse
        assert CoreResponse is ApiResponse
        assert id(DeviceResponse) == id(RestResponse) == id(CoreResponse)


class TestShimFunctionality:
    """Test that shim modules maintain full functionality."""

    def test_device_shim_instantiation(self):
        """Test that VyDevice can be instantiated via shim."""
        from pyvyos.device import VyDevice

        device = VyDevice(
            hostname="localhost",
            apikey="test_key",
            port=443,
            protocol="https",
            verify=False,
        )

        assert device.hostname == "localhost"
        assert device.apikey == "test_key"
        assert isinstance(device, VyDevice)

    def test_device_shim_methods_available(self):
        """Test that all VyDevice methods are available via shim."""
        from pyvyos.device import VyDevice

        device = VyDevice(
            hostname="localhost", apikey="test_key", verify=False, timeout=1
        )

        # Check that methods exist
        assert hasattr(device, "configure_set")
        assert hasattr(device, "configure_delete")
        assert hasattr(device, "retrieve_show_config")
        assert hasattr(device, "show")
        assert hasattr(device, "config_file_save")
        assert hasattr(device, "config_file_load")

    def test_rest_client_shim_instantiation(self):
        """Test that RestClient can be instantiated via shim."""
        from pyvyos.rest import RestClient

        client = RestClient(
            hostname="localhost",
            apikey="test_key",
            port=443,
            protocol="https",
            verify=False,
        )

        assert client.hostname == "localhost"
        assert isinstance(client, RestClient)

    def test_api_response_dataclass(self):
        """Test that ApiResponse dataclass works correctly."""
        from pyvyos import ApiResponse
        from pyvyos.rest import ApiResponse as RestApiResponse
        from pyvyos.core.rest_client import ApiResponse as CoreApiResponse

        # All should be the same class
        assert ApiResponse is RestApiResponse
        assert RestApiResponse is CoreApiResponse

        # Can instantiate
        response = ApiResponse(
            status=200, request={}, result={"data": "test"}, error=""
        )
        assert response.status == 200
        assert response.result == {"data": "test"}


class TestShimAllExports:
    """Test that __all__ exports are correct."""

    def test_device_shim_all(self):
        """Test pyvyos.device.__all__."""
        import pyvyos.device as device_module

        assert "VyDevice" in device_module.__all__
        assert "ApiResponse" in device_module.__all__
        assert len(device_module.__all__) == 2

    def test_rest_shim_all(self):
        """Test pyvyos.rest.__all__."""
        import pyvyos.rest as rest_module

        assert "ApiResponse" in rest_module.__all__
        assert "RestClient" in rest_module.__all__
        assert len(rest_module.__all__) == 2

    def test_main_init_all(self):
        """Test pyvyos.__init__.__all__."""
        import pyvyos as main_module

        assert "VyDevice" in main_module.__all__
        assert "ApiResponse" in main_module.__all__
        assert len(main_module.__all__) == 2

