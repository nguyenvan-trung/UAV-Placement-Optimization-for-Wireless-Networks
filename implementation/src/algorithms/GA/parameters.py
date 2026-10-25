"""Các tham số chỉ thuộc về GA."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GAParameters:
    population_size: int = 30
    generations: int = 100
    crossover_rate: float = 0.9
    mutation_rate: float = 0.1
    elite_count: int = 2

    # Optional experiment operators; disabled for the original baseline.
    use_kmeans_init: bool = False
    use_obl: bool = False
    use_levy: bool = False
    obl_rate: float = 0.2
    levy_rate: float = 0.3
    levy_beta: float = 1.5
    levy_step_size: float = 0.05
