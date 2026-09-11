"""Protocol mà GA, PSO và WOA phải tuân theo."""

from typing import Protocol

from .result import OptimizationResult


class Optimizer(Protocol):
    def optimize(self, problem: object) -> OptimizationResult:
        ...
