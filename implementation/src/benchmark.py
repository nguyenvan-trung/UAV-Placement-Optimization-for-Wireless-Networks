"""Factory and raw reporting interface for opt-in FE experiments."""
import numpy as np
from .algorithms import (GAOptimizer,GAParameters,PSOOptimizer,PSOParameters,
    WOAOptimizer,WOAParameters,IWOAOptimizer,IWOAParameters,
    HybridPSOGAOptimizer,HPSOGAParameters,HybridWOAPSOOptimizer,HWOAPSOParameters)
from .problem.objective import UAVPlacementProblem
from .objectives.sensitivity import evaluate_sensitivity

FACTORIES = {
    'GA':(GAOptimizer,GAParameters,'population_size'),
    'PSO':(PSOOptimizer,PSOParameters,'swarm_size'),
    'WOA':(WOAOptimizer,WOAParameters,'population_size'),
    'H-PSO-GA':(HybridPSOGAOptimizer,HPSOGAParameters,'population_size'),
    'H-WOA-PSO':(HybridWOAPSOOptimizer,HWOAPSOParameters,'population_size'),
    'I-WOA':(IWOAOptimizer,IWOAParameters,'population_size')}


def make_optimizer(name, config, seed, ablation=False):
    if ablation:
        k,o,l=config['ablation'][name]
        parameters=dict(config['algorithms']['I-WOA'],use_kmeans_init=k,use_obl=o,use_levy=l)
        cls,param,size=FACTORIES['I-WOA']
    else:
        cls,param,size=FACTORIES[name]
        parameters=dict(config['algorithms'][name])
    parameters[size]=config['common']['population_size']
    return cls(param(**parameters),seed=int(seed))


class BenchmarkProblem(UAVPlacementProblem):
    def __init__(self, users, config, experiment):
        p=config['problem'];weights=experiment['weights']
        super().__init__(users,num_uavs=p['num_uav'],area_width=p['area_width'],area_height=p['area_height'],
            min_altitude=p['min_altitude'],max_altitude=p['max_altitude'],snr_threshold=p['snr_threshold_db'],
            min_uav_distance=p['min_uav_distance'],weight_coverage=weights['C'],
            weight_energy=weights['E'],weight_interference=weights['I'])
        self.experiment=experiment

    def raw_metrics(self, position):
        x=self.search_space.clip(self._validate_solution(position))
        if not self.is_feasible(x):
            raise ValueError('Cannot report infeasible solution')
        return evaluate_sensitivity(x.reshape(-1,3),self.ue_coords,self.experiment['weights'],
            self.experiment['coverage_quantity'],self.snr_threshold,self.min_altitude,self.max_altitude)

    def evaluate(self, position):
        x=self.search_space.clip(self._validate_solution(position))
        if not self.is_feasible(x):
            return -np.inf
        # Baseline uses the original Fitness implementation; auxiliary SINR is opt-in.
        if self.experiment['coverage_quantity']=='SNR':
            return super().evaluate(x)
        return self.raw_metrics(x)['fitness']
