"""Tests for pyvyos.utils.paths module."""

from pyvyos.utils.paths import build_path


def test_build_path_strings():
    """Test building path from string segments."""
    result = build_path("interfaces", "ethernet", "eth0")
    assert result == ["interfaces", "ethernet", "eth0"]


def test_build_path_mixed():
    """Test building path from mixed strings and lists."""
    result = build_path(["interfaces", "ethernet"], "eth0", "address")
    assert result == ["interfaces", "ethernet", "eth0", "address"]


def test_build_path_empty():
    """Test building path with no arguments."""
    result = build_path()
    assert result == []


def test_build_path_single_list():
    """Test building path with single list."""
    result = build_path(["interfaces", "ethernet"])
    assert result == ["interfaces", "ethernet"]


def test_build_path_multiple_lists():
    """Test building path with multiple lists."""
    result = build_path(["interfaces"], ["ethernet"], ["eth0"])
    assert result == ["interfaces", "ethernet", "eth0"]

