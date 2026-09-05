from __future__ import annotations

import unittest

from melakat_desktop.parameters import CORE_SCHEMA
from melakat_desktop.phase_two_engine import PhaseTwoEngine
from melakat_desktop.phase_two_experiment import (
    PHASE_TWO_CONDITIONS,
    performance_probe,
    run_phase_two_matrix,
)
from melakat_desktop.phase_two_vm import PhaseTwoOpcode
from melakat_desktop.resources import LocalResourceField
from melakat_desktop.spatial import apply_boundary
from melakat_desktop.vm import Instruction, Opcode
from melakat_desktop.world_contract import WORLD_CONTRACT_VERSION


class PhaseTwoCompletionTests(unittest.TestCase):
    def _config(self) -> dict[str, object]:
        config = CORE_SCHEMA.defaults()
        config.update(
            {
                "run.engine_backend": "phase-two-vm",
                "run.seed": 7,
                "run.max_ticks": 40,
                "run.emit_snapshots": False,
                "world.spatial_enabled": True,
                "world.local_resources_enabled": True,
                "world.organism_actions_enabled": False,
                "world.memory_capacity": 2000,
            }
        )
        return CORE_SCHEMA.validate(config)

    def test_final_contract_version_is_explicit(self) -> None:
        self.assertEqual(WORLD_CONTRACT_VERSION, "phase-two-spatial-0.7")
        engine = PhaseTwoEngine(self._config(), lambda _event: None)
        self.assertEqual(engine.engine_version, "phase-two-vm-0.7")
        self.assertEqual(engine.measurement_version, "phase-two-measurement-0.1")

    def test_resource_field_never_goes_negative_and_conserves_transfers(self) -> None:
        field = LocalResourceField(width=100.0, height=70.0, cols=10, rows=7)
        field.seed_uniform(700.0)
        field.renew_uniform(70.0)
        captured = field.capture(5.0, 5.0, 20.0)
        self.assertEqual(captured, 20.0)
        self.assertGreaterEqual(field.minimum(), 0.0)
        self.assertAlmostEqual(field.total(), 750.0, places=9)
        self.assertLessEqual(abs(field.balance_error()), 1e-9)

    def test_local_resource_engine_has_independent_resource_ledger(self) -> None:
        engine = PhaseTwoEngine(self._config(), lambda _event: None)
        for _ in range(20):
            engine.step()
        metrics = engine.metrics()
        self.assertTrue(metrics["local_resources_enabled"])
        self.assertGreaterEqual(metrics["local_resource_total"], 0.0)
        self.assertLessEqual(abs(metrics["local_resource_balance_error"]), 1e-7)
        self.assertIn("resource_input", metrics["resource_ledger"])
        self.assertIn("resource_captured", metrics["resource_ledger"])
        self.assertLessEqual(abs(metrics["energy_balance_error"]), 1e-7)

    def test_snapshot_exposes_resource_layer_and_local_organism_context(self) -> None:
        engine = PhaseTwoEngine(self._config(), lambda _event: None)
        snapshot = engine.snapshot()
        self.assertIn("resource_grid", snapshot)
        self.assertEqual(snapshot["resource_grid"]["cols"], 10)
        organism = snapshot["organisms"][0]
        self.assertIn("local_resource", organism)
        self.assertIn("local_neighbors", organism)

    def test_phase_two_instruction_set_has_only_bounded_environment_primitives(self) -> None:
        self.assertEqual(
            {opcode.name for opcode in PhaseTwoOpcode},
            {"SENSE_RESOURCE", "MOVE_X", "MOVE_Y"},
        )

    def test_sense_resource_writes_a_register_without_moving(self) -> None:
        config = self._config()
        config["world.organism_actions_enabled"] = True
        engine = PhaseTwoEngine(CORE_SCHEMA.validate(config), lambda _event: None)
        organism = engine.organisms[0]
        genome = (
            Instruction(PhaseTwoOpcode.SENSE_RESOURCE, a=0),
            Instruction(Opcode.HALT),
        )
        organism.genome = genome
        organism.vm_state = engine._new_vm_state(genome)
        before = (organism.x, organism.y)
        engine.step()
        self.assertEqual((organism.x, organism.y), before)
        self.assertGreaterEqual(organism.vm_state.registers[0], 0)
        self.assertLessEqual(organism.vm_state.registers[0], 255)
        self.assertGreaterEqual(engine.metrics()["resource_sense_operations"], 1)

    def test_move_instruction_is_costed_bounded_and_observable(self) -> None:
        events: list[dict[str, object]] = []
        config = self._config()
        config.update(
            {
                "world.organism_actions_enabled": True,
                "world.movement_max_step": 1.0,
                "world.movement_cost_per_unit": 0.25,
            }
        )
        engine = PhaseTwoEngine(CORE_SCHEMA.validate(config), events.append)
        organism = engine.organisms[0]
        genome = (
            Instruction(PhaseTwoOpcode.MOVE_X, b=8),
            Instruction(Opcode.HALT),
        )
        organism.genome = genome
        organism.vm_state = engine._new_vm_state(genome)
        before_x = organism.x
        engine.step()
        self.assertLessEqual(abs(organism.x - before_x), 1.0 + 1e-12)
        metrics = engine.metrics()
        self.assertGreaterEqual(metrics["movement_operations"], 1)
        self.assertGreaterEqual(metrics["movement_distance"], 0.0)
        self.assertGreaterEqual(metrics["movement_energy_cost"], 0.0)
        self.assertTrue(any(event.get("name") == "organism_moved" for event in events))

    def test_reflective_and_toroidal_boundaries_are_independently_defined(self) -> None:
        self.assertEqual(apply_boundary(11.0, 10.0, "reflective")[0], 9.0)
        self.assertEqual(apply_boundary(11.0, 10.0, "toroidal")[0], 1.0)
        self.assertEqual(apply_boundary(-1.0, 10.0, "toroidal")[0], 9.0)

    def test_phase_two_matrix_contains_required_controls(self) -> None:
        required = {
            "homogeneous_control",
            "spatial_only",
            "local_resource",
            "movement_enabled",
            "resource_abundant",
            "resource_limited",
            "small_world",
            "large_world",
            "reflective_boundary",
            "toroidal_boundary",
            "movement_cost_zero",
            "movement_cost_high",
        }
        self.assertTrue(required.issubset(PHASE_TWO_CONDITIONS))

        base = self._config()
        base["run.max_ticks"] = 5
        campaign = run_phase_two_matrix(base, seeds=[1, 2])
        self.assertEqual(campaign["seed_count"], 2)
        self.assertEqual(campaign["runs_per_condition"], 2)
        self.assertEqual(
            len(campaign["runs"]),
            len(PHASE_TWO_CONDITIONS) * 2,
        )
        self.assertTrue(campaign["validation"]["passed"])

    def test_performance_probe_records_scale_limits_and_reproducibility(self) -> None:
        config = self._config()
        config["run.max_ticks"] = 10
        report = performance_probe(config)
        self.assertGreater(report["runtime_seconds"], 0.0)
        self.assertGreater(report["ticks_per_second"], 0.0)
        self.assertGreater(report["peak_tracemalloc_bytes"], 0)
        self.assertGreater(report["summary_json_bytes"], 0)
        self.assertTrue(report["deterministic_repeat"])


if __name__ == "__main__":
    unittest.main()
