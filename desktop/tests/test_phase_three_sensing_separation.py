import random
import unittest

from melakat_desktop.parameters import CORE_SCHEMA
from melakat_desktop.phase_two_engine import PhaseTwoEngine
from melakat_desktop.phase_two_vm import (
    PhaseTwoOpcode,
    PhaseTwoVirtualMachine,
    mutate_phase_two_genome,
)
from melakat_desktop.vm import Instruction, Opcode, VMConfig, VMState


class PhaseThreeSensingSeparationTests(unittest.TestCase):
    def test_new_switches_default_off(self) -> None:
        defaults = CORE_SCHEMA.defaults()
        self.assertFalse(defaults["world.resource_sensing_enabled"])
        self.assertFalse(defaults["world.resource_sensing_mutation_enabled"])
        self.assertFalse(defaults["world.movement_enabled"])
        self.assertFalse(defaults["world.movement_mutation_enabled"])
        self.assertFalse(defaults["world.organism_actions_enabled"])

    def test_sensing_only_mutation_excludes_movement(self) -> None:
        genome = tuple(Instruction(Opcode.NOP) for _ in range(64))
        seen = set()
        for seed in range(40):
            mutated = mutate_phase_two_genome(
                genome,
                random.Random(seed),
                1.0,
                sensing_enabled=True,
                movement_enabled=False,
            )
            seen.update(item.opcode for item in mutated)
        self.assertIn(PhaseTwoOpcode.SENSE_RESOURCE, seen)
        self.assertNotIn(PhaseTwoOpcode.MOVE_X, seen)
        self.assertNotIn(PhaseTwoOpcode.MOVE_Y, seen)

    def test_movement_only_mutation_excludes_sensing(self) -> None:
        genome = tuple(Instruction(Opcode.NOP) for _ in range(64))
        seen = set()
        for seed in range(40):
            mutated = mutate_phase_two_genome(
                genome,
                random.Random(seed),
                1.0,
                sensing_enabled=False,
                movement_enabled=True,
            )
            seen.update(item.opcode for item in mutated)
        self.assertNotIn(PhaseTwoOpcode.SENSE_RESOURCE, seen)
        self.assertTrue(
            PhaseTwoOpcode.MOVE_X in seen or PhaseTwoOpcode.MOVE_Y in seen
        )

    def test_sensing_only_vm_executes_sense_without_move(self) -> None:
        program = (
            Instruction(PhaseTwoOpcode.SENSE_RESOURCE, a=0),
            Instruction(PhaseTwoOpcode.MOVE_X, b=5),
            Instruction(Opcode.HALT),
        )
        config = VMConfig()
        state = VMState(
            registers=[0] * config.register_count,
            memory=[0] * config.memory_size,
            replication_buffer=[None] * len(program),
        )
        movement_calls = []
        vm = PhaseTwoVirtualMachine(
            program,
            config,
            state,
            sense_resource=lambda: 7.4,
            move=lambda axis, delta: movement_calls.append((axis, delta))
            or (abs(delta), 0),
            sensing_enabled=True,
            movement_enabled=False,
        )
        result = vm.run(3)
        self.assertEqual(vm.state.registers[0], 7)
        self.assertEqual(result.resource_sense_operations, 1)
        self.assertEqual(result.movement_operations, 0)
        self.assertEqual(result.movement_distance, 0.0)
        self.assertEqual(movement_calls, [])

    def test_engine_supports_sensing_without_movement(self) -> None:
        config = CORE_SCHEMA.validate(
            {
                "world.spatial_enabled": True,
                "world.resource_sensing_enabled": True,
                "world.movement_enabled": False,
                "world.organism_actions_enabled": False,
            }
        )
        engine = PhaseTwoEngine(config, lambda event: None)
        self.assertTrue(engine.resource_sensing_enabled)
        self.assertFalse(engine.movement_enabled)
        self.assertTrue(engine.organism_actions_enabled)
        metrics = engine.metrics()
        self.assertTrue(metrics["resource_sensing_enabled"])
        self.assertFalse(metrics["movement_enabled"])

    def test_movement_mutation_availability_without_execution(self) -> None:
        config = CORE_SCHEMA.validate({
            "world.spatial_enabled": True,
            "world.resource_sensing_enabled": False,
            "world.resource_sensing_mutation_enabled": False,
            "world.movement_enabled": False,
            "world.movement_mutation_enabled": True,
            "world.organism_actions_enabled": False,
        })
        engine = PhaseTwoEngine(config, lambda event: None)
        self.assertFalse(engine.movement_enabled)
        self.assertTrue(engine.movement_mutation_enabled)
        self.assertTrue(engine.phase_two_vm_enabled)

    def test_movement_execution_toggle_preserves_mutation_mapping(self) -> None:
        base = {
            "world.spatial_enabled": True,
            "world.resource_sensing_enabled": False,
            "world.resource_sensing_mutation_enabled": False,
            "world.movement_mutation_enabled": True,
            "world.organism_actions_enabled": False,
        }
        control_engine = PhaseTwoEngine(
            CORE_SCHEMA.validate({**base, "world.movement_enabled": False}),
            lambda event: None,
        )
        treatment_engine = PhaseTwoEngine(
            CORE_SCHEMA.validate({**base, "world.movement_enabled": True}),
            lambda event: None,
        )
        self.assertFalse(control_engine.movement_enabled)
        self.assertTrue(treatment_engine.movement_enabled)
        self.assertTrue(control_engine.movement_mutation_enabled)
        self.assertTrue(treatment_engine.movement_mutation_enabled)

        genome = (
            Instruction(Opcode.NOP),
            Instruction(Opcode.ADD, a=0, b=1),
            Instruction(Opcode.COPY, a=0, b=1),
            Instruction(Opcode.DIVIDE),
        )
        control_mutated = mutate_phase_two_genome(
            genome,
            random.Random(24680),
            0.65,
            sensing_enabled=control_engine.resource_sensing_mutation_enabled,
            movement_enabled=control_engine.movement_mutation_enabled,
        )
        treatment_mutated = mutate_phase_two_genome(
            genome,
            random.Random(24680),
            0.65,
            sensing_enabled=treatment_engine.resource_sensing_mutation_enabled,
            movement_enabled=treatment_engine.movement_mutation_enabled,
        )
        self.assertEqual(control_mutated, treatment_mutated)

    def test_movement_mutation_requires_spatial_world(self) -> None:
        config = CORE_SCHEMA.validate({
            "world.spatial_enabled": False,
            "world.movement_enabled": False,
            "world.movement_mutation_enabled": True,
            "world.organism_actions_enabled": False,
        })
        with self.assertRaisesRegex(ValueError, "movement_mutation_requires_spatial"):
            PhaseTwoEngine(config, lambda event: None)

    def test_legacy_combined_switch_preserves_old_behavior(self) -> None:
        config = CORE_SCHEMA.validate(
            {
                "world.spatial_enabled": True,
                "world.organism_actions_enabled": True,
            }
        )
        engine = PhaseTwoEngine(config, lambda event: None)
        self.assertTrue(engine.resource_sensing_enabled)
        self.assertTrue(engine.movement_enabled)
        self.assertTrue(engine.organism_actions_enabled)


    def test_sensing_execution_can_change_without_changing_mutation_alphabet(self) -> None:
        common = {
            "world.spatial_enabled": True,
            "world.resource_sensing_mutation_enabled": True,
            "world.movement_enabled": False,
            "world.organism_actions_enabled": False,
        }
        control = PhaseTwoEngine(
            CORE_SCHEMA.validate({**common, "world.resource_sensing_enabled": False}),
            lambda event: None,
        )
        treatment = PhaseTwoEngine(
            CORE_SCHEMA.validate({**common, "world.resource_sensing_enabled": True}),
            lambda event: None,
        )
        self.assertTrue(control.resource_sensing_mutation_enabled)
        self.assertTrue(treatment.resource_sensing_mutation_enabled)
        self.assertFalse(control.resource_sensing_enabled)
        self.assertTrue(treatment.resource_sensing_enabled)
        self.assertTrue(control.phase_two_vm_enabled)
        self.assertTrue(treatment.phase_two_vm_enabled)
        self.assertFalse(control.movement_enabled)
        self.assertFalse(treatment.movement_enabled)

        genome = tuple(Instruction(Opcode.NOP) for _ in range(64))
        a = mutate_phase_two_genome(
            genome,
            random.Random(12345),
            1.0,
            sensing_enabled=control.resource_sensing_mutation_enabled,
            movement_enabled=control.movement_enabled,
        )
        b = mutate_phase_two_genome(
            genome,
            random.Random(12345),
            1.0,
            sensing_enabled=treatment.resource_sensing_mutation_enabled,
            movement_enabled=treatment.movement_enabled,
        )
        self.assertEqual(a, b)

    def test_independent_switches_require_spatial_world(self) -> None:
        sensing = CORE_SCHEMA.validate(
            {"world.resource_sensing_enabled": True}
        )
        with self.assertRaisesRegex(
            ValueError, "resource_sensing_requires_spatial"
        ):
            PhaseTwoEngine(sensing, lambda event: None)

        movement = CORE_SCHEMA.validate(
            {"world.movement_enabled": True}
        )
        with self.assertRaisesRegex(ValueError, "movement_requires_spatial"):
            PhaseTwoEngine(movement, lambda event: None)

        mutation_only = CORE_SCHEMA.validate(
            {"world.resource_sensing_mutation_enabled": True}
        )
        with self.assertRaisesRegex(
            ValueError, "resource_sensing_mutation_requires_spatial"
        ):
            PhaseTwoEngine(mutation_only, lambda event: None)


if __name__ == "__main__":
    unittest.main()
