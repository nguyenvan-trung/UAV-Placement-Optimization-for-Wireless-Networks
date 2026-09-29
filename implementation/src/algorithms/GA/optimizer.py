"""Vòng lặp chính thuật toán Genetic Algorithm (GA)."""

import time

import numpy as np

from ..base.result import OptimizationResult
from .crossover import arithmetic_crossover
from .fitness import evaluate_population
from .initialization import initialize_population
from .mutation import gaussian_mutation
from .parameters import GAParameters
from .replacement import elitism_replacement
from .selection import tournament_selection


class GAOptimizer:
    """Thuật toán di truyền chuẩn (Genetic Algorithm - Baseline)."""

    def __init__(self, parameters: GAParameters | None = None, seed: int = 42):
        self.params = parameters or GAParameters()
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def optimize(self, problem: object) -> OptimizationResult:
        start_time = time.perf_counter()

        lb = problem.search_space.lower_bounds
        ub = problem.search_space.upper_bounds

        # 1. Khởi tạo quần thể
        population = initialize_population(
            pop_size=self.params.population_size,
            lower_bounds=lb,
            upper_bounds=ub,
            rng=self.rng,
        )

        # 2. Đánh giá thế hệ đầu tiên
        evaluate_population(population, problem)

        # Lưu cá thể tốt nhất
        best_individual = max(population, key=lambda c: c.fitness).copy()
        convergence_history: list[float] = [best_individual.fitness]

        # 3. Vòng lặp tiến hóa qua các thế hệ
        for _ in range(self.params.generations):
            offspring: list = []

            # Tạo ra thế hệ con
            while len(offspring) < self.params.population_size:
                # Chọn lọc
                p1 = tournament_selection(population, tournament_size=3, rng=self.rng)
                p2 = tournament_selection(population, tournament_size=3, rng=self.rng)

                # Lai ghép
                c1, c2 = arithmetic_crossover(
                    p1, p2,
                    crossover_rate=self.params.crossover_rate,
                    lower_bounds=lb,
                    upper_bounds=ub,
                    rng=self.rng,
                )

                # Đột biến
                c1 = gaussian_mutation(
                    c1,
                    mutation_rate=self.params.mutation_rate,
                    lower_bounds=lb,
                    upper_bounds=ub,
                    rng=self.rng,
                )
                c2 = gaussian_mutation(
                    c2,
                    mutation_rate=self.params.mutation_rate,
                    lower_bounds=lb,
                    upper_bounds=ub,
                    rng=self.rng,
                )

                offspring.extend([c1, c2])

            # Đánh giá fitness cho thế hệ con
            evaluate_population(offspring, problem)

            # Thay thế quần thể kết hợp Elitism
            population = elitism_replacement(
                current_population=population,
                offspring_population=offspring,
                elite_count=self.params.elite_count,
                pop_size=self.params.population_size,
            )

            # Cập nhật cá thể tốt nhất toàn cục
            current_best = max(population, key=lambda c: c.fitness)
            if current_best.fitness > best_individual.fitness:
                best_individual = current_best.copy()

            convergence_history.append(best_individual.fitness)

        runtime = time.perf_counter() - start_time

        return OptimizationResult(
            algorithm="GA",
            best_position=best_individual.genes.copy(),
            best_objective=float(best_individual.fitness),
            convergence_history=convergence_history,
            runtime_seconds=runtime,
            seed=self.seed,
        )
