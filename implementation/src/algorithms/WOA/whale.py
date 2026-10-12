"""Biểu diễn một cá thể cá kình (Whale) trong WOA."""

from dataclasses import dataclass

import numpy as np


@dataclass
class Whale:
    position: np.ndarray
    fitness: float = -np.inf

    def copy(self) -> "Whale":
        return Whale(position=self.position.copy(), fitness=self.fitness)
