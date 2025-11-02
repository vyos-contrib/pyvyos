#!/usr/bin/env python3
"""Quick test script to verify imports and shims work."""

def test_imports():
    """Test all import paths."""
    print("Testing imports...")
    
    # Public API
    from pyvyos import VyDevice, ApiResponse
    print("✓ Public API imports work")
    
    # Shim modules
    from pyvyos.device import VyDevice as DeviceShim
    from pyvyos.rest import RestClient, ApiResponse as RestResponse
    print("✓ Shim module imports work")
    
    # Core modules
    from pyvyos.core.device import VyDevice as CoreDevice
    from pyvyos.core.rest_client import RestClient as CoreRestClient
    print("✓ Core module imports work")
    
    # Identity checks
    assert DeviceShim is VyDevice, "Device shim identity failed"
    assert RestResponse is ApiResponse, "Rest shim identity failed"
    assert CoreDevice is VyDevice, "Core device identity failed"
    print("✓ All identity checks pass")
    
    # Utils
    from pyvyos.utils import redact_key, request_id, build_path
    print("✓ Utils imports work")
    
    # Exceptions
    from pyvyos.exceptions import SDKError, HttpError, ApiError, ValidationError
    print("✓ Exceptions imports work")
    
    print("\n✅ All imports and shims working correctly!")

if __name__ == "__main__":
    test_imports()

