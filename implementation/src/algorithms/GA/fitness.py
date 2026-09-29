"""Đánh giá hàm thích nghi (Fitness) cho quần thể GA."""

from .chromosome import Chromosome


def evaluate_population(population: list[Chromosome], problem: object) -> None:
    """Tính toán và gán fitness cho từng cá thể trong quần thể."""
    for ind in population:
        ind.fitness = problem.evaluate(ind.genes)
