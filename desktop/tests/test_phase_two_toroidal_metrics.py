from types import SimpleNamespace
import unittest

from melakat_desktop.spatial import (
    local_neighbor_count,
    population_spatial_metrics,
    spatial_distance,
)


class ToroidalSpatialMetricTests(unittest.TestCase):
    def setUp(self) -> None:
        self.left = SimpleNamespace(
            organism_id=1,
            alive=True,
            x=0.5,
            y=10.0,
        )
        self.right = SimpleNamespace(
            organism_id=2,
            alive=True,
            x=99.5,
            y=10.0,
        )
        self.organisms = [self.left, self.right]

    def test_toroidal_shortest_distance_wraps_across_world_edge(self) -> None:
        self.assertAlmostEqual(
            spatial_distance(
                self.left.x,
                self.left.y,
                self.right.x,
                self.right.y,
                width=100.0,
                height=70.0,
                boundary_model="toroidal",
            ),
            1.0,
        )
        self.assertAlmostEqual(
            spatial_distance(
                self.left.x,
                self.left.y,
                self.right.x,
                self.right.y,
                width=100.0,
                height=70.0,
                boundary_model="reflective",
            ),
            99.0,
        )

    def test_neighbor_count_respects_active_boundary_model(self) -> None:
        self.assertEqual(
            local_neighbor_count(
                self.left,
                self.organisms,
                2.0,
                width=100.0,
                height=70.0,
                boundary_model="toroidal",
            ),
            1,
        )
        self.assertEqual(
            local_neighbor_count(
                self.left,
                self.organisms,
                2.0,
                width=100.0,
                height=70.0,
                boundary_model="reflective",
            ),
            0,
        )

    def test_population_metrics_use_wrapped_nearest_neighbor_distance(self) -> None:
        toroidal = population_spatial_metrics(
            self.organisms,
            width=100.0,
            height=70.0,
            neighborhood_radius=2.0,
            boundary_model="toroidal",
        )
        reflective = population_spatial_metrics(
            self.organisms,
            width=100.0,
            height=70.0,
            neighborhood_radius=2.0,
            boundary_model="reflective",
        )
        self.assertEqual(toroidal["mean_local_neighbors"], 1.0)
        self.assertEqual(toroidal["mean_nearest_neighbor_distance"], 1.0)
        self.assertEqual(reflective["mean_local_neighbors"], 0.0)
        self.assertEqual(reflective["mean_nearest_neighbor_distance"], 99.0)


if __name__ == "__main__":
    unittest.main()
