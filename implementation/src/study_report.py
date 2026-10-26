"""Export real completed study tables, plots and a notebook report; no optimization."""
import base64
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import nbformat
from .notebook_study import GROUPS, read_results, read_task, task_paths, task_filename
from .input.data_loader import load_users
from .preprocessing.preprocessor import preprocess_users


def build_figures(root, output, tables):
    folder = output / 'figures'
    folder.mkdir(exist_ok=True)
    images = []
    for group, names in GROUPS.items():
        fig, ax = plt.subplots(figsize=(11, 6))
        for name in names:
            g = tables['convergence'].query('case == @name')
            ax.plot(g.iteration, g['median'], label=name)
            ax.fill_between(g.iteration, g.q25, g.q75, alpha=.10)
        ax.set(xlabel='Iteration', ylabel='Best evaluated fitness', title=group+' | median and IQR')
        ax.grid(alpha=.25)
        ax.legend(fontsize=8)
        fig.tight_layout()
        path = folder / f'convergence_{group}.png'
        fig.savefig(path, dpi=180)
        plt.close(fig)
        images.append(path)
        labels = {'fitness_mean': 'Fitness (maximize)', 'coverage': 'Coverage ratio',
            'energy': 'Normalized power proxy', 'interference': 'Overlap ratio',
            'wall_s': 'Observed time (s)', 'fe': 'Fitness evaluations'}
        fig, axes = plt.subplots(2, 3, figsize=(16, 9))
        for ax, (metric, label) in zip(axes.flat, labels.items()):
            for name in names:
                g = tables['by_scale'].query('case == @name').sort_values('users')
                ax.plot(g.users, g[metric], marker='o', label=name)
            ax.set(xlabel='Users', ylabel=label)
            ax.grid(alpha=.25)
        axes.flat[0].legend(fontsize=7)
        fig.suptitle(group)
        fig.tight_layout()
        path = folder / f'scale_{group}.png'
        fig.savefig(path, dpi=180)
        plt.close(fig)
        images.append(path)
    runs, _ = read_results(output)
    candidates = runs.query("case == 'I-WOA'")
    preferred = candidates.query('users == 200')
    sample = (preferred if not preferred.empty else candidates).sort_values(['dataset', 'seed']).iloc[0]
    filename = task_filename(sample.dataset, sample['case'], sample.seed)
    path = next(p for p in task_paths(output) if p.name == filename)
    position = np.asarray(read_task(path)['history'][-1]['position']).reshape(-1, 3)
    users = preprocess_users(load_users(root / 'data/stores' / sample.dataset))
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(users.x_m, users.y_m, users.z_m, s=8, label='UE')
    ax.scatter(*position.T, marker='^', s=100, label='UAV')
    ax.set(xlabel='X (m)', ylabel='Y (m)', zlabel='Z (m)', title=f'{sample.dataset} | I-WOA | seed {sample.seed}')
    ax.legend()
    fig.tight_layout()
    path = folder / 'placement_3d.png'
    fig.savefig(path, dpi=180)
    plt.close(fig)
    images.append(path)
    return images


def build_report(root, output, tables):
    images = build_figures(root, output, tables)
    runs, _ = read_results(output)
    manifest = json.loads((output / 'manifest.json').read_text(encoding='utf-8'))
    text = f"# Study results: {len(manifest['datasets'])} CSV, {len(manifest['cases'])} cases, {manifest['config']['iterations']} iterations\n\n"
    text += f"Seeds: {len(manifest['config']['seeds'])}; completed tasks: {len(runs)}.\n\n"
    text += 'Descriptive results only. Equal iterations do not imply equal FE. IQR is not a confidence interval.\n\n'
    text += '## Main comparison\n\n'+tables['main'].to_markdown(index=False)+'\n\n'
    text += '## Overall descriptive ranking\n\n'+tables['ranking'].to_markdown(index=False)+'\n\n'
    text += 'Best fitness is best evaluated; seed SD is computed within dataset before averaging.\n'
    (output / 'RESULTS.md').write_text(text, encoding='utf-8')
    nb = nbformat.v4.new_notebook()
    nb.cells.append(nbformat.v4.new_markdown_cell(text+
        '\nThis notebook is a report snapshot generated from saved artifacts. Outputs below were not produced by rerunning optimizers.'))
    for name, table in tables.items():
        nb.cells.append(nbformat.v4.new_markdown_cell('## '+name))
        cell = nbformat.v4.new_code_cell(f"# Read the saved table; no optimization\nimport pandas as pd\npd.read_csv(r'{output / 'tables' / (name+'.csv')}').head(100)")
        cell.outputs = [nbformat.v4.new_output('display_data', data={'text/html': table.head(100).to_html(index=False),
            'text/plain': table.head(100).to_string(index=False)})]
        nb.cells.append(cell)
    for path in images:
        nb.cells.append(nbformat.v4.new_markdown_cell('## '+path.stem))
        cell = nbformat.v4.new_code_cell(f"from IPython.display import Image, display\ndisplay(Image(filename=r'{path}'))")
        cell.outputs = [nbformat.v4.new_output('display_data', data={'image/png': base64.b64encode(path.read_bytes()).decode()})]
        nb.cells.append(cell)
    nbformat.write(nb, output / 'study_results.ipynb')
