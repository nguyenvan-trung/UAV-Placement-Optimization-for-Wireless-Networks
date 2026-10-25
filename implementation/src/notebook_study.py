"""Explicitly invoked 100-iteration study on existing CSVs; no work at import."""
import hashlib
import itertools
import json
import os
import time
from pathlib import Path

import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

from .algorithms import (GAOptimizer, GAParameters, PSOOptimizer, PSOParameters,
    WOAOptimizer, WOAParameters, IWOAOptimizer, IWOAParameters,
    HybridPSOGAOptimizer, HPSOGAParameters, HybridWOAPSOOptimizer, HWOAPSOParameters)
from .input.data_loader import load_users
from .input.data_validator import validate_users
from .preprocessing.preprocessor import preprocess_users
from .problem.objective import UAVPlacementProblem


def cases():
    """24 factorial cases + two hybrids + four hybrid ablations."""
    rows = []
    for family in ('WOA', 'PSO', 'GA'):
        for k, o, l in itertools.product((False, True), repeat=3):
            suffix = ''.join(letter for letter, flag in zip('KOL', (k, o, l)) if flag)
            name = family if not suffix else f'{family}-{suffix}'
            if family == 'WOA' and suffix == 'KOL':
                name = 'I-WOA'
            rows.append(dict(case=name, family=family, K=k, O=o, L=l))
    rows.extend([
        dict(case='H-PSO-GA', family='H-PSO-GA', crossover=True, mutation=True),
        dict(case='PSO+Crossover', family='H-PSO-GA', crossover=True, mutation=False),
        dict(case='PSO+Mutation', family='H-PSO-GA', crossover=False, mutation=True),
        dict(case='H-WOA-PSO', family='H-WOA-PSO', personal=True, global_attraction=True),
        dict(case='H-WOA-PSO-no-pbest', family='H-WOA-PSO', personal=False, global_attraction=True),
        dict(case='H-WOA-PSO-no-gbest-velocity', family='H-WOA-PSO', personal=True, global_attraction=False),
    ])
    return rows


MAIN = ['GA', 'PSO', 'WOA', 'H-PSO-GA', 'H-WOA-PSO', 'I-WOA']
GROUPS = {'main': MAIN,
    **{family: [c['case'] for c in cases() if c['family'] == family] for family in ('WOA', 'PSO', 'GA')},
    'hybrid_pso_ga': ['PSO', 'PSO+Crossover', 'PSO+Mutation', 'H-PSO-GA'],
    'hybrid_woa_pso': ['WOA', 'PSO', 'H-WOA-PSO-no-pbest', 'H-WOA-PSO-no-gbest-velocity', 'H-WOA-PSO']}


def make_case(case, population, iterations, seed):
    family = case['family']
    flags = dict(use_kmeans_init=case.get('K', False), use_obl=case.get('O', False), use_levy=case.get('L', False))
    if family == 'WOA':
        if not any(flags.values()):
            return WOAOptimizer(WOAParameters(population_size=population, iterations=iterations), seed=seed)
        return IWOAOptimizer(IWOAParameters(population_size=population, iterations=iterations, **flags), seed=seed)
    if family == 'GA':
        return GAOptimizer(GAParameters(population_size=population, generations=iterations, **flags), seed=seed)
    if family == 'PSO':
        return PSOOptimizer(PSOParameters(swarm_size=population, iterations=iterations, **flags), seed=seed)
    if family == 'H-PSO-GA':
        return HybridPSOGAOptimizer(HPSOGAParameters(population_size=population, iterations=iterations,
            use_crossover=case['crossover'], use_mutation=case['mutation']), seed=seed)
    return HybridWOAPSOOptimizer(HWOAPSOParameters(population_size=population, iterations=iterations,
        use_personal_attraction=case['personal'], use_global_attraction=case['global_attraction']), seed=seed)


class ObservedProblem:
    """Counts actual optimization FE and records the best evaluated feasible point."""
    paired_experiment = True

    def __init__(self, original, initial):
        self.original = original
        self.initial_population = initial.copy()
        self.fe = 0
        self.best = -np.inf
        self.position = None
        self.history = []
        self.started = time.perf_counter()

    def __getattr__(self, key):
        return getattr(self.original, key)

    def evaluate(self, value):
        score = self.original.evaluate(value)
        self.fe += 1
        if np.isfinite(score) and score > self.best:
            self.best = float(score)
            self.position = np.asarray(value).copy()
        return score

    def record_iteration(self, iteration):
        if self.position is None:
            raise ValueError('No feasible point evaluated; inspect input/configuration')
        elapsed = time.perf_counter() - self.started
        metrics = self.original.evaluate_detailed(self.position)
        self.history.append(dict(iteration=iteration, fitness=self.best, fe=self.fe,
            elapsed_s=elapsed, coverage=metrics.coverage_rate, energy=metrics.energy_normalized,
            interference=metrics.interference_rate, position=self.position.tolist()))


def plan(root, config):
    files = sorted((root / 'data/stores').glob('*_users_connect.csv'))
    if len(files) != 500:
        raise ValueError(f'Expected 500 input CSVs, found {len(files)}')
    if config['iterations'] != 100 or config['population'] < 3 or config['num_uavs'] < 1:
        raise ValueError('Study requires 100 iterations, population >= 3 and positive UAV count')
    seeds = config['seeds']
    if len(seeds) != len(set(seeds)) or any(type(s) is not int or not 0 <= s < 2**32 for s in seeds):
        raise ValueError('Seeds must be distinct integers in [0, 2**32)')
    return files, cases(), len(files) * len(cases()) * len(seeds)


def atomic_json(path, value):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, allow_nan=False), encoding='utf-8')
    temp.replace(path)


def study_signature(root, config, files):
    h = hashlib.sha256(json.dumps(config, sort_keys=True).encode())
    for path in sorted((root / 'implementation/src').rglob('*.py')) + files:
        h.update(str(path.relative_to(root)).encode())
        h.update(path.read_bytes())
    return h.hexdigest()


def read_results(output, *, include_history=False):
    records, histories = [], []
    for path in sorted((output / 'tasks').glob('*.json')):
        artifact = json.loads(path.read_text(encoding='utf-8'))
        records.append(artifact['result'])
        if include_history:
            histories.extend(dict(dataset=artifact['result']['dataset'], case=artifact['result']['case'],
                seed=artifact['result']['seed'], **row) for row in artifact['history'])
    return pd.DataFrame(records), pd.DataFrame(histories)


def run_study(root, config, *, confirmed=False):
    if not confirmed:
        raise RuntimeError('Run disabled: explicit confirmation is required')
    files, variants, expected = plan(root, config)
    if len(config['seeds']) < 2:
        raise ValueError('Choose at least two evaluation seeds before running; seed count is not finalized')
    output = (root / config['output']).resolve()
    if not output.is_relative_to((root / 'implementation/results').resolve()):
        raise ValueError('Output must be inside implementation/results')
    output.mkdir(parents=True, exist_ok=True)
    lock = output / '.running'
    # Exclusive lock prevents two notebook kernels writing the same task directory.
    with lock.open('x', encoding='utf-8') as stream:
        stream.write(str(os.getpid()))
    try:
        signature = study_signature(root, config, files)
        manifest = output / 'manifest.json'
        if manifest.exists():
            if json.loads(manifest.read_text(encoding='utf-8'))['signature'] != signature:
                raise ValueError('Source, input data or configuration changed; use a new output directory')
        elif any(p.name != '.running' for p in output.iterdir()):
            raise ValueError('Output is not empty and has no manifest')
        atomic_json(manifest, dict(signature=signature, config=config, expected_tasks=expected,
            datasets=[p.name for p in files], cases=variants))
        tasks = output / 'tasks'
        tasks.mkdir(exist_ok=True)
        completed = 0
        with threadpool_limits(limits=1):
            for path in files:
                users = load_users(path)
                validate_users(users)
                users = preprocess_users(users)
                coords = users[['x_m', 'y_m', 'z_m']].to_numpy()
                for seed in config['seeds']:
                    original = UAVPlacementProblem(coords, num_uavs=config['num_uavs'])
                    rng = np.random.default_rng(np.random.SeedSequence([seed, 1]))
                    initial = rng.uniform(original.search_space.lower_bounds, original.search_space.upper_bounds,
                        (config['population'], original.dimension))
                    for case in variants:
                        task_id = hashlib.sha256(f"{path.name}|{seed}|{case['case']}".encode()).hexdigest()[:24]
                        destination = tasks / f'{task_id}.json'
                        if not destination.exists():
                            observed = ObservedProblem(original, initial)
                            optimizer = make_case(case, config['population'], config['iterations'], seed)
                            result = optimizer.optimize(observed)
                            if len(observed.history) != 101 or not original.is_feasible(observed.position):
                                raise RuntimeError('Incomplete history or infeasible best solution')
                            final = observed.history[-1]
                            record = dict(dataset=path.name, users=len(coords), case=case['case'], seed=seed,
                                fitness=final['fitness'], coverage=final['coverage'], energy=final['energy'],
                                interference=final['interference'], fe=final['fe'], wall_s=final['elapsed_s'],
                                optimizer_fitness=float(result.best_objective), feasible=True)
                            atomic_json(destination, dict(result=record, history=observed.history))
                        completed += 1
                        if completed % 25 == 0:
                            print(f'{completed}/{expected} tasks (including resumed tasks)', flush=True)
        results, _ = read_results(output)
        if len(results) != expected or results.duplicated(['dataset', 'case', 'seed']).any():
            raise RuntimeError('Result count mismatch or duplicate tasks')
        results.to_csv(output / 'runs.csv', index=False)
        atomic_json(output / 'completion.json', dict(complete=True, expected=expected, actual=len(results)))
        return output
    finally:
        lock.unlink(missing_ok=True)


def build_tables(output):
    """Descriptive tables only; no optimizer calls and no fabricated conclusions."""
    df, history = read_results(output)
    if df.empty:
        raise ValueError('No real results found')
    keys = ['dataset', 'case', 'seed']
    if df.duplicated(keys).any():
        raise ValueError('Duplicate tasks')
    # Do not rank incomplete paired experiments.
    manifest = json.loads((output / 'manifest.json').read_text(encoding='utf-8'))
    expected_keys = set(itertools.product(manifest['datasets'],
        [c['case'] for c in manifest['cases']], manifest['config']['seeds']))
    if set(df[keys].itertuples(index=False, name=None)) != expected_keys:
        raise ValueError('Study incomplete: tables/ranking require all paired tasks')
    summary = df.groupby('case').agg(fitness_mean=('fitness', 'mean'),
        fitness_best=('fitness', 'max'), coverage=('coverage', 'mean'), energy=('energy', 'mean'),
        interference=('interference', 'mean'), wall_s=('wall_s', 'mean'), fe=('fe', 'mean'))
    # Across-seed SD is computed within each dataset, then averaged across datasets.
    stability = df.groupby(['dataset', 'case']).fitness.std().groupby('case').mean()
    summary['seed_sd_mean'] = stability
    tables = {name: summary.reindex(names).reset_index() for name, names in GROUPS.items()}
    tables['by_scale'] = df.groupby(['users', 'case']).agg(fitness_mean=('fitness', 'mean'),
        coverage=('coverage', 'mean'), energy=('energy', 'mean'), interference=('interference', 'mean'),
        wall_s=('wall_s', 'mean'), fe=('fe', 'mean')).reset_index()
    # Read one task at a time: never materialize millions of position dictionaries.
    trajectories, checkpoints = {}, {}
    fields = ['fitness', 'coverage', 'energy', 'interference', 'fe', 'elapsed_s']
    for path in sorted((output / 'tasks').glob('*.json')):
        artifact = json.loads(path.read_text(encoding='utf-8'))
        name = artifact['result']['case']
        rows = artifact['history']
        if [r['iteration'] for r in rows] != list(range(101)):
            raise ValueError('Incomplete task history')
        trajectories.setdefault(name, []).append(np.array([r['fitness'] for r in rows]))
        for iteration in (0, 35, 80, 100):
            key = (name, iteration)
            total, count = checkpoints.get(key, (np.zeros(len(fields)), 0))
            checkpoints[key] = (total + np.array([rows[iteration][f] for f in fields]), count + 1)
    tables['checkpoints'] = pd.DataFrame([
        dict(case=name, iteration=iteration, **dict(zip(fields, total / count)))
        for (name, iteration), (total, count) in sorted(checkpoints.items())])
    convergence = []
    for name, values in trajectories.items():
        q25, median, q75 = np.quantile(np.stack(values), [.25, .5, .75], axis=0)
        convergence.extend(dict(case=name, iteration=i, median=median[i], q25=q25[i], q75=q75[i])
            for i in range(101))
    tables['convergence'] = pd.DataFrame(convergence)
    tables['stability'] = df.groupby(['dataset', 'case']).fitness.agg(
        mean='mean', sd='std', minimum='min', maximum='max', seeds='size').reset_index()
    paired = df.pivot(index=['dataset', 'seed'], columns='case', values='fitness')
    contrasts = []
    registry = cases()
    for family in ('WOA', 'PSO', 'GA'):
        group = [c for c in registry if c['family'] == family]
        for component in 'KOL':
            for off in [c for c in group if not c[component]]:
                on = next(c for c in group if c[component] and all(
                    c[key] == off[key] for key in 'KOL' if key != component))
                difference = paired[on['case']] - paired[off['case']]
                contrasts.append(dict(family=family, component=component, off=off['case'], on=on['case'],
                    paired_mean_difference=difference.mean(), paired_median_difference=difference.median(),
                    win_fraction=(difference > 0).mean(), tie_fraction=(difference == 0).mean()))
    tables['contributions'] = pd.DataFrame(contrasts)
    instance_medians = df.groupby(['dataset', 'case']).fitness.median().unstack('case')
    ranks = instance_medians.rank(axis=1, ascending=False, method='average').mean().rename('mean_rank')
    tables['ranking'] = summary.join(ranks).sort_values('mean_rank').reset_index()
    folder = output / 'tables'
    folder.mkdir(exist_ok=True)
    for name, table in tables.items():
        table.to_csv(folder / f'{name}.csv', index=False)
        (folder / f'{name}.md').write_text(table.to_markdown(index=False), encoding='utf-8')
    return tables
