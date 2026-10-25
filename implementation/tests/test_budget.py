"""Small-budget checks; no production results or large experiments."""
import copy
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml
from threadpoolctl import threadpool_limits

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'implementation'))
from src.counter import FitnessCounter,BudgetExhausted
from src.benchmark import BenchmarkProblem,make_optimizer
from src.scenarios import generate_scenario
from src.algorithms.base.budget import CountedProblem,progress

CONFIG=yaml.safe_load((ROOT/'configs/benchmark.yaml').read_text(encoding='utf-8'))
NAMES=[(n,False) for n in CONFIG['algorithms']]+[(n,True) for n in CONFIG['ablation']]


def problem():
    users=generate_scenario('uniform',50,123)[['x_m','y_m','z_m']].to_numpy()
    return BenchmarkProblem(users,CONFIG,dict(id='main',weights=dict(C=.6,E=.2,I=.2),coverage_quantity='SNR'))


@pytest.mark.parametrize('name,ablation',NAMES)
@pytest.mark.parametrize('budget',[5,31,60,120])
def test_exact_budget_and_repeatability(name,ablation,budget):
    cfg=copy.deepcopy(CONFIG);cfg['common']['population_size']=6
    p=problem();raw_calls=[]
    original=p.evaluate
    def spy(x):
        raw_calls.append(np.asarray(x).copy())
        return original(x)
    p.evaluate=spy
    initial=np.random.default_rng(99).uniform(p.search_space.lower_bounds,p.search_space.upper_bounds,(6,12))
    with threadpool_limits(limits=1):
        a=make_optimizer(name,cfg,42,ablation).optimize(p,max_fe=budget,initial_population=initial)
        b=make_optimizer(name,cfg,42,ablation).optimize(problem(),max_fe=budget,initial_population=initial)
    assert len(raw_calls)==a.fe_used==b.fe_used==budget
    assert sum(a.fe_phase_counts.values())==budget
    assert a.fe_history[-1]['fe']==budget
    assert a.fe_history==b.fe_history
    np.testing.assert_array_equal(a.best_position,b.best_position)
    assert a.best_objective==b.best_objective
    assert a.best_objective==pytest.approx(p.raw_metrics(a.best_position)['fitness'],abs=1e-9)
    if not ablation and name!='I-WOA':
        np.testing.assert_array_equal(raw_calls[:min(6,budget)],initial[:min(6,budget)])


def test_counter_never_calls_beyond_limit_and_tracks_last_candidate():
    calls=[]
    counter=FitnessCounter(lambda x:calls.append(x[0]) or x[0],3,target=2)
    for x in [1,2,3]:counter(np.array([x]))
    with pytest.raises(BudgetExhausted):counter(np.array([4]))
    assert calls==[1,2,3] and counter.best_fitness==3 and counter.fe_to_target==2


def test_progress_is_fe_fraction():
    p=problem();counter=FitnessCounter(p.evaluate,100)
    counted=CountedProblem(p,counter,np.zeros((6,12)))
    counter.fe_count=25
    assert progress(counted,99,100)==.25


def test_manifest_reproducibility_and_disjointness():
    spec=importlib.util.spec_from_file_location('seed_generator',ROOT/'implementation/scripts/generate_seeds.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    rows=module.generate(CONFIG)
    assert rows==module.generate(CONFIG)
    tuning={r[k] for r in rows if r['purpose']=='tuning' for k in ['data_seed','algo_seed']}
    evaluation={r[k] for r in rows if r['purpose']=='eval' for k in ['data_seed','algo_seed']}
    assert not tuning&evaluation


def test_000_matches_woa_under_fe():
    cfg=copy.deepcopy(CONFIG);cfg['common']['population_size']=6
    a=make_optimizer('WOA',cfg,42).optimize(problem(),max_fe=60)
    b=make_optimizer('WOA(000)',cfg,42,True).optimize(problem(),max_fe=60)
    np.testing.assert_array_equal(a.best_position,b.best_position)
    assert a.fe_history==b.fe_history
