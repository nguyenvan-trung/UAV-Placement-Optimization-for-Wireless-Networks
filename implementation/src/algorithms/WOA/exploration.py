"""Cơ chế tìm kiếm con mồi toàn cục (Exploration / Search for Prey) của cá kình."""

import numpy as np


def search_for_prey(
    current_position: np.ndarray,
    random_whale_position: np.ndarray,
    A: np.ndarray,
    C: np.ndarray,
) -> np.ndarray:
    """Cập nhật vị trí khi bơi tự do tìm con mồi mới: X = X_rand - A * |C*X_rand - X|."""
    D = np.abs(C * random_whale_position - current_position)
    return random_whale_position - A * D
