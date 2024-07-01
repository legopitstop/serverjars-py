import serverjars
import pytest


@pytest.mark.parametrize(
    "type, category",
    [
        ("vanilla", "release"),
        ("vanilla", "snapshot"),
        ("modded", "banner"),
        ("modded", "fabric"),
        ("modded", "mohist"),
    ],
)
def test_fetch_details(type, category):
    details = serverjars.fetch_details(type=type, category=category)
    assert isinstance(details, serverjars.SoftwareFile)
