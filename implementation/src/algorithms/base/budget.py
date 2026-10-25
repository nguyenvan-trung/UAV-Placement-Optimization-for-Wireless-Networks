"""Opt-in budget integration; calls without max_fe retain legacy behavior."""
from functools import wraps
import time
import numpy as np
from ...counter import BudgetExhausted, FitnessCounter
from .result import OptimizationResult


class CountedProblem:
    def __init__(self, problem, counter, initial_population):
        self.original = problem
        self.counter = counter
        self.initial_population = initial_population
        self.iterations_done = 0
        self.initializing = True

    def __getattr__(self, key):
        return getattr(self.original, key)

    def evaluate(self, position):
        return self.counter(position, 'initialization' if self.initializing else 'core')

    def evaluate_phase(self, position, phase):
        return self.counter(position, phase)


def evaluate_phase(problem, position, phase):
    if isinstance(problem, CountedProblem):
        return problem.evaluate_phase(position, phase)
    return problem.evaluate(position)


def initialize_paired(population, problem):
    if not isinstance(problem, CountedProblem) and not getattr(problem, 'paired_experiment', False):
        return
    positions = problem.initial_population
    if len(population) != len(positions):
        raise ValueError('Initial population size mismatch')
    for individual, position in zip(population, positions):
        if hasattr(individual, 'genes'):
            individual.genes = position.copy()
        else:
            individual.position = position.copy()
            if hasattr(individual, 'best_position'):
                individual.best_position = position.copy()


def iterations(problem, legacy_iterations):
    if not isinstance(problem, CountedProblem):
        for index in range(legacy_iterations):
            if getattr(problem, 'paired_experiment', False):
                problem.record_iteration(index)
            yield index
        if getattr(problem, 'paired_experiment', False):
            problem.record_iteration(legacy_iterations)
        return
    problem.initializing = False
    while True:
        yield problem.iterations_done
        problem.iterations_done += 1
        if problem.counter.fe_count >= problem.counter.max_fe:
            raise BudgetExhausted()


def progress(problem, iteration, total):
    if isinstance(problem, CountedProblem):
        return problem.counter.fe_count / problem.counter.max_fe
    return iteration / max(1, total - 1)


def budgeted(method):
    @wraps(method)
    def run(self, problem, *, max_fe=None, initial_population=None, target=None):
        if max_fe is None:
            return method(self, problem)
        size = getattr(self.params, 'population_size', getattr(self.params, 'swarm_size', None))
        if not isinstance(size, int) or size < 3:
            raise ValueError('Budgeted optimizers require population size >= 3')
        lb, ub = problem.search_space.lower_bounds, problem.search_space.upper_bounds
        if initial_population is None:
            initial_population = np.random.default_rng(self.seed).uniform(lb, ub, (size, len(lb)))
        positions = np.asarray(initial_population, dtype=float)
        if positions.shape != (size, len(lb)) or not np.isfinite(positions).all() or (positions < lb).any() or (positions > ub).any():
            raise ValueError('Invalid paired initial population')
        counter = FitnessCounter(problem.evaluate, max_fe, target=target)
        counted = CountedProblem(problem, counter, positions.copy())
        self.rng = np.random.default_rng(self.seed)
        started = time.perf_counter()
        try:
            method(self, counted)
        except BudgetExhausted:
            pass
        if counter.fe_count != max_fe:
            raise RuntimeError('Optimizer returned before consuming the FE budget')
        result = OptimizationResult(type(self).__name__, counter.best_position.copy(),
            counter.best_fitness, [r['best_fitness'] for r in counter.history],
            time.perf_counter() - started, self.seed)
        result.fe_used = counter.fe_count
        result.iterations_done = counted.iterations_done
        result.fe_history = counter.history
        result.fe_phase_counts = dict(counter.phase_counts)
        result.fe_to_target = counter.fe_to_target
        return result
    return run
