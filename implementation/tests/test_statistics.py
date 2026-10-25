import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('statistics_analysis',ROOT/'implementation/scripts/analyze.py')
analysis=importlib.util.module_from_spec(spec);spec.loader.exec_module(analysis)


@pytest.fixture
def tmp_path():
    # Avoid pytest's chmod-based temp handling on this restricted Windows host.
    import uuid
    folder=ROOT/'reports'/'statistics_test_artifacts'/uuid.uuid4().hex
    folder.mkdir(parents=True)
    return folder


def test_effect_and_ties():
    rng=np.random.default_rng(42)
    result=analysis.compare(np.zeros(12),rng,100)
    assert result['p_raw']==1 and result['effect_rbc']==0
    assert result['difference_ci_low']==result['difference_ci_high']==0
    positive=analysis.compare(np.ones(12),rng,100)
    assert positive['method']=='exact_sign'
    assert positive['effect_rbc']==1
    assert positive['median_difference']==1
    assert positive['p_raw']==pytest.approx(2/2**12)


def test_bootstrap_is_reproducible_and_holm():
    left=analysis.bootstrap(np.arange(10),np.mean,np.random.default_rng(1),100,.05)
    right=analysis.bootstrap(np.arange(10),np.mean,np.random.default_rng(1),100,.05)
    assert left==right
    np.testing.assert_allclose(analysis.holm([.01,.03,.04]),[.03,.06,.06])


def synthetic_rows():
    rows=[]
    for instance in range(12):
        for run in range(2):
            for index,algo in enumerate(analysis.ALGORITHMS):
                rows.append(dict(scenario_id='synthetic_uniform_100',ue_count=100,
                    distribution='uniform',instance_k=instance,data_seed=100+instance,
                    run_id=run,algo_seed=1000+run,algorithm=algo,
                    fitness=.1+index*.02+instance*.001+run*.0001,
                    wall_time_s=2.,cpu_time_s=1.,fe_used=100,
                    batch_wall_time_s=100.,batch_total_cpu_s=144.,n_workers=2,
                    purpose='eval',feasible=True,batch_id='synthetic_test_only'))
    return pd.DataFrame(rows)


def test_end_to_end_exports_use_instances(tmp_path):
    source=tmp_path/'synthetic_runs.csv';synthetic_rows().to_csv(source,index=False)
    output=tmp_path/'analysis'
    analysis.analyze(source,output,resamples=100,expected_runs=2)
    pairs=pd.read_csv(output/'paired_comparisons.csv')
    assert (pairs.n_pairs==12).all() # not 24 per-run observations
    assert (pairs.effect_rbc==1).all()
    assert (pairs.p_holm<.05).all()
    assert len(pd.read_csv(output/'batches.csv'))==1
    assert (output/'critical_difference.png').exists()
    assert (output/'critical_difference.pdf').exists()
    for name in ['descriptive','paired_comparisons','omnibus','nemenyi','performance','batches']:
        for suffix in ['csv','md','tex']:assert (output/f'{name}.{suffix}').exists()


def test_missing_algorithm_rejected(tmp_path):
    source=tmp_path/'incomplete.csv'
    synthetic_rows().iloc[1:].to_csv(source,index=False)
    with pytest.raises(ValueError,match='Incomplete'):
        analysis.analyze(source,tmp_path/'out',resamples=100,expected_runs=2)
