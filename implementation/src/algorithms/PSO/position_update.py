"""Cập nhật vị trí cho hạt trong PSO."""

import numpy as np

from .particle import Particle


def update_position(particle: Particle) -> np.ndarray:
    """Cập nhật vị trí mới: x(t+1) = x(t) + v(t+1)."""
    return particle.position + particle.velocity
