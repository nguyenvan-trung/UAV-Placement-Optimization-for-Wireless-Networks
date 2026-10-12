"""Xử lý điều kiện biên cho cá kình trong WOA."""

import numpy as np


def handle_boundaries(
    position: np.ndarray, lower_bounds: np.ndarray, upper_bounds: np.ndarray
) -> np.ndarray:
    """Giới hạn vị trí cá kình trong miền không gian [lower, upper]."""
    return np.clip(position, lower_bounds, upper_bounds)
