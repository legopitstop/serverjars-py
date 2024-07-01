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
def test_fetch_jar(type, category):
    res = serverjars.fetch_jar(type, category)
    assert res.status_code is 200
