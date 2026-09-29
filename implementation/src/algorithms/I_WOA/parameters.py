"""Các tham số mở rộng của thuật toán cải tiến I-WOA."""

from dataclasses import dataclass


@dataclass(frozen=True)
class IWOAParameters:
    population_size: int = 30
    iterations: int = 100
    spiral_constant: float = 1.0
    levy_beta: float = 1.5           # Số mũ phân phối Levy (1 < beta <= 2)
    levy_step_size: float = 0.05     # Hệ số bước nhảy Levy
    use_obl_init: bool = True        # Sử dụng Học đối kháng khi khởi tạo
    obl_rate: float = 0.2            # Xác suất áp dụng OBL trong quá trình lặp
    use_kmeans_init: bool = True     # Sử dụng K-Means tạo cá thể mầm ban đầu
