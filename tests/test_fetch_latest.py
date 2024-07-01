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
def test_fetch_latest(type, category):
    latest = serverjars.fetch_latest(type, category)
    assert isinstance(latest, serverjars.SoftwareFile)
