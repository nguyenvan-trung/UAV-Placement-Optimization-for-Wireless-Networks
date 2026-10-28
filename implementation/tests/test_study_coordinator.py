"""Coordinator survives progress-file contention without touching real results."""
import importlib.util
from pathlib import Path
from unittest.mock import Mock

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/run_notebook_study.py'
spec = importlib.util.spec_from_file_location('study_coordinator', SCRIPT)
coordinator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(coordinator)


def test_transient_read_lock_retries_then_uses_new_progress(monkeypatch):
    path = Mock()
    path.read_text.side_effect = [PermissionError('locked'), '{"completed":12,"resumed":4}']
    sleep = Mock()
    monkeypatch.setattr(coordinator.time, 'sleep', sleep)
    assert coordinator.read_worker_progress(path, dict(completed=10, resumed=4)) == dict(completed=12, resumed=4)
    assert path.read_text.call_count == 2
    sleep.assert_called_once()


@pytest.mark.parametrize('error', [PermissionError('locked'), FileNotFoundError('replaced')])
def test_unavailable_progress_preserves_previous_snapshot(monkeypatch, error):
    path = Mock()
    path.read_text.side_effect = error
    monkeypatch.setattr(coordinator.time, 'sleep', lambda _: None)
    previous = dict(completed=42, resumed=20)
    assert coordinator.read_worker_progress(path, previous) is previous
    assert path.read_text.call_count == 5


def test_invalid_counts_are_not_silently_accepted():
    path = Mock()
    path.read_text.return_value = '{"completed":1,"resumed":2}'
    with pytest.raises(ValueError, match='Invalid worker progress'):
        coordinator.read_worker_progress(path, {})

def test_signature_error_is_not_masked_by_coordinator_progress(tmp_path, monkeypatch):
    import json
    root = tmp_path
    output = root / 'implementation/results/test'
    output.mkdir(parents=True)
    config = dict(output='implementation/results/test', seeds=[1, 2])
    config_path = root / 'config.json'
    config_path.write_text(json.dumps(config))
    (output / 'manifest.json').write_text(json.dumps(dict(signature='old', workers=1)))
    (output / 'progress.json').write_text(json.dumps(dict(completed=24, phase='aggregating')))
    monkeypatch.setattr(coordinator, 'ROOT', root)
    monkeypatch.setattr(coordinator.sys, 'argv', ['runner', '--config', str(config_path), '--workers', '1'])
    monkeypatch.setattr(coordinator, 'plan', lambda *a: ([root / 'data.csv'], [], 24))
    monkeypatch.setattr(coordinator, 'study_signature', lambda *a: 'new')
    with pytest.raises(ValueError, match='Source/config/data/worker count changed'):
        coordinator.main()
    status = json.loads((output / 'progress.json').read_text())
    assert status['phase'] == 'failed'
    assert status['completed'] == 24
    assert not (output / '.coordinator').exists()
