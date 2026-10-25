"""Contract checks only: these tests never run UAV optimizers or the CSV study."""
from pathlib import Path
import json
from types import SimpleNamespace

import numpy as np
import pytest

from src.notebook_study import cases, make_case, run_study, ObservedProblem
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


def test_notebook_is_unexecuted_and_run_gate_is_off():
    root = Path(__file__).resolve().parents[2]
    notebook = json.loads((root / 'implementation/notebooks/full_study_100_iterations.ipynb').read_text(encoding='utf-8'))
    code = [c for c in notebook['cells'] if c['cell_type'] == 'code']
    assert all(c['execution_count'] is None and c['outputs'] == [] for c in code)
    assert any('CONFIRM_RUN = False' in ''.join(c['source']) for c in code)
    config = json.loads((root / 'configs/notebook_study.json').read_text())
    assert config['seeds'] == []
