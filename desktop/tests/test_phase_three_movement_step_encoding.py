import random
import unittest

from melakat_desktop.parameters import CORE_SCHEMA
from melakat_desktop.phase_three_contract import (
    PHASE_THREE_ENGINE_VERSION,
    PHASE_THREE_MOVEMENT_ENCODING_ENGINE_VERSION,
)
from melakat_desktop.phase_three_engine import (
    PhaseThreeEngine,
    mutate_phase_three_genome,
)
from melakat_desktop.phase_two_vm import (
    PhaseTwoOpcode,
    mutate_phase_two_genome,
)
from melakat_desktop.phase_zero_engine import PhaseZeroEngine
from melakat_desktop.vm import Instruction


class PhaseThreeMovementStepEncodingTests(unittest.TestCase):
    @staticmethod
    def config(*, movement_step_rate: float = 0.0) -> dict:
        config = CORE_SCHEMA.defaults()
        config.update(
            {
                "run.engine_backend": "phase-three-vm",
                "run.seed": 19,
                "run.max_ticks": 20,
                "run.emit_snapshots": False,
                "world.spatial_enabled": True,
                "world.resource_distribution_mode": "uniform",
                "world.movement_enabled": False,
                "world.movement_mutation_enabled": True,
                "mutation.movement_step_rate": movement_step_rate,
            }
        )
        return CORE_SCHEMA.validate(config)

    def test_zero_step_rate_preserves_phase_two_mutation_exactly(self) -> None:
        genome = PhaseZeroEngine.default_genome()
        phase_two_rng = random.Random(12345)
        phase_three_rng = random.Random(12345)

        expected = mutate_phase_two_genome(
            genome,
            phase_two_rng,
            0.25,
            sensing_enabled=False,
            movement_enabled=True,
        )
        observed = mutate_phase_three_genome(
            genome,
            phase_three_rng,
            0.25,
            sensing_enabled=False,
            movement_enabled=True,
            movement_step_rate=0.0,
        )

        self.assertEqual(observed, expected)

    def test_unit_step_mutation_turns_zero_step_movement_nonzero(self) -> None:
        genome = (
            Instruction(PhaseTwoOpcode.MOVE_X, a=0, b=0),  # type: ignore[arg-type]
            Instruction(PhaseTwoOpcode.MOVE_Y, a=0, b=0),  # type: ignore[arg-type]
        )

        mutated = mutate_phase_three_genome(
            genome,
            random.Random(7),
            0.0,
            sensing_enabled=False,
            movement_enabled=True,
            movement_step_rate=1.0,
        )

        self.assertEqual(
            tuple(instruction.opcode for instruction in mutated),
            (PhaseTwoOpcode.MOVE_X, PhaseTwoOpcode.MOVE_Y),
        )
        self.assertTrue(all(instruction.b in {-1, 1} for instruction in mutated))

    def test_existing_unit_step_can_mutate_direction(self) -> None:
        genome = (
            Instruction(PhaseTwoOpcode.MOVE_X, a=0, b=1),  # type: ignore[arg-type]
        )
        mutated = mutate_phase_three_genome(
            genome,
            random.Random(11),
            0.0,
            sensing_enabled=False,
            movement_enabled=True,
            movement_step_rate=1.0,
        )
        self.assertEqual(mutated[0].b, -1)

    def test_engine_revision_changes_only_when_intervention_is_enabled(self) -> None:
        control = PhaseThreeEngine(self.config(movement_step_rate=0.0), lambda _event: None)
        intervention = PhaseThreeEngine(
            self.config(movement_step_rate=0.1),
            lambda _event: None,
        )

        self.assertEqual(control.engine_version, PHASE_THREE_ENGINE_VERSION)
        self.assertEqual(
            intervention.engine_version,
            PHASE_THREE_MOVEMENT_ENCODING_ENGINE_VERSION,
        )
        self.assertEqual(control.metrics()["movement_step_mutation_rate"], 0.0)
        self.assertEqual(intervention.metrics()["movement_step_mutation_rate"], 0.1)

    def test_intervention_requires_movement_mutation_alphabet(self) -> None:
        config = self.config(movement_step_rate=0.1)
        config["world.movement_mutation_enabled"] = False
        with self.assertRaisesRegex(
            ValueError,
            "movement_step_mutation_requires_movement_mutation",
        ):
            PhaseThreeEngine(config, lambda _event: None)

    def test_rate_must_be_bounded(self) -> None:
        config = self.config(movement_step_rate=0.0)
        config["mutation.movement_step_rate"] = 1.1
        with self.assertRaisesRegex(
            ValueError,
            "movement_step_rate must be between 0 and 1",
        ):
            PhaseThreeEngine(config, lambda _event: None)


if __name__ == "__main__":
    unittest.main()
