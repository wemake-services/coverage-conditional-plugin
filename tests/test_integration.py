import json
import sys
from pathlib import Path

import pytest
from coverage import Coverage

from test_project.example import (
    always,
    if_gte_python36,
    if_gte_python37,
    if_gte_python38,
    if_gte_python39,
    if_gte_python310,
)

#: This is just our specific example.
_EXCUDED_LINES = (sys.version_info[1] - 6) * 3 + 6
# 3.9 = 15
# 3.8 = 12
# 3.7 = 9
# 3.6 = 6


def test_integration(cov, capsys):
    """Ensures that coverage is executed correctly."""
    # We call all functions without any actual version checks.
    if_gte_python36()
    if_gte_python37()
    if_gte_python38()
    if_gte_python39()
    if_gte_python310()
    always()

    cov.json_report(outfile='-')
    captured = capsys.readouterr()
    coverage = json.loads(captured.out)

    assert len(
        coverage['files']['test_project/example.py']['excluded_lines'],
    ) == _EXCUDED_LINES
    assert int(coverage['totals']['percent_covered']) >= 80
    assert coverage['totals']['missing_lines'] == 1


@pytest.mark.parametrize('configfile', ['.coveragerc', 'pyproject.toml'])
def test_config_file_parsing(configfile):
    """Ensures that coverage is executed correctly."""
    config_file_path = Path(__file__).parents[1] / 'test_project' / configfile

    cov = Coverage(config_file=str(config_file_path))
    assert cov.config.config_file == str(config_file_path)
    assert cov.config.plugins == ['coverage_conditional_plugin']

    cov.start()
    cov.stop()

    assert (
        'py-gte-3{minor_ver}'.format(minor_ver=sys.version_info[1])
        in cov.config.exclude_list
    )
