import pytest
import serverjars
from serverjars.software import SERVICES

REQUESTED_VERSIONS = [f"1.21.{i}" for i in range(1, 12)] + [
    "26.1",
    "26.1.1",
    "26.1.2",
    "26.2",
    "26.3",
]

CATEGORIES = [
    ("vanilla", "release"),
    ("vanilla", "snapshot"),
    ("modded", "banner"),
    ("modded", "fabric"),
    ("modded", "mohist"),
]


def _print_jars(label, jars):
    print(f"\n== {label} ({len(jars)} jars) ==")
    for j in jars:
        print(
            f"  {j.version:<18} stability={j.stability:<8} built={j.built} "
            f"size={j.size.display:<11} download={j.download}"
        )


@pytest.mark.parametrize("type, category", CATEGORIES)
def test_fetch_all_prints_output(type, category):
    jars = serverjars.fetch_all(type=type, category=category, max=3)
    _print_jars(f"fetch_all {type}/{category} max=3", jars)
    assert len(jars) == 3
    for j in jars:
        assert j.version
        assert j.hash
        assert j.download.startswith("https://")


@pytest.mark.parametrize("type, category", CATEGORIES)
def test_fetch_latest_prints_output(type, category):
    jar = serverjars.fetch_latest(type=type, category=category)
    _print_jars(f"fetch_latest {type}/{category}", [jar])
    assert jar.version


@pytest.mark.parametrize(
    "type, category", [("vanilla", "release"), ("modded", "fabric")]
)
def test_requested_versions_available(type, category):
    builder = next(c for c in SERVICES[type] if c.category == category)
    available = builder.available_versions()
    missing = [v for v in REQUESTED_VERSIONS if v not in available]
    print(f"\n== {type}/{category}: requested versions available ==")
    for v in REQUESTED_VERSIONS:
        print(f"  {v:<8} {'yes' if v in available else 'MISSING'}")
    assert not missing, f"missing from {type}/{category}: {missing}"
