"""Export real completed study tables, plots and a notebook report; no optimization."""
import base64
import json
import os
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import nbformat
from .notebook_study import GROUPS, read_results, read_task, task_paths, task_filename
from .input.data_loader import load_users
from .preprocessing.preprocessor import preprocess_users


def save_image(fig, folder, stem):
    path = folder / (stem + '.jpg')
    fig.tight_layout()
    fig.savefig(path, dpi=180, facecolor='white')
    plt.close(fig)
    return path


def build_table_images(output, tables):
    """Readable summary pages; detailed per-dataset/per-iteration data stays in CSV."""
    folder = output / 'picture'
    folder.mkdir(exist_ok=True)
    catalog = {
        'main': ('bangsosanhthuattoan', 'Main algorithm comparison'),
        'WOA': ('bangsosanhcaitienwoa', 'WOA component comparison'),
        'design': ('bangthietkethuattoan', 'Algorithm components'),
        'ranking': ('bangxephang', 'Descriptive ranking (lower mean rank is better)'),
        'quality_by_scale': ('bangchatluongvasonguoi', 'Quality and runtime by user count'),
        'checkpoints': ('bangthoigianvavongchay', 'Cumulative metrics at iteration milestones'),
        'stages': ('bangsosanhgiaidoan', 'Incremental runtime, FE and fitness gain by stage'),
        'stages_by_scale': ('banggiaidoanvasonguoi', 'Stage metrics by user count'),
        'stability_summary': ('bangdoondinh', 'Within-dataset seed stability'),
        'contributions': ('bangdonggopcaitien', 'Paired component contributions'),
        'paired_comparison': ('bangsosanhhybrid', 'Paired comparisons against parent algorithms'),
    }
    images = []
    for key, (stem, title) in catalog.items():
        frame = tables[key]
        # Split wide tables as well as tall ones; repeat identity columns.
        identity = [c for c in ('users', 'case', 'candidate', 'baseline',
                               'iteration', 'start_iteration', 'end_iteration') if c in frame]
        values = [c for c in frame if c not in identity]
        width = max(1, 9 - len(identity))
        chunks = [identity + values[i:i + width] for i in range(0, len(values), width)]
        for part, columns in enumerate(chunks, 1):
            for offset in range(0, len(frame), 24):
                page = frame.iloc[offset:offset + 24][columns].copy()
                for column in page:
                    page[column] = page[column].map(lambda x:
                        f'{x:.4g}' if isinstance(x, (float, np.floating)) else str(x))
                labels = [c.replace('_', '\n').title() for c in columns]
                fig, ax = plt.subplots(figsize=(max(12, len(columns) * 1.65),
                                                      max(3.5, len(page) * .38 + 2)))
                ax.axis('off')
                ax.set_title(title + f' | rows {offset + 1}-{offset + len(page)} | part {part}', pad=24)
                table = ax.table(cellText=page.values, colLabels=labels,
                                 cellLoc='center', loc='center')
                table.auto_set_font_size(False)
                table.set_fontsize(9)
                table.scale(1, 1.8)
                for (row, _), cell in table.get_celld().items():
                    cell.set_facecolor('#dbeafe' if row == 0 else ('#f1f5f9' if row % 2 else 'white'))
                    if row == 0:
                        cell.set_height(cell.get_height() * 1.8)
                fig.text(.02, .02, 'Descriptive results. Times in seconds; ratios in [0, 1]. SD is not a confidence interval.', fontsize=9)
                images.append(save_image(fig, folder, f'{stem}_phan{part}_trang{offset // 24 + 1:02d}'))
    return images


def build_convergence_figure(convergence, group, names):
    fig, ax = plt.subplots(figsize=(11, 6))
    for name in names:
        rows = convergence.query('case == @name')
        ax.plot(rows.iteration, rows['median'], label=name)
    ax.set(xlabel='Iteration', ylabel='Best evaluated fitness', title=group+' | median')
    ax.grid(alpha=.25)
    ax.legend(fontsize=8)
    return fig


def build_figures(root, output, tables, *, presentation=None):
    folder = (presentation or output) / 'picture'
    folder.mkdir(exist_ok=True)
    images = []
    for group, names in GROUPS.items():
        fig = build_convergence_figure(tables['convergence'], group, names)
        fig.tight_layout()
        suffix = 'chinh' if group == 'main' else 'woa'
        path = save_image(fig, folder, f'dothihoitu_{suffix}')
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
        path = save_image(fig, folder, f'dothisosanhvasonguoi_{suffix}')
        images.append(path)
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        for ax, metric, label in zip(axes,
                ['stage_time_s', 'fitness_gain', 'stage_fe'],
                ['Stage runtime (s)', 'Stage fitness gain', 'Stage fitness evaluations']):
            for name in names:
                g = tables['stages'].query('case == @name').sort_values('end_iteration')
                ax.plot(g.end_iteration, g[metric], marker='o', label=name)
            ax.set(xlabel='Stage end iteration', ylabel=label)
            ax.grid(alpha=.25)
        axes[0].legend(fontsize=7)
        fig.suptitle(group + ' | incremental stage metrics (initialization excluded)')
        images.append(save_image(fig, folder, f'dothigiaidoan_{suffix}'))
    fig, ax = plt.subplots(figsize=(10, 6))
    stability = tables['stability_summary']
    ax.barh(stability['case'], stability.seed_sd_mean)
    ax.set(xlabel='Mean within-dataset fitness SD across seeds', title='Seed stability (lower is more stable)')
    images.append(save_image(fig, folder, 'dothidoondinh'))
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
    path = save_image(fig, folder, 'vitribotriuav3d')
    images.append(path)
    return images


def build_report(root, output, tables):
    # Mirror nested study paths without mixing presentation files with raw results.
    relative = output.resolve().relative_to((root / 'implementation/results').resolve())
    presentation = root / 'implementation/notebooks' / relative
    presentation.mkdir(parents=True, exist_ok=True)
    images = build_figures(root, output, tables, presentation=presentation) + build_table_images(presentation, tables)
    runs, _ = read_results(output)
    manifest = json.loads((output / 'manifest.json').read_text(encoding='utf-8'))
    text = f"# Study results: {len(manifest['datasets'])} CSV, {len(manifest['cases'])} cases, {manifest['config']['iterations']} iterations\n\n"
    text += f"Seeds: {len(manifest['config']['seeds'])}; completed tasks: {len(runs)}.\n\n"
    text += 'Descriptive results only. Equal iterations do not imply equal FE. IQR is not a confidence interval.\n\n'
    text += '## Main comparison\n\n'+tables['main'].to_markdown(index=False)+'\n\n'
    text += '## Overall descriptive ranking\n\n'+tables['ranking'].to_markdown(index=False)+'\n\n'
    text += 'Best fitness is best evaluated; seed SD is computed within dataset before averaging.\n'
    text += '\nStage times and FE are endpoint differences; initialization is included in milestone 0, not in stage 0-to-first. '
    text += 'Stage summaries average over datasets and seeds; quality-by-scale SD includes both sources of variation.\n'
    text += '\n## Figures and table images\n\n'
    for path in images:
        link = Path(os.path.relpath(path, output)).as_posix()
        text += f'- [{path.stem}]({link})\n'
    (output / 'RESULTS.md').write_text(text, encoding='utf-8')
    nb = nbformat.v4.new_notebook()
    nb.cells.append(nbformat.v4.new_markdown_cell(text+
        '\nThis notebook is a report snapshot generated from saved artifacts. Outputs below were not produced by rerunning optimizers.'))
    for name, table in tables.items():
        nb.cells.append(nbformat.v4.new_markdown_cell('## '+name))
        table_link = Path(os.path.relpath(output / 'tables' / (name + '.csv'), presentation)).as_posix()
        cell = nbformat.v4.new_code_cell(f"# Run from this notebook's directory; no optimization\nimport pandas as pd\npd.read_csv({table_link!r}).head(100)")
        cell.outputs = [nbformat.v4.new_output('display_data', data={'text/html': table.head(100).to_html(index=False),
            'text/plain': table.head(100).to_string(index=False)})]
        nb.cells.append(cell)
    for path in images:
        nb.cells.append(nbformat.v4.new_markdown_cell('## '+path.stem))
        image_link = Path(os.path.relpath(path, presentation)).as_posix()
        cell = nbformat.v4.new_code_cell(f"from IPython.display import Image, display\ndisplay(Image(filename={image_link!r}))")
        cell.outputs = [nbformat.v4.new_output('display_data', data={'image/jpeg': base64.b64encode(path.read_bytes()).decode()})]
        nb.cells.append(cell)
    nbformat.write(nb, presentation / 'study_results.ipynb')
