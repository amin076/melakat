import unittest

from melakat_desktop.phase_zero_engine import PhaseZeroEngine
from melakat_desktop.vm import (
    Instruction,
    Opcode,
    VMConfig,
    VirtualMachine,
)


class VirtualMachineTests(unittest.TestCase):
    def test_word_arithmetic_wraps_at_word_size(self) -> None:
        vm = VirtualMachine(
            (
                Instruction(Opcode.SET, a=0, b=255),
                Instruction(Opcode.INC, a=0),
                Instruction(Opcode.HALT),
            ),
            VMConfig(word_bits=8, register_count=2, memory_size=4),
        )

        result = vm.run(10)

        self.assertEqual(result.status, "halted")
        self.assertEqual(vm.state.registers[0], 0)

    def test_memory_store_and_load(self) -> None:
        vm = VirtualMachine(
            (
                Instruction(Opcode.SET, a=0, b=42),
                Instruction(Opcode.STORE, a=0, b=2),
                Instruction(Opcode.LOAD, a=1, b=2),
                Instruction(Opcode.HALT),
            ),
            VMConfig(register_count=2, memory_size=4),
        )

        result = vm.run(10)

        self.assertEqual(result.status, "halted")
        self.assertEqual(vm.state.memory[2], 42)
        self.assertEqual(vm.state.registers[1], 42)

    def test_instruction_budget_stops_an_infinite_loop(self) -> None:
        vm = VirtualMachine(
            (
                Instruction(Opcode.SET, a=0, b=1),
                Instruction(Opcode.JUMP, a=1),
            ),
            VMConfig(),
        )

        result = vm.run(5)

        self.assertEqual(result.status, "budget_exhausted")
        self.assertEqual(result.instructions_executed, 5)
        self.assertFalse(vm.state.halted)

    def test_invalid_register_becomes_a_fault(self) -> None:
        vm = VirtualMachine(
            (Instruction(Opcode.INC, a=99),),
            VMConfig(),
        )

        result = vm.run(5)

        self.assertEqual(result.status, "fault")
        self.assertEqual(result.fault, "invalid_register:99")

    def test_default_ancestor_copies_its_program(self) -> None:
        genome = PhaseZeroEngine.default_genome()
        vm = VirtualMachine(
            genome,
            VMConfig(register_count=4, memory_size=8),
        )

        result = vm.run(200)

        self.assertEqual(result.status, "division_requested")
        self.assertEqual(vm.state.replication_buffer, list(genome))
        self.assertEqual(vm.replication_progress(), len(genome))


if __name__ == "__main__":
    unittest.main()
