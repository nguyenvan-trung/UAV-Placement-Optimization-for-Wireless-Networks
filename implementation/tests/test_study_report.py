"""Report calculations and JPEG rendering without optimizers or disk artifacts."""
import io
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from src import notebook_study as study
from src import study_report as report


def test_stage_deltas_scale_groups_and_paired_comparisons(monkeypatch):
    artifacts = []
    for users in (100, 200):
        for seed in (1, 2):
            for index, case in enumerate(study.cases()):
                rows = [dict(iteration=i, fitness=.1 + index * .01 + i * .001,
                    coverage=.8, energy=.7, interference=.1, fe=25 + i * 25,
                    elapsed_s=2 + i * users / 100, position=[0., 0., 100.])
                    for i in range(81)]
                final = rows[-1]
                record = dict(dataset=f'{users}.csv', users=users, seed=seed,
                    case=case['case'], fitness=final['fitness'], coverage=.8,
                    energy=.7, interference=.1, wall_s=final['elapsed_s'], fe=final['fe'])
                artifacts.append(dict(result=record, history=rows))
    frame = pd.DataFrame([a['result'] for a in artifacts])
    manifest = dict(datasets=['100.csv', '200.csv'], cases=study.cases(),
                    config=dict(iterations=80, seeds=[1, 2]))
    monkeypatch.setattr(study, 'read_results', lambda _: (frame, pd.DataFrame()))
    monkeypatch.setattr(study, 'task_paths', lambda _: range(len(artifacts)))
    monkeypatch.setattr(study, 'read_task', lambda index: artifacts[index])
    monkeypatch.setattr(Path, 'read_text', lambda *a, **k: json.dumps(manifest))
    monkeypatch.setattr(Path, 'mkdir', lambda *a, **k: None)
    monkeypatch.setattr(Path, 'write_text', lambda *a, **k: None)
    monkeypatch.setattr(pd.DataFrame, 'to_csv', lambda *a, **k: None)
    tables = study.build_tables(Path('unused'))
    assert set(tables['checkpoints'].iteration) == {0, 20, 40, 60, 80}
    stages = tables['stages_by_scale']
    assert len(stages) == 2 * 12 * 4
    assert stages.fitness_gain.to_numpy() == pytest.approx([.02] * len(stages))
    assert (stages.stage_fe == 500).all()
    assert (stages.query('users == 100').stage_time_s == 20).all()
    assert (stages.query('users == 200').stage_time_s == 40).all()
    assert (tables['stages'].stage_time_s == 30).all()
    assert len(tables['paired_comparison']) == 5
    assert len(tables['quality_by_scale']) == 24
    # Initial 2 seconds belong to checkpoint 0, not the first stage.
    assert (tables['checkpoints'].query('iteration == 0').elapsed_s == 2).all()


def test_table_images_are_jpeg_with_ascii_vietnamese_names(monkeypatch):
    keys = ['main', 'WOA', 'design', 'ranking', 'quality_by_scale', 'checkpoints',
            'stages', 'stages_by_scale', 'stability_summary', 'contributions', 'paired_comparison']
    tables = {key: pd.DataFrame(dict(case=['PSO'] * 25, fitness_mean=[.1234] * 25))
              for key in keys}
    monkeypatch.setattr(Path, 'mkdir', lambda *a, **k: None)
    outputs = []
    def save(fig, folder, stem):
        buffer = io.BytesIO()
        fig.savefig(buffer, format='jpeg', dpi=40)
        assert buffer.getvalue().startswith(b'\xff\xd8')
        assert stem.isascii() and ' ' not in stem
        plt.close(fig)
        outputs.append(stem)
        return folder / (stem + '.jpg')
    monkeypatch.setattr(report, 'save_image', save)
    paths = report.build_table_images(Path('unused'), tables)
    assert len(paths) == 22  # Every table has two readable pages.
    assert len(set(outputs)) == 22
    assert all(path.suffix == '.jpg' for path in paths)


def test_convergence_figure_draws_median_lines_without_shaded_bands():
    convergence = pd.DataFrame([
        dict(case=case, iteration=iteration, median=value, q25=value - .1, q75=value + .1)
        for case, values in [('GA', [.2, .4]), ('PSO', [.3, .5])]
        for iteration, value in enumerate(values)
    ])

    fig = report.build_convergence_figure(convergence, 'main', ['GA', 'PSO'])
    ax = fig.axes[0]
    try:
        assert len(ax.lines) == 2
        assert [line.get_label() for line in ax.lines] == ['GA', 'PSO']
        assert list(ax.lines[0].get_ydata()) == [.2, .4]
        assert not ax.collections
        assert ax.get_title() == 'main | median'
    finally:
        plt.close(fig)


def test_report_keeps_notebook_separate_from_results(monkeypatch):
    root = Path.cwd()
    output = root / 'implementation/results/example_study'
    presentation = root / 'implementation/notebooks/example_study'
    writes = {}
    monkeypatch.setattr(Path, 'mkdir', lambda *a, **k: None)
    monkeypatch.setattr(Path, 'read_text', lambda *a, **k: json.dumps(
        dict(datasets=['sample'], cases=[{}], config=dict(iterations=80, seeds=[1, 2]))))
    monkeypatch.setattr(Path, 'write_text', lambda path, value, **k: writes.update({path: value}))
    def figures(root_arg, result_arg, tables, *, presentation):
        assert result_arg == output
        assert presentation == root / 'implementation/notebooks/example_study'
        return []
    monkeypatch.setattr(report, 'build_figures', figures)
    monkeypatch.setattr(report, 'build_table_images', lambda path, tables:
        [] if path == presentation else pytest.fail('Wrong table image directory'))
    monkeypatch.setattr(report, 'read_results', lambda _: (pd.DataFrame([{}]), None))
    monkeypatch.setattr(report.nbformat, 'write', lambda nb, path: writes.update({path: nb}))
    table = pd.DataFrame(dict(case=['PSO'], fitness=[.5]))
    report.build_report(root, output, dict(main=table, ranking=table))
    assert output / 'RESULTS.md' in writes
    notebook = writes[presentation / 'study_results.ipynb']
    assert '../../results/example_study/tables/main.csv' in notebook.cells[2].source
