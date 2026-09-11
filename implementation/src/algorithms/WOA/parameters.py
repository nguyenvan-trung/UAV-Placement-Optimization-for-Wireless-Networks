"""Các tham số chỉ thuộc về WOA."""

from dataclasses import dataclass


@dataclass(frozen=True)
class WOAParameters:
    population_size: int = 30
    iterations: int = 100
    spiral_constant: float = 1.0
