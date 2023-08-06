"""Test zero_ex.json_schemas.*."""

import pytest
import jsonschema.exceptions

from zero_ex.json_schemas import assert_valid


def test_assert_valid__no_such_ref():
    """Test that passing an invalid ref id raises an exception."""
    with pytest.raises(jsonschema.exceptions.ValidationError):
        assert_valid({}, "asdf")


def test_assert_valid__missing_field():
    """Test that passing in an object with a missing field raises an exception.
    """
    with pytest.raises(jsonschema.exceptions.ValidationError):
        assert_valid(
            {"v": 27, "r": "0x" + "f" * 64},  # missing 's' property
            "/ECSignature",
        )
