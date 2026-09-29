"""Toán tử chọn lọc Tournament Selection cho GA."""

import numpy as np

from .chromosome import Chromosome


def tournament_selection(
    population: list[Chromosome],
    tournament_size: int,
    rng: np.random.Generator,
) -> Chromosome:
    """Chọn lọc theo hình thức đấu loại Tournament."""
    indices = rng.choice(len(population), size=tournament_size, replace=False)
    candidates = [population[i] for i in indices]
    best = max(candidates, key=lambda ind: ind.fitness)
    return best.copy()
