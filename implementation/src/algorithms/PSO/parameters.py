"""Các tham số chỉ thuộc về PSO."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PSOParameters:
    swarm_size: int = 30
    iterations: int = 100
    inertia_weight: float = 0.7
    cognitive_coefficient: float = 1.5
    social_coefficient: float = 1.5
