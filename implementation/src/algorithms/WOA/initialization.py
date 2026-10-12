"""Khởi tạo quần thể cá kình ban đầu cho WOA."""

import numpy as np

from .whale import Whale


def initialize_whales(
    population_size: int,
    lower_bounds: np.ndarray,
    upper_bounds: np.ndarray,
    rng: np.random.Generator,
) -> list[Whale]:
    """Sinh ngẫu nhiên các vị trí cá thể trong không gian [lower_bounds, upper_bounds]."""
    dim = len(lower_bounds)
    whales: list[Whale] = []
    for _ in range(population_size):
        pos = rng.uniform(lower_bounds, upper_bounds, size=dim)
        whales.append(Whale(position=pos))
    return whales
