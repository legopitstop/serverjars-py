import serverjars
import pytest


@pytest.mark.parametrize("type", [("vanilla"), ("modded")])
def test_fetch_types(type):
    types = serverjars.fetch_types(type)
    assert isinstance(types, list)
