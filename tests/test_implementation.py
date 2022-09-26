from coverage_conditional_plugin import _is_installed
from coverage_conditional_plugin.version import package_version


def test_is_installed():
    """Ensures that ``_is_installed`` works correctly."""
    assert _is_installed('coverage') is True  # regular dependency
    assert _is_installed('pytest') is True  # dev dependency
    assert _is_installed('missing') is False  # missing dependency


def test_package_version():
    """Ensures that ``_package_version`` is correct."""
    coverage_version = package_version('coverage')
    pytest_version = package_version('pytest')

    assert coverage_version is not None
    assert coverage_version < (1000, 0, 0)
    assert pytest_version is not None
    assert pytest_version > (5, 0)
