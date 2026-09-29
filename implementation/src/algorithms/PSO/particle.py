"""Biểu diễn một hạt (Particle) trong thuật toán bầy đàn PSO."""

from dataclasses import dataclass

import numpy as np


@dataclass
class Particle:
    position: np.ndarray
    velocity: np.ndarray
    best_position: np.ndarray
    fitness: float = -np.inf
    best_fitness: float = -np.inf
