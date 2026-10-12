
"""Các thành phần được ghép lại để tạo Genetic Algorithm."""
"""Package Genetic Algorithm (GA)."""

from .chromosome import Chromosome
from .optimizer import GAOptimizer
from .parameters import GAParameters
__all__ = ["GAOptimizer", "GAParameters", "Chromosome"]

