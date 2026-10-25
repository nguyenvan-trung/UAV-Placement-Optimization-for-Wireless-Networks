import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.scenarios import NAMES, generate_scenario, make_seed_split, validate_seed_split


@pytest.mark.parametrize('name',NAMES)
def test_reproducibility_and_bounds(name):
    a=generate_scenario(name,100,123)
    pd.testing.assert_frame_equal(a,generate_scenario(name,100,123))
    assert len(a)==100
    assert a.x_m.between(0,1000).all() and a.y_m.between(0,1000).all()
    assert (a.z_m==0).all()
    assert not a.equals(generate_scenario(name,100,124))


def test_outliers_have_promised_distance():
    df=generate_scenario('with_outliers',100,123)
    radius=np.linalg.norm(df[['x_m','y_m']].to_numpy()-[500,500],axis=1)
    assert df.is_outlier.sum()==10
    assert (radius[df.is_outlier]>=350).all() and (radius[df.is_outlier]<=450).all()
    assert (radius[~df.is_outlier]<=120).all()


def test_multi_clusters_do_not_overlap():
    df=generate_scenario('multi_cluster',100,123)
    centers=np.array([[250,250],[750,250],[250,750],[750,750]])
    radius=np.linalg.norm(df[['x_m','y_m']].to_numpy()-centers[df.cluster_id],axis=1)
    assert (radius<=120).all()


def test_seed_split_is_disjoint():
    tuning,evaluation=make_seed_split(42,10,30)
    assert not set(tuning)&set(evaluation)
    assert (tuning,evaluation)==make_seed_split(42,10,30)
    with pytest.raises(ValueError): validate_seed_split([1,2],[2,3])
