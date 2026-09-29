"""Vòng lặp chính thuật toán Particle Swarm Optimization (PSO)."""

import time

import numpy as np

from ..base.result import OptimizationResult
from .best_update import update_bests
from .boundary_handler import handle_boundaries
from .initialization import initialize_swarm
from .parameters import PSOParameters
from .position_update import update_position
from .velocity_update import update_velocity


class PSOOptimizer:
    """Thuật toán bầy đàn chuẩn (Particle Swarm Optimization - Baseline)."""

    def __init__(self, parameters: PSOParameters | None = None, seed: int = 42):
        self.params = parameters or PSOParameters()
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def optimize(self, problem: object) -> OptimizationResult:
        start_time = time.perf_counter()

        lb = problem.search_space.lower_bounds
        ub = problem.search_space.upper_bounds
        ranges = ub - lb
        v_max = 0.2 * ranges

        # 1. Khởi tạo bầy hạt
        swarm = initialize_swarm(
            swarm_size=self.params.swarm_size,
            lower_bounds=lb,
            upper_bounds=ub,
            rng=self.rng,
        )

        # 2. Đánh giá vị trí ban đầu
        for p in swarm:
            p.fitness = problem.evaluate(p.position)
            p.best_fitness = p.fitness
            p.best_position = p.position.copy()

        # Tìm gbest khởi tạo
        best_particle = max(swarm, key=lambda p: p.fitness)
        gbest_position = best_particle.position.copy()
        gbest_fitness = float(best_particle.fitness)

        convergence_history: list[float] = [gbest_fitness]

        # 3. Vòng lặp tối ưu bầy đàn
        w_max, w_min = 0.9, 0.4
        for t in range(self.params.iterations):
            # Trọng số quán tính suy giảm tuyến tính
            w = w_max - (w_max - w_min) * (t / max(1, self.params.iterations - 1))

            for p in swarm:
                # Cập nhật vận tốc
                p.velocity = update_velocity(
                    particle=p,
                    global_best_position=gbest_position,
                    w=w,
                    c1=self.params.cognitive_coefficient,
                    c2=self.params.social_coefficient,
                    v_max=v_max,
                    rng=self.rng,
                )

                # Cập nhật vị trí
                p.position = update_position(p)

                # Xử lý biên
                handle_boundaries(p, lb, ub)

                # Đánh giá fitness
                p.fitness = problem.evaluate(p.position)

            # Cập nhật pbest và gbest
            gbest_position, gbest_fitness = update_bests(swarm, gbest_position, gbest_fitness)
            convergence_history.append(gbest_fitness)

        runtime = time.perf_counter() - start_time

        return OptimizationResult(
            algorithm="PSO",
            best_position=gbest_position.copy(),
            best_objective=float(gbest_fitness),
            convergence_history=convergence_history,
            runtime_seconds=runtime,
            seed=self.seed,
        )
