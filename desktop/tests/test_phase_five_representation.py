from __future__ import annotations

import unittest

from melakat_desktop.parameters import CORE_SCHEMA
from melakat_desktop.phase_five_engine import PhaseFiveEngine
from melakat_desktop.phase_five_vm import PhaseFiveVirtualMachine
from melakat_desktop.vm import Instruction, Opcode, VMConfig


class PhaseFiveRepresentationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.vm_config = VMConfig(word_bits=8, register_count=4, memory_size=8)

    def _run_to_division(self, genome: tuple[Instruction, ...]) -> PhaseFiveVirtualMachine:
        vm = PhaseFiveVirtualMachine(genome, self.vm_config)
        result = vm.run(2000)
        self.assertEqual(result.status, "division_requested", result.fault)
        self.assertIsNone(result.fault)
        self.assertEqual(result.replication_copy_operations, len(genome))
        self.assertEqual(vm.replication_progress(), len(genome))
        self.assertEqual(vm.copied_genome(), genome)
        return vm

    def test_default_ancestor_copies_current_length_without_literal(self) -> None:
        genome = PhaseFiveEngine.default_genome()
        vm = self._run_to_division(genome)
        self.assertEqual(vm.state.replication_read_position, len(genome))

    def test_neutral_insertion_does_not_break_replication_by_address_shift(self) -> None:
        genome = list(PhaseFiveEngine.default_genome())
        genome.insert(3, Instruction(Opcode.NOP))
        self._run_to_division(tuple(genome))

    def test_neutral_deletion_does_not_break_replication_by_address_shift(self) -> None:
        genome = list(PhaseFiveEngine.default_genome())
        del genome[2]
        self._run_to_division(tuple(genome))

    def test_two_different_lengths_use_same_replication_logic(self) -> None:
        ancestor = PhaseFiveEngine.default_genome()
        longer = tuple((*ancestor[:3], Instruction(Opcode.NOP), Instruction(Opcode.NOP), *ancestor[3:]))
        self._run_to_division(ancestor)
        self._run_to_division(longer)
        self.assertNotEqual(len(ancestor), len(longer))

    def test_divide_rejects_incomplete_copy(self) -> None:
        genome = (Instruction(Opcode.DIVIDE),)
        vm = PhaseFiveVirtualMachine(genome, self.vm_config)
        result = vm.run(1)
        self.assertEqual(result.status, "fault")
        self.assertEqual(result.fault, "division_without_complete_copy")

    def test_engine_replicates_for_multiple_generations(self) -> None:
        config = CORE_SCHEMA.defaults()
        config.update(
            {
                "run.max_ticks": 500,
                "run.seed": 5,
                "population.initial_size": 4,
                "world.memory_capacity": 500,
                "world.initial_energy": 1000.0,
                "world.energy_input_per_tick": 10.0,
                "mutation.substitution_rate": 0.0,
                "execution.instructions_per_tick": 8,
            }
        )
        engine = PhaseFiveEngine(config, lambda _event: None)
        while not engine.finished:
            engine.step()
        summary = engine.summary()
        self.assertGreater(summary["births"], 0)
        self.assertGreaterEqual(summary["max_generation"], 2)
        self.assertEqual(summary["faults"], 0)
        self.assertLessEqual(abs(summary["energy_balance_error"]), 1e-7)
        self.assertEqual(summary["distinct_genome_lengths"], 1)
        self.assertEqual(summary["genome_length_minimum"], len(PhaseFiveEngine.default_genome()))
        self.assertGreater(summary["replication_copy_operations"], 0)

    def test_deterministic_engine_replay(self) -> None:
        config = CORE_SCHEMA.defaults()
        config.update(
            {
                "run.max_ticks": 200,
                "run.seed": 17,
                "population.initial_size": 3,
                "mutation.substitution_rate": 0.0,
            }
        )
        first = PhaseFiveEngine(config, lambda _event: None)
        second = PhaseFiveEngine(config, lambda _event: None)
        while not first.finished:
            first.step()
        while not second.finished:
            second.step()
        self.assertEqual(first.summary(), second.summary())


if __name__ == "__main__":
    unittest.main()
