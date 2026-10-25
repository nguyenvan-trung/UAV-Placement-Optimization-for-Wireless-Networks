"""FE benchmark with atomic per-task outputs and validated resume."""
import os
for _key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[_key]='1'
import argparse
import csv
import hashlib
import json
import platform
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'implementation'))
import numpy as np
import pandas as pd
import scipy
import sklearn
import yaml
from threadpoolctl import threadpool_limits
from src.benchmark import BenchmarkProblem,make_optimizer
from src.scenarios import ScenarioParameters,generate_scenario
from src.constants.network import CARRIER_FREQUENCY_HZ


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_json(path,value):
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(value,indent=2,allow_nan=False),encoding='utf-8')
    temporary.replace(path)


def atomic_csv(path,rows):
    temporary=path.with_suffix(path.suffix+'.tmp')
    pd.DataFrame(rows).to_csv(temporary,index=False)
    temporary.replace(path)


def signature(config_path,manifest,args):
    h=hashlib.sha256(config_path.read_bytes()+manifest.read_bytes())
    for folder in [ROOT/'implementation/src',ROOT/'implementation/scripts']:
        for p in sorted(folder.rglob('*.py')):
            h.update(str(p.relative_to(ROOT)).encode());h.update(p.read_bytes())
    h.update(json.dumps(dict(mode=args.mode,smoke=args.smoke,max_fe=args.max_fe,
                            purpose=args.purpose,workers=args.workers),sort_keys=True).encode())
    return h.hexdigest()


def git(*args):
    p=subprocess.run(['git',*args],cwd=ROOT,capture_output=True,text=True)
    return p.stdout.strip() if p.returncode==0 else 'unavailable'


def environment(config_path,manifest,run_signature,command):
    ram=None
    try:
        import ctypes
        if os.name=='nt':
            class Memory(ctypes.Structure):
                _fields_=[('length',ctypes.c_ulong),('load',ctypes.c_ulong)]+[(k,ctypes.c_ulonglong) for k in ['total','avail','page','avail_page','virtual','avail_virtual','extended']]
            value=Memory();value.length=ctypes.sizeof(value)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(value)):ram=value.total
        else:ram=os.sysconf('SC_PAGE_SIZE')*os.sysconf('SC_PHYS_PAGES')
    except (OSError,AttributeError):pass
    return dict(git_commit=git('rev-parse','HEAD'),dirty=bool(git('status','--porcelain')),
        config_sha256=sha(config_path),seeds_sha256=sha(manifest),run_signature=run_signature,
        python=sys.version,numpy=np.__version__,scipy=scipy.__version__,sklearn=sklearn.__version__,
        pandas=pd.__version__,pyyaml=yaml.__version__,cpu=platform.processor(),logical_cores=os.cpu_count(),
        ram_bytes=ram,os=platform.platform(),thread_environment={k:os.environ[k] for k in
        ['OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS']},command=command,
        timing_scope='worker wall/process CPU includes scenario generation, initialization and final metrics; excludes process startup; batch wall includes dispatch/checkpoint but excludes metadata capture')


def task_work(task):
    seedrow,name,experiment,config,budget,mode,output=task
    started=time.perf_counter();cpu_start=time.process_time()
    with threadpool_limits(limits=1):
        p=config['problem']
        parameters=ScenarioParameters(width=p['area_width'],height=p['area_height'],**config['scenarios']['parameters'])
        data=generate_scenario(seedrow['distribution'],int(seedrow['ue_count']),int(seedrow['data_seed']),parameters)
        users=data[['x_m','y_m','z_m']].to_numpy()
        problem=BenchmarkProblem(users,config,experiment)
        size=config['common']['population_size']
        # Dedicated stream: all algorithms/variants/configurations receive the same base positions.
        rng=np.random.default_rng(np.random.SeedSequence([int(seedrow['algo_seed']),1]))
        initial=rng.uniform(problem.search_space.lower_bounds,problem.search_space.upper_bounds,(size,problem.dimension))
        target=config['output']['target_fitness']
        optimizer=make_optimizer(name,config,int(seedrow['algo_seed']),ablation=mode=='ablation')
        result=optimizer.optimize(problem,max_fe=budget,initial_population=initial,target=target)
        position=problem.search_space.clip(result.best_position)
        feasible=problem.is_feasible(position)
        metrics=problem.raw_metrics(position) if feasible else dict(fitness=None,C=None,C_snr=None,C_sinr=None,E=None,I=None,ue_pass=None,ue_total=len(users))
        if feasible and not np.isclose(metrics['fitness'],result.best_objective,rtol=0,atol=1e-9):
            raise RuntimeError('Reported metrics do not match optimization Fitness')
        identity=dict(seedrow,algorithm=name,config_id=experiment['id'],max_fe=budget)
        task_id=hashlib.sha256(json.dumps(identity,sort_keys=True).encode()).hexdigest()[:24]
        destination=Path(output)
        atomic_csv(destination/'convergence'/f'{task_id}.csv',result.fe_history)
        atomic_json(destination/'solutions'/f'{task_id}.json',dict(identity=identity,
            uav_positions=position.reshape(-1,3).tolist(),initial_population=initial.tolist(),
            data_sha256=hashlib.sha256(users.tobytes()).hexdigest(),fe_phase_counts=result.fe_phase_counts,
            feasible=feasible,violation=0 if feasible else 'minimum_separation',metrics=metrics))
        return dict(identity,**metrics,task_id=task_id,feasible=feasible,violation=0 if feasible else 'minimum_separation',
            fe_used=result.fe_used,iterations_done=result.iterations_done,
            wall_time_s=time.perf_counter()-started,cpu_time_s=time.process_time()-cpu_start,
            worker_id=os.getpid(),hit_target=None if target is None else result.fe_to_target is not None,
            fe_to_target=result.fe_to_target,reoptimized=True,
            initial_population_sha256=hashlib.sha256(initial.tobytes()).hexdigest(),
            convergence_file=f'convergence/{task_id}.csv',solution_file=f'solutions/{task_id}.json')


def load_manifest(path,config):
    with path.open(encoding='utf-8-sig',newline='') as stream:rows=list(csv.DictReader(stream))
    required={'scenario_id','ue_count','distribution','instance_k','data_seed','run_id','algo_seed','purpose'}
    if not rows or set(rows[0])!=required:raise ValueError('Invalid seed manifest schema')
    for r in rows:
        for k in ['ue_count','instance_k','data_seed','run_id','algo_seed']:r[k]=int(r[k])
        if r['purpose'] not in ('tuning','eval'):raise ValueError('Unknown purpose')
    for purpose in ('tuning','eval'):
        values={r[k] for r in rows if r['purpose']==purpose for k in ('data_seed','algo_seed')}
        other={r[k] for r in rows if r['purpose']!=purpose for k in ('data_seed','algo_seed')}
        if values & other:raise ValueError('Tuning/evaluation seed overlap')
    expected=[]
    # Compare against the deterministic manifest design, catching omissions and changed IDs.
    from implementation.scripts.generate_seeds import generate
    expected=generate(config)
    if rows!=expected:raise ValueError('Seed manifest differs from the registered config; regenerate before running')
    return rows


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--config',type=Path,default=ROOT/'configs/benchmark.yaml')
    parser.add_argument('--seeds',type=Path)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--mode',choices=['benchmark','ablation','sensitivity'],default='benchmark')
    parser.add_argument('--purpose',choices=['eval','tuning'],default='eval')
    parser.add_argument('--workers',type=int)
    parser.add_argument('--max-fe',type=int)
    parser.add_argument('--smoke',action='store_true')
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--max-tasks',type=int,help='Intentional checkpoint test; continue with --resume')
    args=parser.parse_args()
    config=yaml.safe_load(args.config.read_text(encoding='utf-8'))
    weights=np.asarray([config['problem']['fitness']['weights'][k] for k in ('C','E','I')],dtype=float)
    if not np.isfinite(weights).all() or (weights<0).any() or not np.isclose(weights.sum(),1):
        raise ValueError('Fitness weights must be finite, nonnegative and sum to one')
    if config['problem']['carrier_frequency_hz']!=CARRIER_FREQUENCY_HZ or config['problem']['num_uav']!=4:
        raise ValueError('This baseline requires the implemented frequency and four UAVs')
    if config['budget']['stop_on']!='fe' or config['budget']['early_stop'] or config['parallel']['threads_per_worker']!=1:
        raise ValueError('Requires FE stop, no early stop, one thread per worker')
    if config['output']['convergence_interval']!=50:
        raise ValueError('Current FE logger uses interval 50')
    if not config['problem']['fitness']['maximize'] or config['problem']['fitness']['coverage_quantity']!='SNR':
        raise ValueError('Baseline must maximize SNR-based Fitness')
    manifest=args.seeds or ROOT/config['seeds']['manifest']
    rows=load_manifest(manifest,config)
    args.workers=args.workers or config['parallel']['n_workers']
    budget=args.max_fe or (60 if args.smoke else config['budget']['max_fe'])
    if args.workers<1 or budget<1:raise ValueError('Positive workers and budget required')
    if args.max_fe is None and config['budget']['max_fe']!=config['common']['population_size']*(1+config['budget']['reference_woa_iterations']):
        raise ValueError('Reference FE budget formula mismatch')
    rows=[r for r in rows if r['purpose']==args.purpose]
    if args.mode!='benchmark':rows=[r for r in rows if r['ue_count'] in (100,300,500)]
    if args.smoke:rows=rows[:1]
    experiments=[dict(id='main',weights=config['problem']['fitness']['weights'],coverage_quantity='SNR')]
    if args.mode=='sensitivity':
        auxiliary=ROOT/config['sensitivity']['configuration_file']
        experiments=yaml.safe_load(auxiliary.read_text(encoding='utf-8'))['sensitivity']['configurations']
    names=list(config['ablation']) if args.mode=='ablation' else list(config['algorithms'])
    output=args.output or ROOT/config['output']['directory']
    fingerprint=signature(args.config,manifest,args)
    if args.mode=='sensitivity':fingerprint=hashlib.sha256((fingerprint+sha(auxiliary)).encode()).hexdigest()
    existing=[];prior_wall=0.
    if output.exists() and any(output.iterdir()):
        if not args.resume:raise ValueError('Output exists: use a new directory or --resume')
        env=json.loads((output/'env.json').read_text())
        if env['run_signature']!=fingerprint:raise ValueError('Source/config/seed/worker signature changed; cannot resume')
        current_versions=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,
                              sklearn=sklearn.__version__,pandas=pd.__version__,pyyaml=yaml.__version__)
        if any(env.get(key)!=value for key,value in current_versions.items()):
            raise ValueError('Python/library versions changed; cannot resume this batch')
        if (output/'runs.csv').exists():
            previous=pd.read_csv(output/'runs.csv')
            existing=previous.where(pd.notna(previous),None).to_dict('records')
            prior_wall=max(float(r['batch_wall_time_s']) for r in existing)
            for r in existing:
                if not (output/r['solution_file']).exists() or not (output/r['convergence_file']).exists():
                    raise ValueError('Checkpoint references missing task artifacts')
    else:
        output.mkdir(parents=True,exist_ok=True)
        atomic_json(output/'env.json',environment(args.config,manifest,fingerprint,sys.argv))
        freeze=subprocess.run([sys.executable,'-m','pip','freeze'],capture_output=True,text=True,check=True)
        (output/'requirements.lock.txt').write_text(freeze.stdout,encoding='utf-8')
        (output/'benchmark.yaml').write_bytes(args.config.read_bytes())
        (output/'seeds.csv').write_bytes(manifest.read_bytes())
        if args.mode=='sensitivity':(output/'sensitivity.yaml').write_bytes(auxiliary.read_bytes())
    for name in ['convergence','solutions']:(output/name).mkdir(exist_ok=True)
    tasks=[]
    for r in rows:
        for experiment in experiments:
            for name in names:tasks.append((r,name,experiment,config,budget,args.mode,str(output)))
    def key(task):
        r,name,ex,*_=task
        return hashlib.sha256(json.dumps(dict(r,algorithm=name,config_id=ex['id'],max_fe=budget),sort_keys=True).encode()).hexdigest()[:24]
    done={r['task_id'] for r in existing}
    if len(done)!=len(existing) or not done<={key(t) for t in tasks}:raise ValueError('Invalid checkpoint task IDs')
    pending=[t for t in tasks if key(t) not in done]
    if args.max_tasks is not None:pending=pending[:args.max_tasks]
    started=time.perf_counter()
    def accept(row):
        existing.append(row)
        wall=prior_wall+time.perf_counter()-started
        cpu=sum(float(r['cpu_time_s']) for r in existing)
        for r in existing:r.update(batch_id=fingerprint[:16],batch_wall_time_s=wall,batch_total_cpu_s=cpu,n_workers=args.workers)
        atomic_csv(output/'runs.csv',sorted(existing,key=lambda r:r['task_id']))
        print(f'{len(existing)}/{len(tasks)} completed; FE={row["fe_used"]}; {row["algorithm"]}',flush=True)
    if args.workers==1:
        for task in pending:accept(task_work(task))
    else:
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            futures=[pool.submit(task_work,t) for t in pending]
            for future in as_completed(futures):accept(future.result())
    atomic_json(output/'completion.json',dict(complete=len(existing)==len(tasks),completed=len(existing),expected=len(tasks),
        run_signature=fingerprint,max_fe=budget,smoke=args.smoke,mode=args.mode))
    print(f'Output: {output}',flush=True)


if __name__=='__main__':main()
