"""Toán tử đột biến Gaussian Mutation cho GA liên tục."""

import numpy as np

from .chromosome import Chromosome


def gaussian_mutation(
    chromosome: Chromosome,
    mutation_rate: float,
    lower_bounds: np.ndarray,
    upper_bounds: np.ndarray,
    rng: np.random.Generator,
    scale: float = 0.1,
) -> Chromosome:
    """Đột biến Gaussian trên các gene với xác suất mutation_rate."""
    mutated_genes = chromosome.genes.copy()
    dim = len(lower_bounds)
    ranges = upper_bounds - lower_bounds

    for i in range(dim):
        if rng.random() < mutation_rate:
            step = rng.normal(loc=0.0, scale=scale * ranges[i])
            mutated_genes[i] += step

    mutated_genes = np.clip(mutated_genes, lower_bounds, upper_bounds)
    return Chromosome(genes=mutated_genes)
