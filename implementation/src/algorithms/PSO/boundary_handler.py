"""Xử lý điều kiện biên cho hạt trong PSO."""

import numpy as np

from .particle import Particle


def handle_boundaries(
    particle: Particle, lower_bounds: np.ndarray, upper_bounds: np.ndarray
) -> None:
    """Kiểm tra và giới hạn vị trí trong không gian tìm kiếm [lower, upper]."""
    # Nếu vượt biên, gán về biên và triệt tiêu vận tốc thành phần đó
    out_of_bounds_lower = particle.position < lower_bounds
    out_of_bounds_upper = particle.position > upper_bounds

    particle.position = np.clip(particle.position, lower_bounds, upper_bounds)
    particle.velocity[out_of_bounds_lower | out_of_bounds_upper] = 0.0
