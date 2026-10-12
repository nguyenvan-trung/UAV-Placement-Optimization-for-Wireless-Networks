"""Cập nhật các hệ số a, A, C, l trong thuật toán WOA."""

import numpy as np


def update_coefficients(
    iteration: int,
    max_iterations: int,
    dimension: int,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray, float]:
    """Tính các vector hệ số A, C và giá trị l cho cá kình.

    a: giảm tuyến tính từ 2 về 0
    A = 2*a*r1 - a
    C = 2*r2
    l: số thực ngẫu nhiên trong [-1, 1]
    """
    a = 2.0 - 2.0 * (iteration / max(1, max_iterations - 1))
    r1 = rng.uniform(0.0, 1.0, size=dimension)
    r2 = rng.uniform(0.0, 1.0, size=dimension)

    A = 2.0 * a * r1 - a
    C = 2.0 * r2
    l = rng.uniform(-1.0, 1.0)

    return A, C, l
