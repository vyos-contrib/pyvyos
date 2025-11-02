"""Tests for pyvyos.utils.json module."""

import pytest

from pyvyos.utils.json import redact_key, safe_dumps


def test_redact_key_single_key():
    """Test redacting a single key."""
    data = {"key": "secret", "other": "visible"}
    result = redact_key(data)
    assert result["key"] == "***REDACTED***"
    assert result["other"] == "visible"


def test_redact_key_multiple_keys():
    """Test redacting multiple keys."""
    data = {"key": "secret", "password": "pass123", "apikey": "api_key", "visible": "data"}
    result = redact_key(data, keys=["key", "password", "apikey"])
    assert result["key"] == "***REDACTED***"
    assert result["password"] == "***REDACTED***"
    assert result["apikey"] == "***REDACTED***"
    assert result["visible"] == "data"


def test_redact_key_default_keys():
    """Test redacting with default keys."""
    data = {"key": "secret", "apikey": "api", "password": "pass", "data": "ok"}
    result = redact_key(data)
    assert result["key"] == "***REDACTED***"
    assert result["apikey"] == "***REDACTED***"
    assert result["password"] == "***REDACTED***"
    assert result["data"] == "ok"


def test_redact_key_copies_data():
    """Test that redact_key returns a copy, not original."""
    data = {"key": "secret"}
    result = redact_key(data)
    result["new"] = "value"
    assert "new" not in data
    assert data["key"] == "secret"  # Original unchanged


def test_safe_dumps_with_dict():
    """Test safe_dumps with dictionary."""
    data = {"key": "secret", "data": "visible"}
    result = safe_dumps(data)
    assert "***REDACTED***" in result
    assert "secret" not in result
    assert "visible" in result


def test_safe_dumps_with_list():
    """Test safe_dumps with list."""
    data = [1, 2, 3]
    result = safe_dumps(data)
    assert result == "[1, 2, 3]"


def test_safe_dumps_with_custom_keys():
    """Test safe_dumps with custom redaction keys."""
    data = {"sensitive": "hide", "public": "show"}
    result = safe_dumps(data, redact_keys=["sensitive"])
    assert "***REDACTED***" in result
    assert "hide" not in result
    assert "show" in result

