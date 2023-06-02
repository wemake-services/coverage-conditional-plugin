from pathlib import Path

import pytest
from coverage import Coverage

_OMIT_DEFAULT = 'test_project/missing.py'
_OMIT_GLOB = 'test_project/omit*.py'
_OMIT_FILE = 'test_project/compat.py'


@pytest.mark.parametrize(('env_key', 'omits'), [
    ('OMIT1', [_OMIT_DEFAULT, _OMIT_GLOB, _OMIT_FILE]),
    ('OMIT2', [_OMIT_DEFAULT, _OMIT_FILE]),
])
def test_omit1(monkeypatch, env_key, omits):
    """Ensures that coverage is executed correctly."""
    monkeypatch.setenv(env_key, '1')
    config_file_path = (
        Path(__file__).parents[1] / 'test_project' / 'pyproject.toml'
    )

    cov = Coverage(config_file=str(config_file_path))

    cov.start()
    cov.stop()

    assert cov.config.run_omit == omits
