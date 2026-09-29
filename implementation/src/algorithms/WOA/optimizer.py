"""Vòng lặp chính thuật toán Whale Optimization Algorithm (WOA)."""

import time

import numpy as np

from ..base.result import OptimizationResult
from .boundary_handler import handle_boundaries
from .coefficient_update import update_coefficients
from .encircling import encircle_prey
from .exploration import search_for_prey
from .initialization import initialize_whales
from .parameters import WOAParameters
from .spiral_update import spiral_update


class WOAOptimizer:
    """Thuật toán tối ưu bầy cá kình chuẩn (Whale Optimization Algorithm - Baseline)."""

    def __init__(self, parameters: WOAParameters | None = None, seed: int = 42):
        self.params = parameters or WOAParameters()
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def optimize(self, problem: object) -> OptimizationResult:
        start_time = time.perf_counter()

        lb = problem.search_space.lower_bounds
        ub = problem.search_space.upper_bounds
        dim = len(lb)

        # 1. Khởi tạo quần thể cá kình
        whales = initialize_whales(
            population_size=self.params.population_size,
            lower_bounds=lb,
            upper_bounds=ub,
            rng=self.rng,
        )

        # 2. Đánh giá thế hệ đầu tiên
        for w in whales:
            w.fitness = problem.evaluate(w.position)

        # Tìm cá thể tốt nhất ban đầu
        best_whale = max(whales, key=lambda w: w.fitness).copy()
        convergence_history: list[float] = [float(best_whale.fitness)]

        # 3. Vòng lặp săn mồi chính
        for t in range(self.params.iterations):
            for i, whale in enumerate(whales):
                A, C, l = update_coefficients(
                    iteration=t,
                    max_iterations=self.params.iterations,
                    dimension=dim,
                    rng=self.rng,
                )
                p = self.rng.uniform(0.0, 1.0)

                if p < 0.5:
                    norm_A = np.linalg.norm(A) / np.sqrt(dim)  # hoặc kiểm tra độ lớn trung bình của A
                    if norm_A < 1.0:
                        # Vây bắt con mồi (Exploitation)
                        new_pos = encircle_prey(whale.position, best_whale.position, A, C)
                    else:
                        # Tìm kiếm con mồi ngẫu nhiên (Exploration)
                        rand_idx = self.rng.integers(0, len(whales))
                        x_rand = whales[rand_idx].position
                        new_pos = search_for_prey(whale.position, x_rand, A, C)
                else:
                    # Tấn công bằng lưới bọt xoắn ốc (Spiral exploitation)
                    new_pos = spiral_update(
                        whale.position,
                        best_whale.position,
                        l=l,
                        b=self.params.spiral_constant,
                    )

                # Giới hạn vị trí trong miền tìm kiếm
                whale.position = handle_boundaries(new_pos, lb, ub)
                whale.fitness = problem.evaluate(whale.position)

                # Cập nhật cá thể tốt nhất
                if whale.fitness > best_whale.fitness:
                    best_whale = whale.copy()

            convergence_history.append(float(best_whale.fitness))

        runtime = time.perf_counter() - start_time

        return OptimizationResult(
            algorithm="WOA",
            best_position=best_whale.position.copy(),
            best_objective=float(best_whale.fitness),
            convergence_history=convergence_history,
            runtime_seconds=runtime,
            seed=self.seed,
        )
