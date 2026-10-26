"""Contract checks only: these tests never run UAV optimizers or the CSV study."""
from pathlib import Path
import json
from types import SimpleNamespace

import numpy as np
import pytest

from src.notebook_study import (cases, make_case, run_study, ObservedProblem, validate_task,
    task_destination, task_filename, atomic_json, read_results, task_paths, export_dataset_csv)
from src.algorithms.base.budget import initialize_paired, iterations
from src.algorithms.base.enhancements import enhance, opposition
from src.algorithms.PSO.particle import Particle


def test_registry_constructs_all_thirty_cases():
    registry = cases()
    assert len(registry) == len({r['case'] for r in registry}) == 30
    for family in ('WOA', 'PSO', 'GA'):
        flags = {(c['K'], c['O'], c['L']) for c in registry if c['family'] == family}
        assert len(flags) == 8
    for row in registry:
        optimizer = make_case(row, 25, 100, 42)
        assert getattr(optimizer.params, 'generations', getattr(optimizer.params, 'iterations', None)) == 100


def test_no_confirmation_cannot_create_output():
    with pytest.raises(RuntimeError, match='disabled'):
        run_study(None, {}, confirmed=False)  # Must refuse before accessing any path.


def test_disabled_operators_preserve_population_and_rng():
    population = [object()]
    rng = np.random.default_rng(42)
    params = SimpleNamespace(use_obl=False, use_levy=False)
    assert enhance(population, None, params, rng, None) is population
    assert rng.random() == np.random.default_rng(42).random()


def test_pso_opposition_resets_velocity_and_preserves_better_pbest():
    particle = Particle(np.array([.2]), np.array([.1]), np.array([.9]), .2, .9)
    problem = SimpleNamespace(search_space=SimpleNamespace(clip=lambda x: np.clip(x, 0, 1)),
        evaluate=lambda x: float(x[0]))
    selected = opposition([particle], problem, np.array([0.]), np.array([1.]))[0]
    assert selected.position[0] == pytest.approx(.8)
    assert selected.velocity[0] == 0
    assert selected.best_position[0] == .9 and selected.best_fitness == .9
    assert particle.position[0] == .2  # Original object was not overwritten.


def test_iteration_observer_records_initial_and_final_without_extra_fe():
    class ToyProblem:
        def evaluate(self, value):
            return float(value[0])

        def evaluate_detailed(self, value):
            return SimpleNamespace(coverage_rate=.5, energy_normalized=.2, interference_rate=.1)

    observed = ObservedProblem(ToyProblem(), np.array([[0.]]))
    individual = SimpleNamespace(position=np.array([-1.]))
    initialize_paired([individual], observed)
    assert individual.position[0] == 0
    observed.evaluate(np.array([0.]))
    for index in iterations(observed, 100):
        observed.evaluate(np.array([index + 1.]))
    assert [r['iteration'] for r in observed.history] == list(range(101))
    assert observed.fe == 101 and observed.history[-1]['fitness'] == 100


def test_notebook_run_gate_is_off():
    root = Path(__file__).resolve().parents[2]
    notebook = json.loads((root / 'implementation/notebooks/full_study_100_iterations.ipynb').read_text(encoding='utf-8'))
    code = [c for c in notebook['cells'] if c['cell_type'] == 'code']
    assert any('CONFIRM_RUN = False' in ''.join(c['source']) for c in code)
    config = json.loads((root / 'configs/notebook_study.json').read_text())
    assert len(config['seeds']) == len(set(config['seeds'])) == 30


def valid_artifact():
    rows = [dict(iteration=i, fitness=.3+i/10000, coverage=.9, energy=.7, interference=.1,
                 fe=25+i*25, elapsed_s=i/100, position=[10., 10., 100.]) for i in range(101)]
    final = rows[-1]
    record = dict(dataset='sample.csv', case='GA', seed=42, feasible=True,
        fitness=final['fitness'], coverage=.9, energy=.7, interference=.1,
        fe=final['fe'], wall_s=final['elapsed_s'], optimizer_fitness=final['fitness'])
    return dict(result=record, history=rows)


def test_validator_accepts_complete_matched_task():
    assert validate_task(valid_artifact(), dataset='sample.csv', case='GA', seed=42)['fe'] == 2525


def test_atomic_json_retries_a_transient_windows_file_lock(tmp_path, monkeypatch):
    original = Path.replace
    attempts = []

    def briefly_locked(source, target):
        attempts.append(target)
        if len(attempts) < 3:
            raise PermissionError('Destination is temporarily locked')
        return original(source, target)

    monkeypatch.setattr(Path, 'replace', briefly_locked)
    monkeypatch.setattr('src.notebook_study.time.sleep', lambda _: None)
    path = tmp_path / 'progress.json'
    path.write_text('{"completed":0}')
    atomic_json(path, {'completed': 1})
    assert json.loads(path.read_text()) == {'completed': 1}
    assert len(attempts) == 3


def test_atomic_json_reports_persistent_write_failure(tmp_path, monkeypatch):
    def always_locked(source, target):
        raise PermissionError('Destination remains locked')

    monkeypatch.setattr(Path, 'replace', always_locked)
    monkeypatch.setattr('src.notebook_study.time.sleep', lambda _: None)
    path = tmp_path / 'progress.json'
    path.write_text('{"completed":0}')
    with pytest.raises(PermissionError):
        atomic_json(path, {'completed': 1})
    assert json.loads(path.read_text()) == {'completed': 0}


def test_dataset_named_results_can_be_read_from_worker_shards(tmp_path):
    dataset = '001_UAV_3D_50_users_connect.csv'
    output = tmp_path / 'shards' / 'worker_00'
    path = task_destination(output, dataset, 'GA', 42)
    assert path.relative_to(output).as_posix() == (
        'tasks/001_UAV_3D_50/001_UAV_3D_50_result_GA_seed42.json.gz')
    assert task_filename(dataset, 'PSO', 42) != path.name
    assert task_filename(dataset, 'GA', 123) != path.name
    artifact = valid_artifact()
    artifact['result']['dataset'] = dataset
    path.parent.mkdir(parents=True)
    atomic_json(path, artifact)
    assert task_paths(tmp_path) == [path]
    results, _ = read_results(tmp_path)
    assert results.iloc[0]['dataset'] == dataset
    assert results.iloc[0]['case'] == 'GA'

    other = valid_artifact()
    other['result'].update(dataset=dataset, case='PSO')
    atomic_json(task_destination(output, dataset, 'PSO', 42), other)
    export_dataset_csv(tmp_path)
    import pandas as pd
    folder = tmp_path / 'datasets' / '001_UAV_3D_50'
    result_file = folder / '001_UAV_3D_50_result.csv'
    exported = pd.read_csv(result_file)
    assert set(exported['case']) == {'GA', 'PSO'}
    assert exported.fitness.tolist() == pytest.approx([.31, .31])
    assert result_file.read_bytes().startswith(b'\xef\xbb\xbf')
    positions = pd.read_csv(folder / '001_UAV_3D_50_positions.csv')
    assert positions[['x_m', 'y_m', 'z_m']].values.tolist() == [[10., 10., 100.]] * 2
    convergence = pd.read_csv(folder / '001_UAV_3D_50_convergence.csv')
    assert len(convergence) == 202
    assert convergence.groupby('case').iteration.apply(list).tolist() == [list(range(101))] * 2


@pytest.mark.parametrize('corruption', ['identity', 'history', 'fitness', 'fe', 'nonfinite', 'final'])
def test_validator_rejects_corrupt_resume_task(corruption):
    artifact = valid_artifact()
    if corruption == 'identity':
        artifact['result']['seed'] = 99
    elif corruption == 'history':
        artifact['history'].pop()
    elif corruption == 'fitness':
        artifact['history'][2]['fitness'] = -.5
    elif corruption == 'fe':
        artifact['history'][2]['fe'] = 1
    elif corruption == 'nonfinite':
        artifact['history'][2]['energy'] = float('nan')
    elif corruption == 'final':
        artifact['result']['fitness'] += .1
    with pytest.raises(ValueError):
        validate_task(artifact, dataset='sample.csv', case='GA', seed=42)
