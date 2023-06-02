import pytest

from coverage_conditional_plugin import _should_be_applied


@pytest.mark.parametrize('code', [
    'True or False',
    'bool(1 + 2)',

    'sys_version_info > (3,)',
    'bool(os_name)',
    '"PATH" in os_environ',
    'isinstance(platform_system, str)',
    'len(platform_release) > 1',
    'is_installed("pytest")',
    'package_version("pytest") > (5,)',
])
def test_plugin_should_be_applied(code):
    """Ensures code is evaluated correctly."""
    assert _should_be_applied(code) is True
