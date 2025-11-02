"""Tests for pyvyos.utils.ids module."""

import uuid

from pyvyos.utils.ids import request_id


def test_request_id_returns_string():
    """Test that request_id returns a string."""
    rid = request_id()
    assert isinstance(rid, str)


def test_request_id_valid_uuid():
    """Test that request_id returns a valid UUID."""
    rid = request_id()
    uuid.UUID(rid)  # Should not raise


def test_request_id_unique():
    """Test that request_id generates unique IDs."""
    id1 = request_id()
    id2 = request_id()
    assert id1 != id2

