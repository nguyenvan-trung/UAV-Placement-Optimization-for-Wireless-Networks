"""Các tham số chỉ thuộc về PSO."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PSOParameters:
    swarm_size: int = 30
    iterations: int = 100
    inertia_weight: float = 0.7
    cognitive_coefficient: float = 1.5
    social_coefficient: float = 1.5

    # Optional experiment operators; disabled for the original baseline.
    use_kmeans_init: bool = False
    use_obl: bool = False
    use_levy: bool = False
    obl_rate: float = 0.2
    levy_rate: float = 0.3
    levy_beta: float = 1.5
    levy_step_size: float = 0.05
