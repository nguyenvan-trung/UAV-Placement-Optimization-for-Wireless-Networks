"""Generate disjoint data/algo seed streams without global RNG mutation."""
import argparse
import csv
from pathlib import Path
import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]


def generate(config):
    rows = []
    used = set()
    sequence = np.random.SeedSequence(config['seeds']['root_seed'])
    def seed():
        while True:
            value = int(sequence.spawn(1)[0].generate_state(1)[0])
            if value not in used:
                used.add(value)
                return value
    s = config['scenarios']
    for purpose, runs in [('tuning', s['tuning_runs']), ('eval', s['eval_runs'])]:
        for count in s['ue_counts']:
            for distribution in s['distributions']:
                for instance in range(s['instances_per_scenario']):
                    data_seed = seed()
                    for run in range(runs):
                        rows.append(dict(scenario_id=f'{count}_{distribution}',ue_count=count,
                            distribution=distribution,instance_k=instance,data_seed=data_seed,
                            run_id=run,algo_seed=seed(),purpose=purpose))
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',type=Path,default=ROOT/'configs/benchmark.yaml')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--force',action='store_true')
    args = parser.parse_args()
    config = yaml.safe_load(args.config.read_text(encoding='utf-8'))
    destination = args.output or ROOT/config['seeds']['manifest']
    if destination.exists() and not args.force:
        raise SystemExit('Seed manifest exists; use --force only before preregistered experiments')
    rows = generate(config)
    destination.parent.mkdir(parents=True,exist_ok=True)
    with destination.open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print(f'{len(rows)} seed rows -> {destination}')
