"""Independent numerical audit; does not modify the model. Exit 1 means findings exist."""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.physics.channel import (compute_distance_3d, compute_elevation_angle_deg,
    compute_los_probability, compute_path_loss, compute_snr)
from src.objectives.metrics import (calculate_coverage_rate, calculate_interference_rate,
    calculate_energy_consumption, evaluate_solution)
from src.problem.objective import UAVPlacementProblem


def main():
    rows = []

    def check(name, inputs, actual, expected, note=""):
        passed = bool(np.allclose(actual, expected, atol=1e-8, rtol=1e-8))
        rows.append(dict(case=name, inputs=inputs, actual=np.asarray(actual).tolist(),
                         expected=np.asarray(expected).tolist(), passed=passed, note=note))

    u = np.array([[0., 0., 50.]])
    ue = np.array([[0., 0., 0.]])
    check("distance_vertical", "UAV=(0,0,50); UE=(0,0,0)", compute_distance_3d(u, ue), [[50.]])
    check("distance_3_4_12", "UAV=(3,4,12); UE=(0,0,0)", compute_distance_3d(np.array([[3.,4.,12.]]), ue), [[13.]])
    check("elevation_vertical", "height difference=50; distance=50", compute_elevation_angle_deg(u,ue,np.array([[50.]])), [[90.]])
    check("elevation_45", "UAV=(50,0,50); UE=(0,0,0)", compute_elevation_angle_deg(np.array([[50.,0.,50.]]),ue,np.array([[math.sqrt(5000)]])), [[45.]])
    check("los_at_a", "angle=9.61 degrees; a=9.61", compute_los_probability(np.array([9.61])), [1/10.61])
    check("pathloss_los_1m", "d=1m; f=3.5GHz; PLoS=1", compute_path_loss(np.array([1.]),np.array([1.])), [20*math.log10(4*math.pi*3.5e9/3e8)+1])
    check("pathloss_nlos_difference", "same distance; LoS vs NLoS", compute_path_loss(np.array([100.]),np.array([0.]))-compute_path_loss(np.array([100.]),np.array([1.])), [19.])
    check("snr_threshold", "Ptx=30dBm; PL=116dB; noise=-104dBm", compute_snr(np.array([116.])), [18.])
    s = np.array([[20.,17.,18.,0.],[19.,16.,10.,0.]])
    check("coverage_boundary", s.tolist(), calculate_coverage_rate(s)[0], .5)
    check("overlap_count", s.tolist(), calculate_interference_rate(s), .25)
    for z, expected in [(50.,101/151),(175.,126/151),(300.,1.)]:
        check(f"power_z_{z:g}", {"z":z}, calculate_energy_consumption(np.array([[0.,0.,z]])), expected,
              "Checks arithmetic of the current surrogate, not physical validity.")
    r = evaluate_solution(u,ue)
    check("fitness_overhead", {"UAV":u.tolist(),"UE":ue.tolist()}, r.fitness, .6-.2*101/151)
    far = evaluate_solution(np.array([[1000.,1000.,50.]]),ue)
    check("fitness_far_uncovered", "UE=(0,0,0); UAV=(1000,1000,50)", far.fitness, -.2*101/151)
    p = UAVPlacementProblem(ue,num_uavs=1,min_altitude=100,max_altitude=200)
    check("custom_altitude_propagation", "configured altitude=100..200; UAV=(0,0,100)",
          p.evaluate_detailed(np.array([0.,0.,100.])).energy_normalized,101/151,
          "Regression check: configured altitude bounds must reach the energy calculation.")
    p4 = UAVPlacementProblem(ue,num_uavs=4)
    collision_accepted = np.isfinite(p4.evaluate(np.tile([0.,0.,50.],4)))
    check("reject_coincident_uavs", "four UAVs at (0,0,50)", bool(collision_accepted), False,
          "Safety audit expectation: a coincident placement must be identified as infeasible; the configured minimum distance must be enforced.")
    print(json.dumps(dict(passed=sum(r['passed'] for r in rows),total=len(rows),checks=rows),ensure_ascii=False,indent=2))
    return int(any(not r['passed'] for r in rows))


if __name__ == '__main__':
    sys.exit(main())
