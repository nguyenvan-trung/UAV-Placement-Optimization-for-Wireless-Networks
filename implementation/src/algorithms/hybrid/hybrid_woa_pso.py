"""Thuật toán lai ghép Hybrid WOA-PSO (H-WOA-PSO).

Kết hợp cơ chế lưới bọt xoắn ốc (Spiral Bubble-net) của WOA
với cập nhật vận tốc pbest/gbest của PSO.
"""

import time
from dataclasses import dataclass

import numpy as np

from ..base.result import OptimizationResult
from ..WOA.boundary_handler import handle_boundaries
from ..WOA.coefficient_update import update_coefficients
from ..WOA.encircling import encircle_prey
from ..WOA.exploration import search_for_prey
from ..WOA.initialization import initialize_whales
from ..WOA.spiral_update import spiral_update


@dataclass(frozen=True)
class HWOAPSOParameters:
    population_size: int = 30
    iterations: int = 100
    spiral_constant: float = 1.0
    c1: float = 1.2
    c2: float = 1.2


class HybridWOAPSOOptimizer:
    """Bộ tối ưu hóa lai WOA và PSO."""

    def __init__(self, parameters: HWOAPSOParameters | None = None, seed: int = 42):
        self.params = parameters or HWOAPSOParameters()
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def optimize(self, problem: object) -> OptimizationResult:
        start_time = time.perf_counter()

        lb = problem.search_space.lower_bounds
        ub = problem.search_space.upper_bounds
        dim = len(lb)
        ranges = ub - lb
        v_max = 0.2 * ranges

        # Khởi tạo cá kình và vận tốc kèm pbest
        whales = initialize_whales(
            population_size=self.params.population_size,
            lower_bounds=lb,
            upper_bounds=ub,
            rng=self.rng,
        )

        velocities = [self.rng.uniform(-v_max, v_max, size=dim) for _ in whales]
        pbests = [w.position.copy() for w in whales]
        pbest_fits = [-np.inf for _ in whales]

        for i, w in enumerate(whales):
            w.fitness = problem.evaluate(w.position)
            pbests[i] = w.position.copy()
            pbest_fits[i] = w.fitness

        best_whale = max(whales, key=lambda w: w.fitness).copy()
        convergence_history: list[float] = [float(best_whale.fitness)]

        w_max, w_min = 0.9, 0.4
        for t in range(self.params.iterations):
            w = w_max - (w_max - w_min) * (t / max(1, self.params.iterations - 1))

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
                        # WOA Encircling
                        woa_pos = encircle_prey(whale.position, best_whale.position, A, C)
                    else:
                        # WOA Exploration
                        rand_idx = self.rng.integers(0, len(whales))
                        woa_pos = search_for_prey(whale.position, whales[rand_idx].position, A, C)
                else:
                    # WOA Spiral
                    woa_pos = spiral_update(
                        whale.position,
                        best_whale.position,
                        l=l,
                        b=self.params.spiral_constant,
                    )

                # Kết hợp thành phần vận tốc của PSO để định hướng
                r1 = self.rng.uniform(0.0, 1.0, size=dim)
                r2 = self.rng.uniform(0.0, 1.0, size=dim)
                velocities[i] = (
                    w * velocities[i]
                    + self.params.c1 * r1 * (pbests[i] - whale.position)
                    + self.params.c2 * r2 * (best_whale.position - whale.position)
                )
                velocities[i] = np.clip(velocities[i], -v_max, v_max)

                # Vị trí mới là sự kết hợp giữa bước nhảy WOA và vận tốc PSO
                new_pos = 0.5 * woa_pos + 0.5 * (whale.position + velocities[i])
                whale.position = handle_boundaries(new_pos, lb, ub)
                whale.fitness = problem.evaluate(whale.position)

                # Cập nhật pbest và gbest
                if whale.fitness > pbest_fits[i]:
                    pbest_fits[i] = whale.fitness
                    pbests[i] = whale.position.copy()

                if whale.fitness > best_whale.fitness:
                    best_whale = whale.copy()

            convergence_history.append(float(best_whale.fitness))

        runtime = time.perf_counter() - start_time

        return OptimizationResult(
            algorithm="Hybrid-WOA-PSO",
            best_position=best_whale.position.copy(),
            best_objective=float(best_whale.fitness),
            convergence_history=convergence_history,
            runtime_seconds=runtime,
            seed=self.seed,
        )
