"""Toán tử thay thế quần thể kết hợp Elitism cho GA."""

from .chromosome import Chromosome


def elitism_replacement(
    current_population: list[Chromosome],
    offspring_population: list[Chromosome],
    elite_count: int,
    pop_size: int,
) -> list[Chromosome]:
    """Giữ lại elite_count cá thể tốt nhất từ thế hệ hiện tại và ghép với con cháu."""
    # Sắp xếp cá thể tốt nhất lên đầu
    sorted_current = sorted(current_population, key=lambda c: c.fitness, reverse=True)
    elites = [c.copy() for c in sorted_current[:elite_count]]

    # Sắp xếp offspring và lấy phần còn lại
    sorted_offspring = sorted(offspring_population, key=lambda c: c.fitness, reverse=True)
    remaining_needed = pop_size - elite_count
    new_population = elites + sorted_offspring[:remaining_needed]

    return new_population
