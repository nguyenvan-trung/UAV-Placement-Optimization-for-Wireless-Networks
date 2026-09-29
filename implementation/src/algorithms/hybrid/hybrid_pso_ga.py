"""Thuật toán lai ghép Hybrid PSO-GA (H-PSO-GA).

Kết hợp thế mạnh:
- PSO: Tốc độ hội tụ và khai thác cực nhanh theo pbest và gbest.
- GA: Duy trì đa dạng quần thể thông qua lai ghép (Crossover) và đột biến (Mutation),
  giúp bầy hạt thoát khỏi bẫy cực trị địa phương (Local Optima).
"""

import time
from dataclasses import dataclass

import numpy as np

from ..base.result import OptimizationResult
from ..GA.crossover import arithmetic_crossover
from ..GA.mutation import gaussian_mutation
from ..GA.chromosome import Chromosome
from ..PSO.best_update import update_bests
from ..PSO.boundary_handler import handle_boundaries
from ..PSO.initialization import initialize_swarm
from ..PSO.particle import Particle
from ..PSO.position_update import update_position
from ..PSO.velocity_update import update_velocity


@dataclass(frozen=True)
class HPSOGAParameters:
    population_size: int = 30
    iterations: int = 100
    cognitive_coefficient: float = 1.5
    social_coefficient: float = 1.5
    crossover_rate: float = 0.8
    mutation_rate: float = 0.15


class HybridPSOGAOptimizer:
    """Bộ tối ưu hóa kết hợp Hybrid PSO-GA."""

    def __init__(self, parameters: HPSOGAParameters | None = None, seed: int = 42):
        self.params = parameters or HPSOGAParameters()
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def optimize(self, problem: object) -> OptimizationResult:
        start_time = time.perf_counter()

        lb = problem.search_space.lower_bounds
        ub = problem.search_space.upper_bounds
        ranges = ub - lb
        v_max = 0.2 * ranges

        # 1. Khởi tạo bầy hạt PSO
        swarm = initialize_swarm(
            swarm_size=self.params.population_size,
            lower_bounds=lb,
            upper_bounds=ub,
            rng=self.rng,
        )

        # 2. Đánh giá ban đầu
        for p in swarm:
            p.fitness = problem.evaluate(p.position)
            p.best_fitness = p.fitness
            p.best_position = p.position.copy()

        best_particle = max(swarm, key=lambda p: p.fitness)
        gbest_position = best_particle.position.copy()
        gbest_fitness = float(best_particle.fitness)

        convergence_history: list[float] = [gbest_fitness]

        w_max, w_min = 0.9, 0.4
        for t in range(self.params.iterations):
            # Hệ số quán tính PSO suy giảm
            w = w_max - (w_max - w_min) * (t / max(1, self.params.iterations - 1))

            # --- Pha 1: Cập nhật vận tốc và vị trí kiểu PSO ---
            for p in swarm:
                p.velocity = update_velocity(
                    particle=p,
                    global_best_position=gbest_position,
                    w=w,
                    c1=self.params.cognitive_coefficient,
                    c2=self.params.social_coefficient,
                    v_max=v_max,
                    rng=self.rng,
                )
                p.position = update_position(p)
                handle_boundaries(p, lb, ub)

            # --- Pha 2: Lai ghép (Crossover) và Đột biến (Mutation) kiểu GA ---
            # Chọn ngẫu nhiên các cặp hạt để lai ghép, tăng tính đa dạng
            indices = self.rng.permutation(len(swarm))
            for i in range(0, len(swarm) - 1, 2):
                idx1, idx2 = indices[i], indices[i + 1]
                p1, p2 = swarm[idx1], swarm[idx2]

                c1 = Chromosome(genes=p1.position.copy())
                c2 = Chromosome(genes=p2.position.copy())

                c1_crossed, c2_crossed = arithmetic_crossover(
                    parent1=c1,
                    parent2=c2,
                    crossover_rate=self.params.crossover_rate,
                    lower_bounds=lb,
                    upper_bounds=ub,
                    rng=self.rng,
                )

                # Đột biến cá thể con
                c1_mutated = gaussian_mutation(
                    chromosome=c1_crossed,
                    mutation_rate=self.params.mutation_rate,
                    lower_bounds=lb,
                    upper_bounds=ub,
                    rng=self.rng,
                )
                c2_mutated = gaussian_mutation(
                    chromosome=c2_crossed,
                    mutation_rate=self.params.mutation_rate,
                    lower_bounds=lb,
                    upper_bounds=ub,
                    rng=self.rng,
                )

                # Gán lại vị trí mới sau khi lai ghép & đột biến
                p1.position = c1_mutated.genes.copy()
                p2.position = c2_mutated.genes.copy()

            # --- Pha 3: Đánh giá và cập nhật pbest / gbest ---
            for p in swarm:
                handle_boundaries(p, lb, ub)
                p.fitness = problem.evaluate(p.position)

            gbest_position, gbest_fitness = update_bests(swarm, gbest_position, gbest_fitness)
            convergence_history.append(gbest_fitness)

        runtime = time.perf_counter() - start_time

        return OptimizationResult(
            algorithm="Hybrid-PSO-GA",
            best_position=gbest_position.copy(),
            best_objective=float(gbest_fitness),
            convergence_history=convergence_history,
            runtime_seconds=runtime,
            seed=self.seed,
        )
