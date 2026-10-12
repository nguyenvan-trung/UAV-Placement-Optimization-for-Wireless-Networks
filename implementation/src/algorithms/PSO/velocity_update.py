"""Cập nhật vận tốc cho hạt trong PSO."""

import numpy as np

from .particle import Particle


def update_velocity(
    particle: Particle,
    global_best_position: np.ndarray,
    w: float,
    c1: float,
    c2: float,
    v_max: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray:
    """Cập nhật vận tốc hạt: v = w*v + c1*r1*(pbest - x) + c2*r2*(gbest - x)."""
    dim = len(particle.position)
    r1 = rng.uniform(0.0, 1.0, size=dim)
    r2 = rng.uniform(0.0, 1.0, size=dim)

    cognitive = c1 * r1 * (particle.best_position - particle.position)
    social = c2 * r2 * (global_best_position - particle.position)

    new_velocity = w * particle.velocity + cognitive + social
    # Giới hạn vận tốc [-v_max, v_max]
    new_velocity = np.clip(new_velocity, -v_max, v_max)
    return new_velocity
