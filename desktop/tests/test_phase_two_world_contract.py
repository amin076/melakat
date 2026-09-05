import hashlib
import math
import unittest

from melakat_desktop.artifacts import (
    SPATIAL_RUN_ARTIFACT_FORMAT,
    canonical_json,
    make_run_artifact,
)
from melakat_desktop.parameters import CORE_SCHEMA
from melakat_desktop.phase_two_engine import PhaseTwoEngine
from melakat_desktop.spatial import reflect_coordinate
from melakat_desktop.worker import create_engine
from melakat_desktop.world_contract import (
    BASELINE_SCIENTIFIC_SHA256,
    BASELINE_SNAPSHOT_SHA256,
    PHASE_TWO_WORLD_CONTRACT,
    WORLD_CONTRACT_VERSION,
    scientific_baseline_projection,
)


class PhaseTwoWorldContractTests(unittest.TestCase):
    @staticmethod
    def run_engine(config: dict) -> PhaseTwoEngine:
        engine = PhaseTwoEngine(CORE_SCHEMA.validate(config), lambda _event: None)
        while not engine.finished:
            engine.step()
        return engine

    def test_contract_version_and_reflective_topology_are_explicit(self) -> None:
        self.assertEqual(WORLD_CONTRACT_VERSION, "phase-two-spatial-0.2")
        self.assertEqual(PHASE_TWO_WORLD_CONTRACT["observation_model"], "sequential")
        self.assertEqual(PHASE_TWO_WORLD_CONTRACT["boundary_model"], "reflective")
        self.assertEqual(
            PHASE_TWO_WORLD_CONTRACT["offspring_placement_model"],
            "local_radial_dispersion_with_reflection",
        )
        self.assertEqual(PHASE_TWO_WORLD_CONTRACT["movement_model"], "none")
        self.assertEqual(PHASE_TWO_WORLD_CONTRACT["local_resource_model"], "none")

    def test_spatial_schema_defaults_are_explicit(self) -> None:
        config = CORE_SCHEMA.defaults()
        self.assertFalse(config["world.spatial_enabled"])
        self.assertEqual(config["world.boundary_model"], "reflective")
        self.assertEqual(config["world.offspring_dispersion_radius"], 1.0)
        self.assertEqual(config["world.neighborhood_radius"], 2.0)

    def test_reflect_coordinate_handles_both_boundaries_and_large_overshoot(self) -> None:
        self.assertAlmostEqual(reflect_coordinate(3.0, 10.0), 3.0)
        self.assertAlmostEqual(reflect_coordinate(-2.0, 10.0), 2.0)
        self.assertAlmostEqual(reflect_coordinate(12.0, 10.0), 8.0)
        self.assertAlmostEqual(reflect_coordinate(27.0, 10.0), 7.0)
        self.assertAlmostEqual(reflect_coordinate(-27.0, 10.0), 7.0)
        with self.assertRaises(ValueError):
            reflect_coordinate(1.0, 0.0)

    def test_spatial_mode_can_be_enabled_with_reflective_boundary(self) -> None:
        config = CORE_SCHEMA.defaults()
        config["run.engine_backend"] = "phase-two-vm"
        config["world.spatial_enabled"] = True
        engine = PhaseTwoEngine(CORE_SCHEMA.validate(config), lambda _event: None)
        self.assertTrue(engine.spatial_enabled)
        self.assertEqual(engine.boundary_model, "reflective")

    def test_worker_exposes_phase_two_backend(self) -> None:
        config = CORE_SCHEMA.defaults()
        config["run.engine_backend"] = "phase-two-vm"
        engine = create_engine(config, lambda _event: None)
        self.assertIsInstance(engine, PhaseTwoEngine)

    def test_disabled_spatial_mode_preserves_phase_one_baseline(self) -> None:
        config = CORE_SCHEMA.defaults()
        config["run.engine_backend"] = "phase-two-vm"
        config["run.max_ticks"] = 2000
        config["run.seed"] = 1
        config["run.emit_snapshots"] = False
        config["world.spatial_enabled"] = False

        engine = self.run_engine(config)
        summary = engine.summary()

        projection = scientific_baseline_projection(summary)
        scientific_digest = hashlib.sha256(
            canonical_json(projection).encode("utf-8")
        ).hexdigest()
        snapshot_projection = scientific_baseline_projection(
            {"final_snapshot": summary["final_snapshot"]}
        )["final_snapshot"]
        snapshot_digest = hashlib.sha256(
            canonical_json(snapshot_projection).encode("utf-8")
        ).hexdigest()

        self.assertEqual(scientific_digest, BASELINE_SCIENTIFIC_SHA256)
        self.assertEqual(snapshot_digest, BASELINE_SNAPSHOT_SHA256)

    def test_spatial_mode_preserves_nonspatial_dynamics_for_same_seed(self) -> None:
        base = CORE_SCHEMA.defaults()
        base["run.engine_backend"] = "phase-two-vm"
        base["run.max_ticks"] = 500
        base["run.seed"] = 7
        base["run.emit_snapshots"] = False

        disabled = dict(base)
        disabled["world.spatial_enabled"] = False
        enabled = dict(base)
        enabled["world.spatial_enabled"] = True

        disabled_summary = self.run_engine(disabled).summary()
        enabled_summary = self.run_engine(enabled).summary()

        keys = (
            "tick",
            "active_population",
            "births",
            "deaths",
            "max_population",
            "active_genotypes",
            "historical_genotypes",
            "active_lineages",
            "max_generation",
            "instructions_executed",
            "faults",
            "pending_divisions",
            "blocked_divisions",
            "waiting_for_memory",
            "waiting_for_energy",
            "waiting_disabled",
            "energy_pool",
            "memory_used",
            "free_memory",
            "energy_balance_error",
            "death_reasons",
            "ledger",
            "genealogy",
            "genotype_catalog",
        )
        for key in keys:
            self.assertEqual(disabled_summary[key], enabled_summary[key], key)

    def test_spatial_births_are_local_deterministic_and_inside_bounds(self) -> None:
        config = CORE_SCHEMA.defaults()
        config["run.engine_backend"] = "phase-two-vm"
        config["run.max_ticks"] = 500
        config["run.seed"] = 11
        config["run.emit_snapshots"] = False
        config["world.spatial_enabled"] = True
        config["world.offspring_dispersion_radius"] = 1.5

        first = self.run_engine(config)
        second = self.run_engine(config)
        self.assertEqual(first.snapshot(), second.snapshot())

        width = float(config["world.width"])
        height = float(config["world.height"])
        radius = float(config["world.offspring_dispersion_radius"])
        by_id = {organism.organism_id: organism for organism in first.organisms}
        children = [organism for organism in first.organisms if organism.parent_id is not None]
        self.assertGreater(len(children), 0)

        for organism in first.organisms:
            self.assertGreaterEqual(organism.x, 0.0)
            self.assertLessEqual(organism.x, width)
            self.assertGreaterEqual(organism.y, 0.0)
            self.assertLessEqual(organism.y, height)

        for child in children:
            parent = by_id[child.parent_id]
            distance = math.hypot(child.x - parent.x, child.y - parent.y)
            self.assertLessEqual(distance, radius + 1e-12)

    def test_spatial_metrics_cover_birth_distance_neighborhood_and_occupancy(self) -> None:
        config = CORE_SCHEMA.defaults()
        config["run.engine_backend"] = "phase-two-vm"
        config["run.max_ticks"] = 500
        config["run.seed"] = 3
        config["run.emit_snapshots"] = False
        config["world.spatial_enabled"] = True

        summary = self.run_engine(config).summary()
        self.assertGreater(summary["spatial_births"], 0)
        self.assertGreaterEqual(summary["boundary_contacts"], 0)
        self.assertGreaterEqual(summary["mean_parent_child_distance"], 0.0)
        self.assertLessEqual(
            summary["mean_parent_child_distance"],
            config["world.offspring_dispersion_radius"],
        )
        self.assertGreaterEqual(summary["mean_local_neighbors"], 0.0)
        self.assertGreaterEqual(summary["mean_nearest_neighbor_distance"], 0.0)
        self.assertGreaterEqual(summary["occupied_spatial_bins"], 1)
        self.assertGreater(summary["spatial_occupancy_fraction"], 0.0)
        self.assertLessEqual(summary["spatial_occupancy_fraction"], 1.0)

    def test_world_contract_metadata_is_exposed_and_artifact_versioned(self) -> None:
        config = CORE_SCHEMA.defaults()
        config["run.engine_backend"] = "phase-two-vm"
        engine = PhaseTwoEngine(config, lambda _event: None)
        summary = engine.summary()

        self.assertEqual(summary["world_contract_version"], WORLD_CONTRACT_VERSION)
        self.assertFalse(summary["spatial_enabled"])
        self.assertEqual(engine.snapshot()["world_contract_version"], WORLD_CONTRACT_VERSION)

        artifact = make_run_artifact(config, summary)
        self.assertEqual(artifact["format"], SPATIAL_RUN_ARTIFACT_FORMAT)
        self.assertEqual(artifact["world_contract_version"], WORLD_CONTRACT_VERSION)


if __name__ == "__main__":
    unittest.main()
