"""Thuật toán Whale Optimization Algorithm cải tiến (I-WOA).

Tích hợp 3 cải tiến khoa học cốt lõi:
1. K-Means Smart Initialization: Gom cụm người dùng đặt vị trí mầm.
2. Opposition-Based Learning (OBL): Tăng tốc hội tụ bằng quần thể đối kháng.
3. Levy Flight Mutation: Đột biến bước nhảy phân phối nặng thoát khỏi cực trị địa phương.
"""

import time

import numpy as np

from ..base.result import OptimizationResult
from ...preprocessing.kmeans_init import generate_kmeans_uav_initial_guess
from ..WOA.boundary_handler import handle_boundaries
from ..WOA.coefficient_update import update_coefficients
from ..WOA.encircling import encircle_prey
from ..WOA.exploration import search_for_prey
from ..WOA.initialization import initialize_whales
from ..WOA.spiral_update import spiral_update
from ..WOA.whale import Whale
from .levy_flight import apply_levy_flight, compute_levy_sigma
from .obl import apply_obl_population
from .parameters import IWOAParameters


class IWOAOptimizer:
    """Bộ tối ưu hóa I-WOA (Whale Optimization Algorithm cải tiến)."""

    def __init__(self, parameters: IWOAParameters | None = None, seed: int = 42):
        self.params = parameters or IWOAParameters()
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.sigma_u = compute_levy_sigma(self.params.levy_beta)

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

        # 1.1. Cải tiến K-Means Smart Initialization
        if self.params.use_kmeans_init and hasattr(problem, "ue_coords") and hasattr(problem, "num_uavs"):
            try:
                kmeans_guess = generate_kmeans_uav_initial_guess(
                    ue_coords=problem.ue_coords,
                    num_uavs=problem.num_uavs,
                    random_state=self.seed,
                )
                whales[0].position = np.clip(kmeans_guess, lb, ub)
            except Exception:
                pass

        # Đánh giá ban đầu
        for w in whales:
            w.fitness = problem.evaluate(w.position)

        # 1.2. Cải tiến Opposition-Based Learning (OBL) khởi tạo
        if self.params.use_obl_init:
            whales = apply_obl_population(whales, problem, lb, ub)

        best_whale = max(whales, key=lambda w: w.fitness).copy()
        convergence_history: list[float] = [float(best_whale.fitness)]

        # 2. Vòng lặp chính I-WOA
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
                    norm_A = np.linalg.norm(A) / np.sqrt(dim)
                    if norm_A < 1.0:
                        new_pos = encircle_prey(whale.position, best_whale.position, A, C)
                    else:
                        rand_idx = self.rng.integers(0, len(whales))
                        new_pos = search_for_prey(whale.position, whales[rand_idx].position, A, C)
                else:
                    new_pos = spiral_update(
                        whale.position,
                        best_whale.position,
                        l=l,
                        b=self.params.spiral_constant,
                    )

                new_pos = handle_boundaries(new_pos, lb, ub)
                new_fit = problem.evaluate(new_pos)

                # 2.1. Cải tiến Bước nhảy Levy Flight
                # Khi cá thể không cải thiện hoặc theo xác suất ngẫu nhiên, kích hoạt Levy Flight
                if self.rng.uniform(0.0, 1.0) < 0.3:
                    levy_pos = apply_levy_flight(
                        position=new_pos,
                        best_position=best_whale.position,
                        lower_bounds=lb,
                        upper_bounds=ub,
                        beta=self.params.levy_beta,
                        sigma_u=self.sigma_u,
                        step_size=self.params.levy_step_size,
                        rng=self.rng,
                    )
                    levy_fit = problem.evaluate(levy_pos)
                    if levy_fit > new_fit:
                        new_pos = levy_pos
                        new_fit = levy_fit

                whale.position = new_pos
                whale.fitness = new_fit

                if whale.fitness > best_whale.fitness:
                    best_whale = whale.copy()

            # 2.2. Dynamic OBL định kỳ
            if self.rng.uniform(0.0, 1.0) < self.params.obl_rate:
                # Tính biên động hiện tại của quần thể
                positions = np.array([w.position for w in whales])
                dyn_lb = np.min(positions, axis=0)
                dyn_ub = np.max(positions, axis=0)
                whales = apply_obl_population(whales, problem, dyn_lb, dyn_ub)
                current_best = max(whales, key=lambda w: w.fitness)
                if current_best.fitness > best_whale.fitness:
                    best_whale = current_best.copy()

            convergence_history.append(float(best_whale.fitness))

        runtime = time.perf_counter() - start_time

        return OptimizationResult(
            algorithm="I-WOA",
            best_position=best_whale.position.copy(),
            best_objective=float(best_whale.fitness),
            convergence_history=convergence_history,
            runtime_seconds=runtime,
            seed=self.seed,
        )
