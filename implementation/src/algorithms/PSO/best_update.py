"""Cập nhật vị trí tốt nhất của cá nhân (pbest) và toàn cục (gbest) cho PSO."""

import numpy as np

from .particle import Particle


def update_bests(
    swarm: list[Particle],
    global_best_position: np.ndarray,
    global_best_fitness: float,
) -> tuple[np.ndarray, float]:
    """Cập nhật pbest cho từng hạt và gbest của toàn bộ bầy đàn."""
    best_pos = global_best_position.copy()
    best_fit = global_best_fitness

    for p in swarm:
        # Cập nhật pbest (bài toán tối đa hóa)
        if p.fitness > p.best_fitness:
            p.best_fitness = p.fitness
            p.best_position = p.position.copy()

        # Cập nhật gbest
        if p.best_fitness > best_fit:
            best_fit = p.best_fitness
            best_pos = p.best_position.copy()

    return best_pos, best_fit
