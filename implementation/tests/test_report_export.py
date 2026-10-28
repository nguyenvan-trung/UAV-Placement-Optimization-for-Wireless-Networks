"""Separate reporting entry point: reject incomplete studies before rendering."""
import importlib.util
import json
from pathlib import Path
from unittest.mock import Mock
import pytest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/export_study_report.py'
spec = importlib.util.spec_from_file_location('report_export', SCRIPT)
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


def test_incomplete_results_do_not_render_or_mark_complete(tmp_path, monkeypatch):
    output = tmp_path / 'implementation/results/old'
    output.mkdir(parents=True)
    (output / 'manifest.json').write_text(json.dumps(dict(signature='original')))
    monkeypatch.setattr(exporter, 'build_tables', Mock(side_effect=ValueError('Study incomplete')))
    render = Mock()
    monkeypatch.setattr(exporter, 'build_report', render)
    with pytest.raises(ValueError, match='Study incomplete'):
        exporter.export_report(tmp_path, output)
    render.assert_not_called()
    assert not (output / 'report_completion.json').exists()


def test_report_uses_saved_artifacts_and_preserves_optimization_status(tmp_path, monkeypatch):
    import pandas as pd
    output = tmp_path / 'implementation/results/old'
    output.mkdir(parents=True)
    (output / 'manifest.json').write_text(json.dumps(dict(signature='original')))
    status = output / 'progress.json'
    status.write_text('{"phase":"aggregating"}')
    tables = {'main': pd.DataFrame()}
    monkeypatch.setattr(exporter, 'build_tables', lambda _: tables)
    monkeypatch.setattr(exporter, 'read_results', lambda _: (pd.DataFrame([dict(fitness=.4)]), None))
    csv = Mock()
    render = Mock()
    monkeypatch.setattr(exporter, 'export_dataset_csv', csv)
    monkeypatch.setattr(exporter, 'build_report', render)
    exporter.export_report(tmp_path, output)
    render.assert_called_once_with(tmp_path, output, tables)
    csv.assert_called_once_with(output)
    assert status.read_text() == '{"phase":"aggregating"}'
    assert json.loads((output / 'report_completion.json').read_text())['source_signature'] == 'original'
