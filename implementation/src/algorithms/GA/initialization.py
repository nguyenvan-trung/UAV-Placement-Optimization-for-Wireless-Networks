"""Khởi tạo quần thể ban đầu cho GA."""

import numpy as np

from .chromosome import Chromosome


def initialize_population(
    pop_size: int,
    lower_bounds: np.ndarray,
    upper_bounds: np.ndarray,
    rng: np.random.Generator,
) -> list[Chromosome]:
    """Sinh ngẫu nhiên pop_size cá thể đều trong khoảng [lower_bounds, upper_bounds]."""
    dim = len(lower_bounds)
    population = []
    for _ in range(pop_size):
        genes = rng.uniform(lower_bounds, upper_bounds, size=dim)
        population.append(Chromosome(genes=genes))
    return population
