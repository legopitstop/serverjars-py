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
def test_fetch_all(type, category):
    all = serverjars.fetch_all(type=type, category=category, max=3)
    assert isinstance(all, list)
