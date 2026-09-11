"""Kiểu kết quả chuẩn giúp việc so sánh không phụ thuộc thuật toán."""

from dataclasses import dataclass

import numpy as np


@dataclass
class OptimizationResult:
    algorithm: str
    best_position: np.ndarray
    best_objective: float
    convergence_history: list[float]
    runtime_seconds: float
    seed: int
