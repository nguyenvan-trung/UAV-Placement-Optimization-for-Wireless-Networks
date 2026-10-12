"""Cơ chế học đối kháng (Opposition-Based Learning - OBL).

Với mỗi giải pháp X trong [L, U], sinh nghiệm đối xứng:
X_op = L + U - X
So sánh và giữ lại các cá thể ưu tú nhất, tăng tốc độ hội tụ và tránh
tập trung một góc bản đồ.
"""

import numpy as np

from ..WOA.whale import Whale


def generate_opposite_position(
    position: np.ndarray,
    lower_bounds: np.ndarray,
    upper_bounds: np.ndarray,
) -> np.ndarray:
    """Tạo vị trí đối xứng X_op = L + U - X."""
    opposite = lower_bounds + upper_bounds - position
    return np.clip(opposite, lower_bounds, upper_bounds)


def apply_obl_population(
    whales: list[Whale],
    problem: object,
    lower_bounds: np.ndarray,
    upper_bounds: np.ndarray,
) -> list[Whale]:
    """Sinh quần thể đối lập, đánh giá và chọn lọc N cá thể tốt nhất từ tập (Gốc U Đối lập)."""
    pop_size = len(whales)
    opposite_whales: list[Whale] = []

    for w in whales:
        op_pos = generate_opposite_position(w.position, lower_bounds, upper_bounds)
        op_fit = problem.evaluate(op_pos)
        opposite_whales.append(Whale(position=op_pos, fitness=op_fit))

    # Ghép 2 quần thể (kích thước 2 * pop_size)
    combined = whales + opposite_whales
    # Chọn pop_size cá thể có fitness cao nhất
    combined.sort(key=lambda w: w.fitness, reverse=True)
    return combined[:pop_size]
