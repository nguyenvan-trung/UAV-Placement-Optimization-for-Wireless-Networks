"""Run the approved CSV study with independent Windows-safe subprocess workers."""
import os
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
os.environ['MPLBACKEND'] = 'Agg'
os.environ['PYTHONUNBUFFERED'] = '1'

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'implementation'))
from src.notebook_study import (plan, run_study, study_signature, atomic_json,
    read_results)


def read_worker_progress(path, previous):
    """Progress is advisory: a transient Windows read lock must not kill workers."""
    for attempt in range(5):
        try:
            row = json.loads(path.read_text(encoding='utf-8'))
            if (type(row['completed']) is not int or type(row['resumed']) is not int
                    or not 0 <= row['resumed'] <= row['completed']):
                raise ValueError(f'Invalid worker progress: {path}')
            return row
        except (PermissionError, FileNotFoundError, json.JSONDecodeError) as error:
            if attempt == 4:
                print(f'Progress temporarily unavailable: {path.name} ({path.parent.name}); '
                      f'keeping previous snapshot ({type(error).__name__})', flush=True)
                return previous
            time.sleep(0.05 * (attempt + 1))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=Path, default=ROOT / 'configs/notebook_study.json')
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--worker-index', type=int)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding='utf-8'))
    if args.worker_index is not None:
        index = args.worker_index
        config['output'] = str(Path(config['output']) / 'shards' / f'worker_{index:02d}')
        run_study(ROOT, config, confirmed=True, shard_index=index, shard_count=args.workers)
        return
    files, variants, expected = plan(ROOT, config)
    if len(config['seeds']) < 2 or not 1 <= args.workers <= len(files):
        raise ValueError('Choose evaluation seeds and a valid worker count')
    output = (ROOT / config['output']).resolve()
    if not output.is_relative_to((ROOT / 'implementation/results').resolve()):
        raise ValueError('Output must stay inside implementation/results')
    output.mkdir(parents=True, exist_ok=True)
    lock = output / '.coordinator'
    with lock.open('x') as stream:
        stream.write(str(os.getpid()))
    children, handles = [], []
    started = time.perf_counter()
    try:
        signature = study_signature(ROOT, config, files)
        manifest_path = output / 'manifest.json'
        if manifest_path.exists():
            previous = json.loads(manifest_path.read_text(encoding='utf-8'))
            if previous['signature'] != signature or previous['workers'] != args.workers:
                raise ValueError('Source/config/data/worker count changed; choose new output')
        elif any(p.name != '.coordinator' for p in output.iterdir()):
            raise ValueError('Nonempty output has no manifest')
        atomic_json(manifest_path, dict(signature=signature, config=config, expected_tasks=expected,
            datasets=[p.name for p in files], cases=variants, workers=args.workers,
            artifact_format='gzip JSON, level 3; lossless', pid=os.getpid()))
        print(f'Starting {expected} tasks: {len(files)} CSV x {len(variants)} cases x {len(config["seeds"])} seeds', flush=True)
        logs = output / 'logs'
        logs.mkdir(exist_ok=True)
        for index in range(args.workers):
            handle = (logs / f'worker_{index:02d}.log').open('a', encoding='utf-8')
            handles.append(handle)
            child = subprocess.Popen([sys.executable, '-B', str(Path(__file__).resolve()),
                '--config', str(args.config.resolve()), '--workers', str(args.workers),
                '--worker-index', str(index)], cwd=ROOT, stdout=handle, stderr=subprocess.STDOUT,
                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            children.append(child)
        snapshots = {index: dict(completed=0, resumed=0) for index in range(args.workers)}
        while True:
            complete = resumed = 0
            for index in range(args.workers):
                progress = output / 'shards' / f'worker_{index:02d}' / 'progress.json'
                if progress.exists():
                    snapshots[index] = read_worker_progress(progress, snapshots[index])
                complete += snapshots[index]['completed']
                resumed += snapshots[index]['resumed']
            elapsed = time.perf_counter() - started
            fresh = complete-resumed
            eta = (expected-complete)*elapsed/fresh if fresh else None
            atomic_json(output / 'progress.json', dict(completed=complete, expected=expected,
                elapsed_s=elapsed, eta_s=eta, resumed=resumed, phase='optimizing',
                coordinator_pid=os.getpid(), worker_pids=[p.pid for p in children]))
            print(f'{complete}/{expected} tasks | elapsed {elapsed/3600:.2f} h | ETA {eta/3600 if eta else 0:.2f} h', flush=True)
            states = [p.poll() for p in children]
            if any(code is not None and code != 0 for code in states):
                raise RuntimeError(f'A worker failed: {states}; inspect logs')
            if all(code == 0 for code in states):
                break
            time.sleep(20)
        print('All workers finished; validating saved results...', flush=True)
        atomic_json(output / 'progress.json', dict(completed=expected, expected=expected, phase='validating',
            elapsed_s=time.perf_counter()-started, coordinator_pid=os.getpid()))
        results, _ = read_results(output)
        if len(results) != expected:
            raise RuntimeError('Completed task count differs from design')
        results.to_csv(output / 'runs.csv', index=False)
        atomic_json(output / 'completion.json', dict(complete=True, expected=expected, actual=len(results),
            elapsed_s=time.perf_counter()-started))
        atomic_json(output / 'progress.json', dict(completed=expected, expected=expected, phase='complete',
            elapsed_s=time.perf_counter()-started))
        print('OPTIMIZATION COMPLETE: results saved. Run export_study_report.py separately.', flush=True)
    except BaseException as error:
        for child in children:
            if child.poll() is None:
                child.terminate()
        for child in children:
            child.wait()
        status_path = output / 'progress.json'
        try:
            status = json.loads(status_path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            status = {}
        status.update(phase='failed', error=str(error), elapsed_s=time.perf_counter()-started)
        atomic_json(status_path, status)
        raise
    finally:
        for handle in handles:
            handle.close()
        lock.unlink(missing_ok=True)


if __name__ == '__main__':
    main()
