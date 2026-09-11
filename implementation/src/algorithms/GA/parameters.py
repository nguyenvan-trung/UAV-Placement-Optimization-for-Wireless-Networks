"""Các tham số chỉ thuộc về GA."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GAParameters:
    population_size: int = 30
    generations: int = 100
    crossover_rate: float = 0.9
    mutation_rate: float = 0.1
    elite_count: int = 2
