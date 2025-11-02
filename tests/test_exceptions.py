"""Tests for pyvyos.exceptions module."""

import pytest

from pyvyos.exceptions import SDKError, HttpError, ApiError, ValidationError


def test_sdk_error_base():
    """Test SDKError is base exception."""
    assert issubclass(HttpError, SDKError)
    assert issubclass(ApiError, SDKError)
    assert issubclass(ValidationError, SDKError)


def test_http_error():
    """Test HttpError creation and attributes."""
    error = HttpError(status=404, message="Not Found")
    assert error.status == 404
    assert error.message == "Not Found"
    assert "404" in str(error)
    assert "Not Found" in str(error)


def test_api_error():
    """Test ApiError creation."""
    error = ApiError(message="API failure")
    assert error.message == "API failure"
    assert "API failure" in str(error)


def test_api_error_with_details():
    """Test ApiError with details."""
    details = {"code": "ERR001", "field": "path"}
    error = ApiError(message="Validation failed", details=details)
    assert error.message == "Validation failed"
    assert error.details == details


def test_validation_error():
    """Test ValidationError creation."""
    error = ValidationError(message="Invalid path format")
    assert error.message == "Invalid path format"
    assert "Invalid path format" in str(error)


def test_exceptions_raiseable():
    """Test that exceptions can be raised and caught."""
    with pytest.raises(HttpError) as exc_info:
        raise HttpError(status=500, message="Internal Error")
    assert exc_info.value.status == 500

