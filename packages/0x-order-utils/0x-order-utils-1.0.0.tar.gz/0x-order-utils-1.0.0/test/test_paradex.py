"""Test the code given to us by Paradex."""

import json
from pkg_resources import resource_string

import pytest

from zero_ex.order_utils import _Constants

# generate_order_hash_hex,
# make_empty_order,
# NULL_ADDRESS,

# from zerox_v2 import ZRXOrder


def get_contract_abi(contract_name: str) -> str:
    """Get the ABI object for the named contract."""
    contract_name_to_artifact_file_name = {
        "Exchange": "artifacts/Exchange.json"
    }
    if contract_name not in contract_name_to_artifact_file_name:
        raise ValueError(f"Unknown contract '{contract_name}'")

    if not hasattr(get_contract_abi, "abis"):  # type: ignore
        get_contract_abi.abis = {}  # type: ignore

    if contract_name not in get_contract_abi.abis:  # type: ignore
        get_contract_abi.abis[contract_name] = json.loads(  # type: ignore
            resource_string(
                "zero_ex.contract_artifacts",
                contract_name_to_artifact_file_name[contract_name],
            )
        )["compilerOutput"]["abi"]

    return get_contract_abi.abis[contract_name]  # type: ignore


def test_get_contract_abi():
    """Test it."""
    with pytest.raises(ValueError):
        get_contract_abi("asdf")

    assert (
        get_contract_abi("Exchange")
        == _Constants.contract_name_to_abi["Exchange"]
    )


def skip_test_zrxorder_sign():
    """Test signing an order through the object interface."""
    # order = ZRXOrder()
    # order.order_hash = generate_order_hash_hex(
    # make_empty_order(), NULL_ADDRESS
    # )
    signature = (  # order.sign(
        "c10c9a5b3a1b0f74b415f1b8afa7b494f63f8ee67935db41776007ac77380002"
    )
    assert signature == "deadbeef"
