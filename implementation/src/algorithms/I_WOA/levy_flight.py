"""Cơ chế bước nhảy Levy Flight (Mantegna's Algorithm).

Đặc trưng bởi phân phối đuôi nặng (heavy-tailed): các bước nhảy ngắn
xen kẽ các bước nhảy rất dài ngẫu nhiên, giúp cá kình bứt phá khỏi các
cực trị địa phương (Local Optima).
"""

import math
import numpy as np


def compute_levy_sigma(beta: float = 1.5) -> float:
    """Tính độ lệch chuẩn sigma_u theo công thức Mantegna."""
    num = math.gamma(1.0 + beta) * math.sin(math.pi * beta / 2.0)
    den = math.gamma((1.0 + beta) / 2.0) * beta * (2.0 ** ((beta - 1.0) / 2.0))
    return (num / den) ** (1.0 / beta)


def sample_levy_step(dimension: int, beta: float, sigma_u: float, rng: np.random.Generator) -> np.ndarray:
    """Sinh vector bước nhảy Levy có chiều dimension."""
    u = rng.normal(0.0, sigma_u, size=dimension)
    v = rng.normal(0.0, 1.0, size=dimension)
    step = u / (np.abs(v) ** (1.0 / beta))
    return step


def apply_levy_flight(
    position: np.ndarray,
    best_position: np.ndarray,
    lower_bounds: np.ndarray,
    upper_bounds: np.ndarray,
    beta: float,
    sigma_u: float,
    step_size: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Áp dụng đột biến bước nhảy Levy: X_new = X + step_size * Levy(beta) * (X - X*)."""
    dim = len(position)
    levy = sample_levy_step(dim, beta, sigma_u, rng)
    ranges = upper_bounds - lower_bounds

    # Bước nhảy kết hợp hướng đến con mồi và biên kích thước
    delta = (position - best_position)
    # Nếu delta quá nhỏ (gần hội tụ), dùng ranges để kích hoạt cú nhảy bứt phá
    perturbation = np.where(np.abs(delta) > 1e-3, delta, 0.1 * ranges)

    new_position = position + step_size * levy * perturbation
    return np.clip(new_position, lower_bounds, upper_bounds)
