"""Ground-UE scenario generators, independent of optimization algorithms.

New experimental design, not a replacement for the existing dataset generator.
Cluster centers and distances are fractions of min(width, height).
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd

NAMES = ('single_cluster', 'multi_cluster', 'uniform', 'offset_cluster', 'with_outliers')


@dataclass(frozen=True)
class ScenarioParameters:
    width: float = 1000.
    height: float = 1000.
    cluster_sigma_fraction: float = .05
    cluster_radius_fraction: float = .12
    outlier_fraction: float = .10
    outlier_min_distance_fraction: float = .35
    outlier_max_distance_fraction: float = .45

    def __post_init__(self):
        values = list(vars(self).values())
        if not np.isfinite(values).all() or self.width <= 0 or self.height <= 0:
            raise ValueError('Parameters must be finite; area dimensions must be positive')
        if not (0 < self.cluster_sigma_fraction < self.cluster_radius_fraction <= .15):
            raise ValueError('Require 0 < sigma < cluster radius <= .15')
        if not 0 <= self.outlier_fraction <= 1:
            raise ValueError('outlier_fraction must be in [0,1]')
        if not self.cluster_radius_fraction < self.outlier_min_distance_fraction <= self.outlier_max_distance_fraction <= .49:
            raise ValueError('Require cluster radius < outlier min <= outlier max <= .49')


def _cluster(rng, count, center, params):
    """Rejection-sampled truncated isotropic Gaussian; no boundary clipping."""
    scale = min(params.width, params.height)
    chunks = []
    remaining = count
    while remaining:
        proposals = rng.normal(0, params.cluster_sigma_fraction*scale, size=(max(16,2*remaining),2))
        accepted = proposals[np.linalg.norm(proposals,axis=1) <= params.cluster_radius_fraction*scale][:remaining]
        chunks.append(accepted + center)
        remaining -= len(accepted)
    return np.vstack(chunks) if count else np.empty((0,2))


def generate_scenario(name, count, data_seed, parameters=None):
    params = parameters or ScenarioParameters()
    if name not in NAMES:
        raise ValueError(f'Unknown distribution: {name}')
    if not isinstance(count,(int,np.integer)) or count <= 0:
        raise ValueError('count must be a positive integer')
    rng = np.random.default_rng(data_seed)
    center = np.array([params.width/2,params.height/2])
    outliers = np.zeros(count,dtype=bool)
    cluster_ids = np.zeros(count,dtype=int)
    if name == 'uniform':
        xy = rng.uniform([0,0],[params.width,params.height],size=(count,2))
        cluster_ids[:] = -1
    elif name == 'multi_cluster':
        centers = np.array([[.25,.25],[.75,.25],[.25,.75],[.75,.75]]) * [params.width,params.height]
        cluster_ids = np.arange(count)%len(centers)
        xy = np.empty((count,2))
        for index,c in enumerate(centers):
            mask = cluster_ids == index
            xy[mask] = _cluster(rng,int(mask.sum()),c,params)
    elif name == 'with_outliers':
        n_outlier = int(np.floor(count*params.outlier_fraction+.5))
        core = _cluster(rng,count-n_outlier,center,params)
        theta = rng.uniform(0,2*np.pi,size=n_outlier)
        scale = min(params.width,params.height)
        # Uniform area in the annulus, not uniform radius.
        radius = np.sqrt(rng.uniform(params.outlier_min_distance_fraction**2,
                                    params.outlier_max_distance_fraction**2,size=n_outlier))*scale
        outer = center + np.column_stack((radius*np.cos(theta),radius*np.sin(theta)))
        xy = np.vstack((core,outer))
        outliers[count-n_outlier:] = True
        cluster_ids[outliers] = -1
    else:
        c = center if name == 'single_cluster' else np.array([.2*params.width,.75*params.height])
        xy = _cluster(rng,count,c,params)
    order = rng.permutation(count)
    return pd.DataFrame(dict(user_id=np.arange(1,count+1),x_m=xy[order,0],y_m=xy[order,1],
                             z_m=np.zeros(count),demand=np.ones(count),
                             is_outlier=outliers[order],cluster_id=cluster_ids[order]))


def validate_seed_split(tuning_seeds, eval_seeds):
    if set(tuning_seeds) & set(eval_seeds):
        raise ValueError('Tuning and evaluation seeds overlap')


def make_seed_split(root_seed, tuning_count, eval_count):
    """SeedSequence streams with explicit collision checks for scalar seeds."""
    if tuning_count < 0 or eval_count < 0:
        raise ValueError('Seed counts must be nonnegative')
    children = np.random.SeedSequence(root_seed).spawn(tuning_count+eval_count)
    values = [int(s.generate_state(1,dtype=np.uint64)[0]) for s in children]
    if len(values) != len(set(values)):
        raise RuntimeError('Generated duplicate seeds; choose another root_seed')
    tuning, evaluation = values[:tuning_count],values[tuning_count:]
    validate_seed_split(tuning,evaluation)
    return tuning,evaluation
