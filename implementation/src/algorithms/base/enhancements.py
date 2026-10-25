"""Optional K/OBL/Levy operators for GA and PSO experiments."""
import copy
import numpy as np
from ...preprocessing.kmeans_init import generate_kmeans_uav_initial_guess
from ..I_WOA.levy_flight import apply_levy_flight, compute_levy_sigma
from .budget import evaluate_phase


def position(individual):
    return individual.genes if hasattr(individual, 'genes') else individual.position


def assign(individual, value, fitness=None):
    if hasattr(individual, 'genes'):
        individual.genes = value.copy()
    else:
        individual.position = value.copy()
        individual.velocity[:] = 0
        # Preserve the historical personal best when replacing a position.
        if fitness is not None and fitness > individual.best_fitness:
            individual.best_position = value.copy()
            individual.best_fitness = fitness
    if fitness is not None:
        individual.fitness = fitness


def seed_kmeans(population, problem, params, seed):
    if params.use_kmeans_init:
        value = generate_kmeans_uav_initial_guess(problem.ue_coords, problem.num_uavs, random_state=seed)
        assign(population[0], problem.search_space.clip(value))


def opposition(population, problem, lower, upper):
    candidates = list(population)
    for original in population:
        candidate = copy.deepcopy(original)
        value = problem.search_space.clip(lower + upper - position(original))
        assign(candidate, value, evaluate_phase(problem, value, 'obl'))
        candidates.append(candidate)
    return sorted(candidates, key=lambda x: x.fitness, reverse=True)[:len(population)]


def enhance(population, problem, params, rng, best, *, initial=False):
    if initial:
        if params.use_obl:
            return opposition(population, problem, problem.search_space.lower_bounds, problem.search_space.upper_bounds)
        return population
    if params.use_levy:
        for individual in population:
            if rng.random() < params.levy_rate:
                value = apply_levy_flight(position(individual), best,
                    problem.search_space.lower_bounds, problem.search_space.upper_bounds,
                    params.levy_beta, compute_levy_sigma(params.levy_beta), params.levy_step_size, rng)
                fitness = evaluate_phase(problem, value, 'levy')
                if fitness > individual.fitness:
                    assign(individual, value, fitness)
    if params.use_obl and rng.random() < params.obl_rate:
        positions = np.array([position(x) for x in population])
        population = opposition(population, problem, positions.min(axis=0), positions.max(axis=0))
    return population
