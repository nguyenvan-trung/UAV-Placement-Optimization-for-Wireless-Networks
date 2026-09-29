"""Khởi tạo bầy hạt cho PSO."""

import numpy as np

from .particle import Particle


def initialize_swarm(
    swarm_size: int,
    lower_bounds: np.ndarray,
    upper_bounds: np.ndarray,
    rng: np.random.Generator,
) -> list[Particle]:
    """Khởi tạo vị trí và vận tốc ban đầu cho từng hạt trong bầy."""
    dim = len(lower_bounds)
    ranges = upper_bounds - lower_bounds
    v_max = 0.2 * ranges

    swarm: list[Particle] = []
    for _ in range(swarm_size):
        pos = rng.uniform(lower_bounds, upper_bounds, size=dim)
        vel = rng.uniform(-v_max, v_max, size=dim)
        swarm.append(
            Particle(
                position=pos.copy(),
                velocity=vel.copy(),
                best_position=pos.copy(),
            )
        )
    return swarm
