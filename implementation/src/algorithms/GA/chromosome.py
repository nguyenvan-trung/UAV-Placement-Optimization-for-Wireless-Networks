"""Biểu diễn cá thể (Chromosome) trong GA cho bài toán liên tục."""

from dataclasses import dataclass

import numpy as np


@dataclass
class Chromosome:
    genes: np.ndarray
    fitness: float = -np.inf

    def copy(self) -> "Chromosome":
        return Chromosome(genes=self.genes.copy(), fitness=self.fitness)
