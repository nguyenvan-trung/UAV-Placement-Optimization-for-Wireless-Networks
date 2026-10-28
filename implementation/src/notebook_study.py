"""Explicitly invoked configurable-iteration study on existing CSVs; no work at import."""
import hashlib
import itertools
import json
import os
import time
import platform
import importlib.metadata
import gzip
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
    """Eight WOA combinations and four unchanged comparison algorithms."""
    rows = []
    for k, o, l in itertools.product((False, True), repeat=3):
        suffix = ''.join(letter for letter, flag in zip('KOL', (k, o, l)) if flag)
        name = 'I-WOA' if suffix == 'KOL' else ('WOA' if not suffix else 'WOA-' + suffix)
        rows.append(dict(case=name, family='WOA', K=k, O=o, L=l))
    rows.extend(dict(case=name, family=name, K=False, O=False, L=False)
                for name in ('GA', 'PSO', 'H-PSO-GA', 'H-WOA-PSO'))
    return rows


MAIN = ['GA', 'PSO', 'WOA', 'H-PSO-GA', 'H-WOA-PSO', 'I-WOA']
GROUPS = {'main': MAIN, 'WOA': [c['case'] for c in cases() if c['family'] == 'WOA']}


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
            use_crossover=case.get('crossover', True), use_mutation=case.get('mutation', True)), seed=seed)
    return HybridWOAPSOOptimizer(HWOAPSOParameters(population_size=population, iterations=iterations,
        use_personal_attraction=case.get('personal', True), use_global_attraction=case.get('global_attraction', True)), seed=seed)


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
    if len(files) != config.get('expected_datasets', 200):
        raise ValueError(f"Expected {config.get('expected_datasets', 200)} input CSVs, found {len(files)}")
    if config['iterations'] not in (80, 100) or config['population'] < 3 or config['num_uavs'] < 1:
        raise ValueError('Study requires 80 or 100 iterations, population >= 3 and positive UAV count')
    seeds = config['seeds']
    if len(seeds) != len(set(seeds)) or any(type(s) is not int or not 0 <= s < 2**32 for s in seeds):
        raise ValueError('Seeds must be distinct integers in [0, 2**32)')
    return files, cases(), len(files) * len(cases()) * len(seeds)


def atomic_json(path, value):
    temp = path.with_suffix('.tmp')
    payload = json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(',', ':')).encode('utf-8')
    if path.suffix == '.gz':
        temp.write_bytes(gzip.compress(payload, compresslevel=3, mtime=0))
    else:
        temp.write_bytes(payload)
    # Windows readers/editors can briefly hold the destination without delete sharing.
    for attempt in range(20):
        try:
            temp.replace(path)
            break
        except PermissionError:
            if attempt == 19:
                raise
            time.sleep(min(0.05 * (attempt + 1), 0.5))


def task_paths(output):
    folders = [output / 'tasks', *sorted((output / 'shards').glob('worker_*/tasks'))]
    return [p for folder in folders for p in sorted(folder.rglob('*.json*'))
            if p.name.endswith(('.json', '.json.gz'))]


def read_task(path):
    payload = gzip.decompress(path.read_bytes()) if path.suffix == '.gz' else path.read_bytes()
    return json.loads(payload.decode('utf-8'))


def dataset_result_stem(dataset):
    return Path(dataset).stem.removesuffix('_users_connect')


def task_filename(dataset, case, seed):
    return f'{dataset_result_stem(dataset)}_result_{case}_seed{seed}.json.gz'


def task_destination(output, dataset, case, seed):
    return output / 'tasks' / dataset_result_stem(dataset) / task_filename(dataset, case, seed)


def validate_task(artifact, *, dataset=None, case=None, seed=None, problem=None, iterations=None):
    """Reject corrupt/resumed artifacts before completion or aggregation."""
    record, history = artifact['result'], artifact['history']
    for key, expected in [('dataset', dataset), ('case', case), ('seed', seed)]:
        if expected is not None and record[key] != expected:
            raise ValueError(f'Task identity mismatch: {key}')
    if record['feasible'] is not True:
        raise ValueError('Task has no feasible result')
    iterations = len(history) - 1 if iterations is None else iterations
    if iterations not in (80, 100) or [r['iteration'] for r in history] != list(range(iterations + 1)):
        raise ValueError('Task must contain all iterations from 0 to the configured final iteration')
    numeric = np.array([[r[k] for k in ('fitness', 'coverage', 'energy', 'interference', 'fe', 'elapsed_s')]
                        for r in history], dtype=float)
    if not np.isfinite(numeric).all():
        raise ValueError('Nonfinite history metrics')
    if (numeric[:, 1:4] < 0).any() or (numeric[:, 1:4] > 1).any():
        raise ValueError('Quality metrics outside [0,1]')
    if (np.diff(numeric[:, 0]) < -1e-12).any():
        raise ValueError('Best fitness decreased')
    if (numeric[:, 4] <= 0).any() or (numeric[:, 4] != np.floor(numeric[:, 4])).any() or (np.diff(numeric[:, 4]) < 0).any():
        raise ValueError('Invalid FE history')
    if (numeric[:, 5] < 0).any() or (np.diff(numeric[:, 5]) < 0).any():
        raise ValueError('Invalid timing history')
    positions = np.asarray([r['position'] for r in history], dtype=float)
    if positions.ndim != 2 or positions.shape[1] < 3 or positions.shape[1] % 3 or not np.isfinite(positions).all():
        raise ValueError('Invalid position history')
    final = history[-1]
    for field, history_field in [('fitness', 'fitness'), ('coverage', 'coverage'), ('energy', 'energy'),
                                 ('interference', 'interference'), ('fe', 'fe'), ('wall_s', 'elapsed_s')]:
        if not np.isclose(record[field], final[history_field], rtol=0, atol=1e-10):
            raise ValueError(f'Result/history mismatch: {field}')
    if not np.isfinite(record['optimizer_fitness']) or record['optimizer_fitness'] > record['fitness'] + 1e-10:
        raise ValueError('Invalid optimizer result')
    if problem is not None:
        if positions.shape[1] != problem.dimension or not all(problem.is_feasible(x) for x in positions):
            raise ValueError('Infeasible history position')
        metrics = problem.evaluate_detailed(positions[-1])
        expected = [metrics.fitness, metrics.coverage_rate, metrics.energy_normalized, metrics.interference_rate]
        if not np.allclose(numeric[-1, :4], expected, rtol=0, atol=1e-10):
            raise ValueError('Final solution does not reproduce reported metrics')
    return record


def study_signature(root, config, files):
    h = hashlib.sha256(json.dumps(config, sort_keys=True).encode())
    for path in sorted((root / 'implementation/src').rglob('*.py')) + files:
        h.update(str(path.relative_to(root)).encode())
        h.update(path.read_bytes())
    return h.hexdigest()


def read_results(output, *, include_history=False):
    records, histories = [], []
    for path in task_paths(output):
        artifact = read_task(path)
        records.append(validate_task(artifact))
        if include_history:
            histories.extend(dict(dataset=artifact['result']['dataset'], case=artifact['result']['case'],
                seed=artifact['result']['seed'], **row) for row in artifact['history'])
    return pd.DataFrame(records), pd.DataFrame(histories)


def export_dataset_csv(output, *, dataset=None, destination=None):
    """Export Excel-readable CSVs, loading only one dataset's history at a time."""
    grouped = {}
    paths = (sorted((output / 'tasks' / dataset_result_stem(dataset)).glob('*.json*'))
             if dataset is not None else task_paths(output))
    for path in paths:
        record = read_task(path)['result']
        grouped.setdefault(record['dataset'], []).append(path)
    for dataset, paths in sorted(grouped.items()):
        records, positions, convergence = [], [], []
        for path in paths:
            artifact = read_task(path)
            record = validate_task(artifact, dataset=dataset)
            records.append(record)
            identity = dict(dataset=dataset, case=record['case'], seed=record['seed'])
            final_positions = np.asarray(artifact['history'][-1]['position']).reshape(-1, 3)
            for index, (x, y, z) in enumerate(final_positions, start=1):
                positions.append(dict(**identity, uav_id=index, x_m=x, y_m=y, z_m=z))
            for row in artifact['history']:
                convergence.append(dict(**identity, **{k: v for k, v in row.items() if k != 'position'}))
        results = pd.DataFrame(records)
        if results.duplicated(['dataset', 'case', 'seed']).any():
            raise ValueError('Duplicate tasks in CSV export')
        stem = dataset_result_stem(dataset)
        folder = (destination or output) / 'datasets' / stem
        folder.mkdir(parents=True, exist_ok=True)
        for suffix, frame, order in (
            ('result', results, ['case', 'seed']),
            ('positions', pd.DataFrame(positions), ['case', 'seed', 'uav_id']),
            ('convergence', pd.DataFrame(convergence), ['case', 'seed', 'iteration']),
        ):
            frame.sort_values(order).to_csv(folder / f'{stem}_{suffix}.csv',
                index=False, encoding='utf-8-sig')


def run_study(root, config, *, confirmed=False, shard_index=0, shard_count=1):
    if not confirmed:
        raise RuntimeError('Run disabled: explicit confirmation is required')
    files, variants, expected = plan(root, config)
    if not 0 <= shard_index < shard_count <= len(files):
        raise ValueError('Invalid dataset shard')
    files = files[shard_index::shard_count]
    expected = len(files) * len(variants) * len(config['seeds'])
    if len(config['seeds']) < 2:
        raise ValueError('Choose at least two evaluation seeds before running; seed count is not finalized')
    output = (root / config['output']).resolve()
    if not output.is_relative_to((root / 'implementation/results').resolve()):
        raise ValueError('Output must be inside implementation/results')
    output.mkdir(parents=True, exist_ok=True)
    if (output / '.coordinator').exists():
        raise RuntimeError('A coordinator is running for this output; do not start a second runner')
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
        versions = {name: importlib.metadata.version(name) for name in
                    ['numpy', 'pandas', 'scipy', 'scikit-learn', 'matplotlib', 'threadpoolctl']}
        environment = dict(python=platform.python_version(), platform=platform.platform(), versions=versions)
        env_path = output / 'env.json'
        if env_path.exists() and json.loads(env_path.read_text(encoding='utf-8')) != environment:
            raise ValueError('Environment changed; use a new output directory')
        atomic_json(env_path, environment)
        tasks = output / 'tasks'
        tasks.mkdir(exist_ok=True)
        completed = 0
        resumed = 0
        started = time.perf_counter()
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
                        destination = task_destination(output, path.name, case['case'], seed)
                        destination.parent.mkdir(exist_ok=True)
                        if destination.exists():
                            validate_task(read_task(destination),
                                dataset=path.name, case=case['case'], seed=seed, problem=original, iterations=config['iterations'])
                            resumed += 1
                        else:
                            observed = ObservedProblem(original, initial)
                            optimizer = make_case(case, config['population'], config['iterations'], seed)
                            result = optimizer.optimize(observed)
                            if len(observed.history) != config['iterations'] + 1 or not original.is_feasible(observed.position):
                                raise RuntimeError('Incomplete history or infeasible best solution')
                            final = observed.history[-1]
                            record = dict(dataset=path.name, users=len(coords), case=case['case'], seed=seed,
                                fitness=final['fitness'], coverage=final['coverage'], energy=final['energy'],
                                interference=final['interference'], fe=final['fe'], wall_s=final['elapsed_s'],
                                optimizer_fitness=float(result.best_objective), feasible=True)
                            artifact = dict(result=record, history=observed.history)
                            validate_task(artifact, dataset=path.name, case=case['case'], seed=seed, problem=original, iterations=config['iterations'])
                            atomic_json(destination, artifact)
                        completed += 1
                        atomic_json(output / 'progress.json', dict(completed=completed, expected=expected,
                            resumed=resumed, elapsed_s=time.perf_counter()-started,
                            dataset=path.name, case=case['case'], seed=seed, pid=os.getpid()))
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
    iterations = manifest['config']['iterations']
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
    tables['design'] = pd.DataFrame(cases())
    tables['by_dataset'] = df.groupby(['dataset', 'users', 'case']).agg(
        fitness_mean=('fitness', 'mean'), fitness_sd=('fitness', 'std'),
        coverage_mean=('coverage', 'mean'), energy_mean=('energy', 'mean'),
        interference_mean=('interference', 'mean'), wall_s_mean=('wall_s', 'mean'),
        fe_mean=('fe', 'mean'), seeds=('seed', 'size')).reset_index()
    tables['by_scale'] = df.groupby(['users', 'case']).agg(fitness_mean=('fitness', 'mean'),
        coverage=('coverage', 'mean'), energy=('energy', 'mean'), interference=('interference', 'mean'),
        wall_s=('wall_s', 'mean'), fe=('fe', 'mean')).reset_index()
    # Read one task at a time: never materialize millions of position dictionaries.
    trajectories, checkpoints, stages = {}, {}, {}
    milestones = sorted({0, iterations // 4, iterations // 2, 3 * iterations // 4, iterations})
    fields = ['fitness', 'coverage', 'energy', 'interference', 'fe', 'elapsed_s']
    for path in task_paths(output):
        artifact = read_task(path)
        name = artifact['result']['case']
        rows = artifact['history']
        if [r['iteration'] for r in rows] != list(range(iterations + 1)):
            raise ValueError('Incomplete task history')
        trajectories.setdefault(name, []).append(np.array([r['fitness'] for r in rows]))
        for iteration in milestones:
            key = (name, iteration)
            total, count = checkpoints.get(key, (np.zeros(len(fields)), 0))
            checkpoints[key] = (total + np.array([rows[iteration][f] for f in fields]), count + 1)
        for start, end in zip(milestones, milestones[1:]):
            before, after = rows[start], rows[end]
            key = (artifact['result']['users'], name, start, end)
            delta = np.array([after['elapsed_s'] - before['elapsed_s'],
                after['fitness'] - before['fitness'], after['fe'] - before['fe'],
                after['fitness'], after['coverage'], after['energy'], after['interference']])
            total, count = stages.get(key, (np.zeros(7), 0))
            stages[key] = (total + delta, count + 1)
    tables['checkpoints'] = pd.DataFrame([
        dict(case=name, iteration=iteration, **dict(zip(fields, total / count)))
        for (name, iteration), (total, count) in sorted(checkpoints.items())])
    convergence = []
    for name, values in trajectories.items():
        q25, median, q75 = np.quantile(np.stack(values), [.25, .5, .75], axis=0)
        convergence.extend(dict(case=name, iteration=i, median=median[i], q25=q25[i], q75=q75[i])
            for i in range(iterations + 1))
    tables['convergence'] = pd.DataFrame(convergence)
    stage_fields = ['stage_time_s', 'fitness_gain', 'stage_fe', 'fitness_end',
                    'coverage_end', 'energy_end', 'interference_end']
    tables['stages_by_scale'] = pd.DataFrame([
        dict(users=users, case=name, start_iteration=start, end_iteration=end,
             runs=count, **dict(zip(stage_fields, total / count)))
        for (users, name, start, end), (total, count) in sorted(stages.items())])
    tables['stages'] = tables['stages_by_scale'].groupby(
        ['case', 'start_iteration', 'end_iteration'])[stage_fields].mean().reset_index()
    tables['quality_by_scale'] = df.groupby(['users', 'case']).agg(
        fitness_mean=('fitness', 'mean'), fitness_median=('fitness', 'median'),
        fitness_sd=('fitness', 'std'), coverage_mean=('coverage', 'mean'),
        coverage_sd=('coverage', 'std'), time_mean_s=('wall_s', 'mean'),
        time_median_s=('wall_s', 'median'), time_sd_s=('wall_s', 'std'),
        fe_mean=('fe', 'mean')).reset_index()
    tables['stability'] = df.groupby(['dataset', 'case']).fitness.agg(
        mean='mean', sd='std', minimum='min', maximum='max', seeds='size').reset_index()
    paired = df.pivot(index=['dataset', 'seed'], columns='case', values='fitness')
    contrasts = []
    registry = cases()
    for family in ('WOA',):
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
    tables['stability_summary'] = tables['stability'].groupby('case').agg(
        seed_sd_mean=('sd', 'mean'), seed_sd_max=('sd', 'max')).reset_index()
    hybrid_pairs = [('H-PSO-GA', 'PSO'), ('H-PSO-GA', 'GA'),
                    ('H-WOA-PSO', 'WOA'), ('H-WOA-PSO', 'PSO'), ('I-WOA', 'WOA')]
    comparisons = []
    times = df.pivot(index=['dataset', 'seed'], columns='case', values='wall_s')
    for candidate, baseline in hybrid_pairs:
        difference = paired[candidate] - paired[baseline]
        comparisons.append(dict(candidate=candidate, baseline=baseline,
            fitness_gain_mean=difference.mean(), fitness_gain_median=difference.median(),
            win_fraction=(difference > 1e-12).mean(),
            tie_fraction=(difference.abs() <= 1e-12).mean(),
            time_difference_s=(times[candidate] - times[baseline]).mean()))
    tables['paired_comparison'] = pd.DataFrame(comparisons)
    folder = output / 'tables'
    folder.mkdir(exist_ok=True)
    for name, table in tables.items():
        table.to_csv(folder / f'{name}.csv', index=False)
        (folder / f'{name}.md').write_text(table.to_markdown(index=False), encoding='utf-8')
    return tables
