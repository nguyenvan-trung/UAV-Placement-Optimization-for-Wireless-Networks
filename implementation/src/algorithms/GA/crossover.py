"""Toán tử lai ghép Arithmetic / Blend Crossover cho GA liên tục."""

import numpy as np

from .chromosome import Chromosome


def arithmetic_crossover(
    parent1: Chromosome,
    parent2: Chromosome,
    crossover_rate: float,
    lower_bounds: np.ndarray,
    upper_bounds: np.ndarray,
    rng: np.random.Generator,
) -> tuple[Chromosome, Chromosome]:
    """Lai ghép số học (Arithmetic Crossover) giữa 2 cá thể cha mẹ."""
    if rng.random() > crossover_rate:
        return parent1.copy(), parent2.copy()

    # Hệ số lai ngẫu nhiên theo từng chiều
    dim = len(lower_bounds)
    alpha = rng.uniform(0.0, 1.0, size=dim)

    child1_genes = alpha * parent1.genes + (1.0 - alpha) * parent2.genes
    child2_genes = (1.0 - alpha) * parent1.genes + alpha * parent2.genes

    child1_genes = np.clip(child1_genes, lower_bounds, upper_bounds)
    child2_genes = np.clip(child2_genes, lower_bounds, upper_bounds)

    return Chromosome(genes=child1_genes), Chromosome(genes=child2_genes)
