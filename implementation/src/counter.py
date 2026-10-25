"""Shared maximize FE budget. Failed feasibility evaluations also consume one FE."""
from collections import Counter
import numpy as np


class BudgetExhausted(Exception):
    pass


class FitnessCounter:
    def __init__(self, fitness, max_fe, interval=50, target=None):
        if not isinstance(max_fe, int) or max_fe < 1 or interval < 1:
            raise ValueError('Positive integer FE budget and logging interval required')
        self.fitness = fitness
        self.max_fe = max_fe
        self.interval = interval
        self.target = target
        self.fe_count = 0
        self.best_fitness = -np.inf
        self.best_position = None
        self.history = []
        self.phase_counts = Counter()
        self.fe_to_target = None

    def __call__(self, position, phase='core'):
        if self.fe_count >= self.max_fe:
            raise BudgetExhausted()
        value = float(self.fitness(position))
        if np.isnan(value) or value == np.inf:
            raise ValueError('Fitness returned NaN or positive infinity')
        self.fe_count += 1
        self.phase_counts[phase] += 1
        if self.best_position is None or value > self.best_fitness:
            self.best_fitness = value
            self.best_position = np.asarray(position, dtype=float).copy()
        if self.target is not None and self.fe_to_target is None and value >= self.target:
            self.fe_to_target = self.fe_count
        if self.fe_count % self.interval == 0 or self.fe_count == self.max_fe:
            self.history.append({'fe': self.fe_count, 'best_fitness': self.best_fitness})
        return value
