"""Cơ chế vây bắt con mồi (Encircling Prey) của cá kình."""

import numpy as np


def encircle_prey(
    current_position: np.ndarray,
    best_position: np.ndarray,
    A: np.ndarray,
    C: np.ndarray,
) -> np.ndarray:
    """Cập nhật vị trí khi co cụm vây quanh con mồi tốt nhất: X = X* - A * |C*X* - X|."""
    D = np.abs(C * best_position - current_position)
    return best_position - A * D
