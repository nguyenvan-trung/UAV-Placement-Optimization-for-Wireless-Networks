"""Mã hóa/giải mã [x1, y1, h1, ..., xN, yN, hN]."""

import numpy as np


def decode_uav_positions(solution: np.ndarray) -> np.ndarray:
    if solution.size % 3 != 0:
        raise ValueError("Kích thước nghiệm phải chia hết cho 3.")
    return solution.reshape(-1, 3)
