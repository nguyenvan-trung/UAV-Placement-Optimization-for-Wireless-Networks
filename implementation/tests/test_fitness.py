"""Audit current behavior against a scalar oracle, not production helpers.

CSV records characterization checks; PASS does not validate physical assumptions.
Run without pytest-xdist so this single CSV has one writer.
"""
import csv
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'implementation'))
from src.problem.objective import UAVPlacementProblem
from src.objectives.metrics import calculate_coverage_rate, calculate_interference_rate
from src.physics.channel import compute_distance_3d, compute_elevation_angle_deg, compute_snr

BASE = [[200.,200.,50.],[400.,200.,50.],[200.,400.,50.],[400.,400.,50.]]
CLUSTER = [[290.,290.,0.],[300.,300.,0.],[310.,310.,0.]]


def variant(index, value):
    coords = np.array(BASE).copy()
    coords[index] = value
    return coords.tolist()


CASES = [
    ('cluster_center', BASE, CLUSTER, {}, 'normal'),
    ('far_from_users', BASE, [[1000.,1000.,0.]], {}, 'normal'),
    ('low_altitude', BASE, CLUSTER, {}, 'normal'),
    ('high_altitude', [[x,y,300.] for x,y,z in BASE], CLUSTER, {}, 'normal'),
    ('too_close', variant(1,[205.,200.,50.]), CLUSTER, {}, 'collision'),
    ('partly_uncovered', BASE, [[200.,200.,0.],[1000.,1000.,0.]], {}, 'normal'),
    ('out_of_xy', variant(0,[-100.,200.,50.]), CLUSTER, {}, 'repair'),
    ('out_of_altitude', variant(0,[200.,200.,20.]), CLUSTER, {}, 'repair'),
    ('coincident_uavs', variant(1,BASE[0]), CLUSTER, {}, 'collision'),
    ('wrong_uav_count', BASE[:3], CLUSTER, {}, 'shape_error'),
    ('separation_boundary', variant(1,[210.,200.,50.]), CLUSTER, {}, 'normal'),
    ('custom_altitude', [[x,y,100.] for x,y,z in BASE], CLUSTER,
     {'min_altitude':100.,'max_altitude':200.}, 'normal'),
]


def oracle(coords, users, min_alt=50., max_alt=300.):
    """Scalar equations with atan2 geometry and explicit per-user counting."""
    links = []
    for ux,uy,uz in users:
        values = []
        for x,y,z in coords:
            horizontal = math.hypot(x-ux,y-uy)
            distance = max(math.sqrt(horizontal**2+(z-uz)**2), .001)
            angle = max(0., math.degrees(math.atan2(z-uz,horizontal)))
            los = 1/(1+9.61*math.exp(-.16*(angle-9.61)))
            loss = 20*math.log10(4*math.pi*3.5e9*distance/3e8)+los*1+(1-los)*20
            values.append(30-loss+104)
        links.append(values)
    covered = sum(any(s >= 18 for s in row) for row in links)
    overlap = sum(sum(s >= 18 for s in row) >= 2 for row in links)/len(users)
    # Preserve the documented numerical regularizer in the current surrogate.
    energy = sum((100*(1+.5*min(1.,max(0.,(z-min_alt)/(max_alt-min_alt+1e-6))))+1)/151
                 for x,y,z in coords)/len(coords)
    coverage = covered/len(users)
    return {'coverage':coverage,'energy':energy,'overlap':overlap,
            'fitness':.6*coverage-.2*energy-.2*overlap,'covered':covered,'snr':links}


def independent_feasible(coords, low, high, count=4):
    if len(coords) != count:
        return False
    if any(not (0 <= x <= 1000 and 0 <= y <= 1000 and low <= z <= high) for x,y,z in coords):
        return False
    return all(math.dist(coords[i],coords[j]) >= 10 for i in range(count) for j in range(i))


@pytest.fixture(scope='module')
def audit_rows():
    rows = []
    yield rows
    destination = ROOT/'reports'/'fitness_audit.csv'
    destination.parent.mkdir(exist_ok=True)
    if rows:
        with destination.open('w',newline='',encoding='utf-8-sig') as stream:
            writer = csv.DictWriter(stream,fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)


@pytest.mark.parametrize('name,coords,users,options,behavior', CASES, ids=[c[0] for c in CASES])
def test_fitness_cases(name,coords,users,options,behavior,audit_rows):
    p = UAVPlacementProblem(np.array(users), **options)
    low,high = options.get('min_altitude',50.),options.get('max_altitude',300.)
    raw = np.array(coords).ravel()
    raw_feasible = independent_feasible(coords,low,high)
    repaired = [[min(1000.,max(0.,x)),min(1000.,max(0.,y)),min(high,max(low,z))] for x,y,z in coords]
    expected = oracle(repaired, users, low, high)
    snapshot = hashlib.sha256(b''.join((ROOT/f).read_bytes() for f in [
        'implementation/src/problem/objective.py','implementation/src/objectives/metrics.py',
        'implementation/src/physics/channel.py','implementation/src/problem/constraints.py',
        'implementation/src/constants/network.py','implementation/src/problem/search_space.py',
        'implementation/src/problem/solution_encoding.py',
    ])).hexdigest()
    row = dict(case=name, input_uavs=json.dumps(coords), input_ues=json.dumps(users),
               config=json.dumps(options), source_sha256=snapshot,
               raw_feasible_expected=raw_feasible,raw_feasible_actual='',
               evaluated_uavs=json.dumps(repaired) if behavior!='shape_error' else 'N/A',
               repaired_feasible='',coverage='',energy='',overlap='',fitness='',
               expected=json.dumps(expected),expected_behavior=behavior,
               verification='Scalar math: Euclid, atan2, LoS, FSPL; explicit UE count; power ratio; pairwise distance.',
               status='FAIL',error='')
    try:
        if behavior == 'shape_error':
            with pytest.raises(ValueError): p.evaluate(raw)
            with pytest.raises(ValueError): p.is_feasible(raw)
            with pytest.raises(ValueError): p.evaluate_detailed(raw)
            row.update(raw_feasible_actual='ValueError',fitness='ValueError',
                       coverage='N/A: invalid UAV count',energy='N/A: invalid UAV count',overlap='N/A: invalid UAV count')
        else:
            actual_feasible = p.is_feasible(raw)
            row['raw_feasible_actual'] = actual_feasible
            assert actual_feasible == raw_feasible
            row['repaired_feasible'] = p.is_feasible(np.array(repaired).ravel())
            result = p.evaluate(raw)
            row['fitness'] = result
            if behavior == 'collision':
                assert result == -math.inf
                with pytest.raises(ValueError): p.evaluate_detailed(raw)
                row.update(coverage='N/A: infeasible',energy='N/A: infeasible',overlap='N/A: infeasible')
            else:
                actual = p.evaluate_detailed(raw)
                row.update(coverage=actual.coverage_rate,energy=actual.energy_normalized,overlap=actual.interference_rate)
                for got,want in [(actual.coverage_rate,expected['coverage']),
                                 (actual.energy_normalized,expected['energy']),
                                 (actual.interference_rate,expected['overlap']),
                                 (actual.fitness,expected['fitness']),(result,expected['fitness'])]:
                    assert got == pytest.approx(want,abs=1e-10)
                assert actual.covered_users_count == expected['covered']
                if name == 'partly_uncovered': assert 0 < actual.coverage_rate < 1
        row['status'] = 'PASS'
    except BaseException as exc:
        row['error'] = str(exc)
        raise
    finally:
        audit_rows.append(row)


def test_threshold_is_inclusive():
    snr = np.array([[18.,17.999,18.001]])
    assert calculate_coverage_rate(snr)[0] == pytest.approx(2/3)
    assert calculate_interference_rate(snr) == 0
    assert compute_snr(np.array([116.]))[0] == 18


def test_ue_height_and_degree_geometry():
    u,ue = np.array([[3.,4.,17.]]),np.array([[0.,0.,5.]])
    d = compute_distance_3d(u,ue)
    assert d[0,0] == 13
    assert compute_elevation_angle_deg(u,ue,d)[0,0] == pytest.approx(math.degrees(math.atan2(12,5)))


def test_energy_random_variance():
    from src.objectives.metrics import calculate_energy_consumption
    rng = np.random.default_rng(20261024)
    rows = []
    for sample_id in range(1000):
        coords = rng.uniform([0.,0.,50.],[1000.,1000.,300.],size=(4,3))
        actual = calculate_energy_consumption(coords)
        expected = sum(101+50*(float(z)-50)/(250+1e-6) for z in coords[:,2])/(4*151)
        assert actual == pytest.approx(expected,abs=1e-12)
        # E must depend on altitude only under the current surrogate.
        shifted = coords.copy()
        shifted[:,:2] = rng.uniform(0,1000,size=(4,2))
        assert calculate_energy_consumption(shifted) == actual
        rows.append(dict(sample_id=sample_id,seed=20261024,uavs=json.dumps(coords.tolist()),
                         energy=actual,expected_energy=expected,feasible=independent_feasible(coords.tolist(),50,300)))
    path = ROOT/'reports/fitness_energy_samples.csv'
    with path.open('w',newline='',encoding='utf-8-sig') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    observed = np.var([r['energy'] for r in rows],ddof=1)
    theoretical = (50*250/((250+1e-6)*151))**2/(12*4)
    assert observed == pytest.approx(theoretical,rel=.2)


def test_report_energy_inversion():
    # Historical values supplied by the user; input evidence, not simulated results.
    c,i,f = .9991,.0572,.4505
    energy = (.6*c-.2*i-f)/.2
    minimum = 101/151
    assert minimum <= energy <= 1
    path=ROOT/'reports/fitness_report_reconciliation.csv'
    row=dict(source='user supplied historical tuple; aggregation unverified',coverage=c,interference=i,
             fitness=f,inferred_energy=energy,minimum_energy=minimum,
             reported_energy='UNKNOWN: original report/log unavailable',comparison='UNVERIFIED',
             assumption='C I F must share the same runs and aggregation')
    with path.open('w',newline='',encoding='utf-8-sig') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(row)); writer.writeheader(); writer.writerow(row)


def test_max_snr_equivalence_four_uavs():
    # Each column has a distinct strongest UAV; denominator is all UE, not served UE.
    snr=np.array([[19.,0.,0.,0.,0.],[0.,20.,0.,0.,0.],
                  [0.,0.,18.,0.,0.],[0.,0.,0.,17.,0.]])
    assert calculate_coverage_rate(snr)[0] == pytest.approx(3/5)
