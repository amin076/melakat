import unittest

from melakat_desktop.parameters import CORE_SCHEMA
from melakat_desktop.phase_three_contract import (
    PHASE_THREE_ATOMIC_MOVEMENT_ENGINE_VERSION,
    PHASE_THREE_ATOMIC_MOVEMENT_MEASUREMENT_VERSION,
)
from melakat_desktop.phase_three_engine import PhaseThreeEngine
from melakat_desktop.phase_three_experiment_support import validate_phase_three_config
from melakat_desktop.phase_two_vm import PhaseTwoOpcode
from melakat_desktop.vm import Instruction


class PhaseThreeAtomicMovementPaymentTests(unittest.TestCase):
    @staticmethod
    def config() -> dict:
        config = CORE_SCHEMA.defaults()
        config.update(
            {
                "run.engine_backend": "phase-three-vm",
                "run.seed": 7,
                "run.max_ticks": 10,
                "run.emit_snapshots": False,
                "world.spatial_enabled": True,
                "world.local_resources_enabled": False,
                "world.resource_distribution_mode": "uniform",
                "world.movement_enabled": True,
                "world.movement_mutation_enabled": True,
                "world.atomic_movement_payment_enabled": True,
                "mutation.movement_step_rate": 0.5,
                "population.initial_size": 1,
                "execution.instructions_per_tick": 1,
                "execution.maintenance_cost": 0.0,
                "execution.instruction_cost": 2.0,
                "world.movement_cost_per_unit": 0.1,
                "reproduction.enabled": False,
            }
        )
        return CORE_SCHEMA.validate(config)

    @staticmethod
    def install_single_move(engine: PhaseThreeEngine, *, energy: float):
        organism = engine.organisms[0]
        genome = (
            Instruction(PhaseTwoOpcode.MOVE_X, a=0, b=1),  # type: ignore[arg-type]
        )
        organism.genome = genome
        organism.vm_state = engine._new_vm_state(genome)
        organism.x = 10.0
        organism.y = 10.0
        organism.energy = energy
        engine.energy_pool = 0.0
        return organism

    def test_atomic_intervention_has_distinct_engine_and_measurement_versions(self) -> None:
        engine = PhaseThreeEngine(self.config(), lambda _event: None)
        self.assertEqual(
            engine.engine_version,
            PHASE_THREE_ATOMIC_MOVEMENT_ENGINE_VERSION,
        )
        self.assertEqual(
            engine.measurement_version,
            PHASE_THREE_ATOMIC_MOVEMENT_MEASUREMENT_VERSION,
        )
        self.assertTrue(engine.metrics()["atomic_movement_payment_enabled"])

    def test_execution_energy_failure_cannot_commit_staged_movement(self) -> None:
        events: list[dict] = []
        engine = PhaseThreeEngine(self.config(), events.append)
        organism = self.install_single_move(engine, energy=1.5)

        engine._execute_one(organism)

        self.assertFalse(organism.alive)
        self.assertEqual(organism.death_reason, "energy_exhausted_execution")
        self.assertEqual((organism.x, organism.y), (10.0, 10.0))
        self.assertEqual(engine.movement_operations, 0)
        self.assertEqual(engine.movement_nonzero_operations, 0)
        self.assertEqual(engine.movement_distance, 0.0)
        self.assertEqual(engine.ledger["energy_movement"], 0.0)
        self.assertEqual(engine.movement_uncommitted_operations, 1)
        self.assertEqual(engine.movement_uncommitted_nonzero_operations, 1)
        self.assertEqual(engine.movement_uncommitted_distance, 1.0)
        self.assertEqual(engine.movement_uncommitted_execution_energy_batches, 1)
        self.assertFalse(
            any(event.get("type") == "organism_moved" for event in events)
        )

    def test_movement_energy_failure_cannot_commit_staged_movement(self) -> None:
        events: list[dict] = []
        engine = PhaseThreeEngine(self.config(), events.append)
        organism = self.install_single_move(engine, energy=2.05)

        engine._execute_one(organism)

        self.assertFalse(organism.alive)
        self.assertEqual(organism.death_reason, "energy_exhausted_movement")
        self.assertEqual((organism.x, organism.y), (10.0, 10.0))
        self.assertEqual(engine.movement_operations, 0)
        self.assertEqual(engine.movement_nonzero_operations, 0)
        self.assertEqual(engine.movement_distance, 0.0)
        self.assertAlmostEqual(engine.ledger["energy_execution"], 2.0)
        self.assertAlmostEqual(engine.ledger["energy_movement"], 0.05)
        self.assertEqual(engine.movement_uncommitted_operations, 1)
        self.assertEqual(engine.movement_uncommitted_movement_energy_batches, 1)
        self.assertFalse(
            any(event.get("type") == "organism_moved" for event in events)
        )

    def test_fully_paid_movement_commits_position_counters_and_event(self) -> None:
        events: list[dict] = []
        engine = PhaseThreeEngine(self.config(), events.append)
        organism = self.install_single_move(engine, energy=3.0)

        engine._execute_one(organism)

        self.assertTrue(organism.alive)
        self.assertEqual((organism.x, organism.y), (11.0, 10.0))
        self.assertEqual(engine.movement_operations, 1)
        self.assertEqual(engine.movement_nonzero_operations, 1)
        self.assertEqual(engine.movement_zero_step_operations, 0)
        self.assertEqual(engine.movement_distance, 1.0)
        self.assertAlmostEqual(engine.ledger["energy_execution"], 2.0)
        self.assertAlmostEqual(engine.ledger["energy_movement"], 0.1)
        moved = [event for event in events if event.get("type") == "organism_moved"]
        self.assertEqual(len(moved), 1)
        self.assertEqual(moved[0]["from_x"], 10.0)
        self.assertEqual(moved[0]["x"], 11.0)
        self.assertEqual(engine.movement_uncommitted_operations, 0)

    def test_atomic_flag_is_phase_three_scoped_and_type_checked(self) -> None:
        config = self.config()
        config["world.atomic_movement_payment_enabled"] = "yes"
        with self.assertRaisesRegex(
            ValueError,
            "atomic_movement_payment_enabled_must_be_boolean",
        ):
            validate_phase_three_config(config)

    def test_atomic_flag_requires_spatial_movement_availability(self) -> None:
        config = self.config()
        config["world.spatial_enabled"] = False
        with self.assertRaisesRegex(
            ValueError,
            "atomic_movement_payment_requires_spatial",
        ):
            validate_phase_three_config(config)

        config = self.config()
        config["world.movement_enabled"] = False
        config["world.movement_mutation_enabled"] = False
        config["mutation.movement_step_rate"] = 0.0
        with self.assertRaisesRegex(
            ValueError,
            "atomic_movement_payment_requires_movement",
        ):
            validate_phase_three_config(config)


if __name__ == "__main__":
    unittest.main()
