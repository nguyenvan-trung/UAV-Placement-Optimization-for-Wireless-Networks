import unittest
import numpy as np
from src.problem.objective import UAVPlacementProblem


class FitnessRegressionTests(unittest.TestCase):
    def setUp(self):
        self.ue = np.array([[0., 0., 0.]])

    def test_custom_altitude_in_both_evaluation_paths(self):
        p = UAVPlacementProblem(self.ue, num_uavs=1, min_altitude=100, max_altitude=200)
        x = np.array([0., 0., 100.])
        self.assertAlmostEqual(p.evaluate_detailed(x).energy_normalized, 101/151)
        self.assertAlmostEqual(p.evaluate(x), .6-.2*101/151)
        self.assertEqual(p.evaluate(x), p.evaluate_detailed(x).fitness)

    def test_collision_is_rejected(self):
        p = UAVPlacementProblem(self.ue, num_uavs=2)
        x = np.array([0.,0.,50.,0.,0.,50.])
        self.assertFalse(p.is_feasible(x))
        self.assertEqual(p.evaluate(x), -np.inf)
        with self.assertRaisesRegex(ValueError, 'Infeasible'):
            p.evaluate_detailed(x)

    def test_boundary_uses_3d_distance(self):
        p = UAVPlacementProblem(self.ue, num_uavs=2, min_uav_distance=20)
        self.assertTrue(p.is_feasible(np.array([0.,0.,50.,0.,0.,70.])))
        self.assertFalse(p.is_feasible(np.array([0.,0.,50.,0.,0.,69.])))

    def test_clipping_does_not_hide_collision(self):
        p = UAVPlacementProblem(self.ue, num_uavs=2)
        self.assertEqual(p.evaluate(np.array([-1.,0.,50.,0.,0.,50.])), -np.inf)

    def test_bad_shape_and_nan_rejected(self):
        p = UAVPlacementProblem(self.ue)
        for x in (np.zeros(3), np.full(12, np.nan)):
            with self.assertRaises(ValueError):
                p.evaluate(x)

    def test_legacy_separation_can_be_disabled(self):
        p = UAVPlacementProblem(self.ue, num_uavs=2, min_uav_distance=0)
        self.assertTrue(np.isfinite(p.evaluate(np.array([0.,0.,50.,0.,0.,50.]))))
