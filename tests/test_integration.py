# -*- coding: utf-8 -*-

import json
import sys

from test_project.example import (
    always,
    if_gte_python36,
    if_gte_python37,
    if_gte_python38,
)

#: This is just our specific example.
_EXCUDED_LINES = (10 - sys.version_info[1]) * 3


def test_integration(cov, capsys):
    """Ensures that coverage is executed correctly."""
    assert if_gte_python36() != if_gte_python37() != if_gte_python38()
    assert always() == 'always'

    cov.json_report(outfile='-')
    captured = capsys.readouterr()
    coverage = json.loads(captured.out)

    assert len(
        coverage['files']['test_project/example.py']['excluded_lines'],
    ) == _EXCUDED_LINES
    assert int(coverage['totals']['percent_covered']) == 85
    assert coverage['totals']['missing_lines'] == 1
