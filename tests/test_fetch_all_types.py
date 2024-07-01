import serverjars


def test_fetch_all():
    types = serverjars.fetch_all_types()
    assert isinstance(types, dict)
