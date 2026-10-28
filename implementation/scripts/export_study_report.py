"""Export saved study artifacts without running optimizers or changing checkpoints."""
import os
os.environ['MPLBACKEND'] = 'Agg'

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'implementation'))
from src.notebook_study import build_tables, export_dataset_csv, read_results, atomic_json
from src.study_report import build_report


def export_report(root, output):
    output = output.resolve()
    if not output.is_relative_to((root / 'implementation/results').resolve()):
        raise ValueError('Output must stay inside implementation/results')
    if any(output.rglob('.running')) or (output / '.coordinator').exists():
        raise RuntimeError('Study is locked; wait for the optimizer to finish')
    manifest = json.loads((output / 'manifest.json').read_text(encoding='utf-8'))
    print('Validating saved artifacts and complete paired task set...', flush=True)
    # Uses the original manifest, not current optimizer code/config signatures.
    # build_tables rejects missing/duplicate tasks and validates saved histories.
    tables = build_tables(output)
    runs, _ = read_results(output)
    runs.to_csv(output / 'runs.csv', index=False)
    print('Exporting dataset CSVs...', flush=True)
    export_dataset_csv(output)
    print('Rendering figures and report notebook...', flush=True)
    build_report(root, output, tables)
    atomic_json(output / 'report_completion.json', dict(complete=True,
        actual=len(runs), source_signature=manifest['signature']))
    print('REPORT COMPLETE', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=ROOT / 'implementation/results/study_80_iterations')
    args = parser.parse_args()
    export_report(ROOT, args.output)


if __name__ == '__main__':
    main()
