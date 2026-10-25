import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'implementation'))
from src.objectives.sensitivity import evaluate_sensitivity
from src.objectives.metrics import evaluate_solution


def test_main_matches_baseline():
    u=np.array([[0.,0.,50.],[1000.,1000.,100.]])
    ue=np.array([[0.,0.,0.],[500.,500.,0.]])
    actual=evaluate_sensitivity(u,ue,dict(C=.6,E=.2,I=.2))
    expected=evaluate_solution(u,ue)
    assert actual['fitness']==pytest.approx(expected.fitness)
    assert actual['I']==expected.interference_rate


def test_equal_power_interferers_destroy_sinr_coverage():
    # Equal powers => SINR=p/(noise+p)<1, while overhead SNR exceeds 18 dB.
    u=np.array([[0.,0.,50.],[0.,0.,50.]])
    ue=np.array([[0.,0.,0.]])
    result=evaluate_sensitivity(u,ue,dict(C=.6,E=.2,I=.2),'SINR')
    assert result['C_snr']==1 and result['C_sinr']==0 and result['I']==1
    assert result['fitness']==pytest.approx(-.2*101/151-.2)


def test_coverage_only_and_single_transmitter():
    u=np.array([[0.,0.,50.]])
    result=evaluate_sensitivity(u,np.array([[0.,0.,0.]]),dict(C=1.,E=0.,I=0.))
    assert result['fitness']==result['C_snr']==result['C_sinr']==1


def test_preregistered_weights():
    cfg=yaml.safe_load((ROOT/'configs/sensitivity.yaml').read_text(encoding='utf-8'))
    rows=cfg['sensitivity']['configurations']
    assert len(rows)==7
    assert all(sum(row['weights'].values())==pytest.approx(1) for row in rows)


def test_paired_statistics():
    spec=importlib.util.spec_from_file_location('analysis',ROOT/'implementation/scripts/analyze_sensitivity.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    assert module.paired_test([1,1],[1,1])==(1.,0.)
    assert module.paired_test([2,3,4],[1,1,1])[1]==1
    np.testing.assert_allclose(module.holm([.01,.03,.04]),[.03,.06,.06])
