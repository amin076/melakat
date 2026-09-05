import hashlib
import unittest

from melakat_desktop.artifacts import canonical_json
from melakat_desktop.parameters import CORE_SCHEMA
from melakat_desktop.phase_two_engine import PhaseTwoEngine
from melakat_desktop.world_contract import (
    BASELINE_SCIENTIFIC_SHA256,
    BASELINE_SNAPSHOT_SHA256,
    PHASE_TWO_WORLD_CONTRACT,
    WORLD_CONTRACT_VERSION,
    scientific_baseline_projection,
)


class PhaseTwoWorldContractTests(unittest.TestCase):
    def test_contract_version_and_tick_order_are_explicit(self) -> None:
        self.assertEqual(WORLD_CONTRACT_VERSION, "phase-two-spatial-0.1")
        self.assertEqual(PHASE_TWO_WORLD_CONTRACT["observation_model"], "sequential")
        self.assertEqual(
            PHASE_TWO_WORLD_CONTRACT["tick_order"],
            [
                "environment_update",
                "active_schedule_shuffle",
                "organism_age_increment",
                "global_energy_capture",
                "maintenance_cost",
                "pending_division_retry_or_vm_execution",
                "execution_cost",
                "fault_or_energy_death",
                "division_attempt",
                "history_snapshot_and_finish",
            ],
        )

    def test_spatial_mode_defaults_off(self) -> None:
        config = CORE_SCHEMA.defaults()
        self.assertIn("world.spatial_enabled", config)
        self.assertFalse(config["world.spatial_enabled"])

    def test_enabling_spatial_rules_is_rejected_until_p2_2(self) -> None:
        config = CORE_SCHEMA.defaults()
        config["world.spatial_enabled"] = True
        with self.assertRaisesRegex(ValueError, "spatial_rules_not_implemented"):
            PhaseTwoEngine(config, lambda _event: None)

    def test_disabled_spatial_mode_preserves_phase_one_baseline(self) -> None:
        config = CORE_SCHEMA.defaults()
        config["run.engine_backend"] = "phase-two-vm"
        config["run.max_ticks"] = 2000
        config["run.seed"] = 1
        config["run.emit_snapshots"] = False
        config["world.spatial_enabled"] = False
        config = CORE_SCHEMA.validate(config)

        engine = PhaseTwoEngine(config, lambda _event: None)
        while not engine.finished:
            engine.step()
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

    def test_world_contract_metadata_is_exposed(self) -> None:
        config = CORE_SCHEMA.defaults()
        config["run.engine_backend"] = "phase-two-vm"
        engine = PhaseTwoEngine(config, lambda _event: None)
        self.assertEqual(
            engine.metrics()["world_contract_version"],
            WORLD_CONTRACT_VERSION,
        )
        self.assertFalse(engine.metrics()["spatial_enabled"])
        self.assertEqual(
            engine.snapshot()["world_contract_version"],
            WORLD_CONTRACT_VERSION,
        )


if __name__ == "__main__":
    unittest.main()
