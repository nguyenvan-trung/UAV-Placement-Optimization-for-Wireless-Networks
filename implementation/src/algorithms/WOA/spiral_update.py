"""Cơ chế tấn công mạng bọt xoắn ốc (Spiral Bubble-net Attacking) của cá kình."""

import numpy as np


def spiral_update(
    current_position: np.ndarray,
    best_position: np.ndarray,
    l: float,
    b: float = 1.0,
) -> np.ndarray:
    """Cập nhật vị trí bơi xoắn ốc: X = D' * exp(b*l) * cos(2*pi*l) + X*."""
    D_prime = np.abs(best_position - current_position)
    spiral_term = D_prime * np.exp(b * l) * np.cos(2.0 * np.pi * l)
    return spiral_term + best_position
