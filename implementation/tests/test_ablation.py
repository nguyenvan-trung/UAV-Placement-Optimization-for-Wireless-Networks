"""Core equivalence before FE benchmark integration."""
from dataclasses import replace
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.algorithms.I_WOA.parameters import IWOAParameters
from src.algorithms.I_WOA.optimizer import IWOAOptimizer
from src.algorithms.WOA.parameters import WOAParameters
from src.algorithms.WOA.optimizer import WOAOptimizer
from src.problem.objective import UAVPlacementProblem


class CountedProblem:
    def __init__(self):
        self.problem=UAVPlacementProblem(np.array([[100.,100.,0.],[900.,900.,0.]]))
        self.calls=0

    def __getattr__(self,name):
        return getattr(self.problem,name)

    def evaluate(self,x):
        self.calls+=1
        return self.problem.evaluate(x)


@pytest.mark.parametrize('seed',[42,123,2026])
def test_000_matches_original_woa(seed):
    baseline,variant=CountedProblem(),CountedProblem()
    expected=WOAOptimizer(WOAParameters(population_size=6,iterations=5),seed=seed).optimize(baseline)
    actual=IWOAOptimizer(IWOAParameters(population_size=6,iterations=5,
                        use_kmeans_init=False,use_obl=False,use_levy=False),seed=seed).optimize(variant)
    np.testing.assert_array_equal(actual.best_position,expected.best_position)
    assert actual.convergence_history==expected.convergence_history
    assert actual.best_objective==expected.best_objective
    assert baseline.calls==variant.calls==6*(1+5)


def test_obl_master_disables_initial_and_dynamic_overhead():
    p=CountedProblem()
    IWOAOptimizer(IWOAParameters(population_size=6,iterations=5,use_kmeans_init=False,
                  use_obl=False,use_obl_init=True,obl_rate=1.,use_levy=False)).optimize(p)
    assert p.calls==6*(1+5)
