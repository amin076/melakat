from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Literal


class Opcode(IntEnum):
    NOP = 0
    SET = 1
    INC = 2
    DEC = 3
    ADD = 4
    SUB = 5
    LOAD = 6
    STORE = 7
    COPY = 8
    DIVIDE = 9
    JUMP = 10
    JUMP_IF_ZERO = 11
    HALT = 12


@dataclass(frozen=True)
class Instruction:
    opcode: Opcode
    a: int = 0
    b: int = 0


@dataclass(frozen=True)
class VMConfig:
    word_bits: int = 8
    register_count: int = 4
    memory_size: int = 8

    def __post_init__(self) -> None:
        if not 1 <= self.word_bits <= 32:
            raise ValueError("word_bits must be between 1 and 32")
        if not 1 <= self.register_count <= 64:
            raise ValueError("register_count must be between 1 and 64")
        if self.memory_size < 1:
            raise ValueError("memory_size must be positive")


@dataclass
class VMState:
    instruction_pointer: int = 0
    registers: list[int] = field(default_factory=list)
    memory: list[int] = field(default_factory=list)
    replication_buffer: list[Instruction | None] = field(default_factory=list)
    halted: bool = False
    fault: str | None = None
    division_requested: bool = False
    blocked_on_division: bool = False
    instructions_executed: int = 0


@dataclass(frozen=True)
class ExecutionResult:
    status: Literal[
        "halted",
        "fault",
        "budget_exhausted",
        "division_requested",
    ]
    instructions_executed: int
    fault: str | None


class VirtualMachine:
    """Bounded interpreter for data-only Phase Zero genomes."""

    def __init__(
        self,
        program: tuple[Instruction, ...],
        config: VMConfig,
        state: VMState | None = None,
    ) -> None:
        self.program = program
        self.config = config
        self.state = state or VMState(
            registers=[0] * config.register_count,
            memory=[0] * config.memory_size,
            replication_buffer=[None] * len(program),
        )
        if len(self.state.registers) != config.register_count:
            raise ValueError("state register count does not match VMConfig")
        if len(self.state.memory) != config.memory_size:
            raise ValueError("state memory size does not match VMConfig")
        if len(self.state.replication_buffer) != len(program):
            raise ValueError("replication buffer size does not match program")

    @property
    def modulus(self) -> int:
        return 1 << self.config.word_bits

    def _wrap(self, value: int) -> int:
        return value % self.modulus

    def _require_register(self, index: int) -> None:
        if not 0 <= index < self.config.register_count:
            raise ValueError(f"invalid_register:{index}")

    def _require_memory_address(self, address: int) -> None:
        if not 0 <= address < self.config.memory_size:
            raise ValueError(f"invalid_memory_address:{address}")

    def _require_program_address(self, address: int) -> None:
        if not 0 <= address < len(self.program):
            raise ValueError(f"invalid_program_address:{address}")

    def _fault(self, message: str) -> None:
        self.state.fault = message

    def reset_for_next_lifecycle(self) -> None:
        self.state.instruction_pointer = 0
        self.state.registers = [0] * self.config.register_count
        self.state.memory = [0] * self.config.memory_size
        self.state.replication_buffer = [None] * len(self.program)
        self.state.halted = False
        self.state.fault = None
        self.state.division_requested = False
        self.state.blocked_on_division = False
        self.state.instructions_executed = 0

    def replication_progress(self) -> int:
        return sum(item is not None for item in self.state.replication_buffer)

    def step(self) -> bool:
        if (
            self.state.halted
            or self.state.fault is not None
            or self.state.blocked_on_division
        ):
            return False

        ip = self.state.instruction_pointer
        if not 0 <= ip < len(self.program):
            self._fault(f"instruction_pointer_out_of_bounds:{ip}")
            return False

        instruction = self.program[ip]
        if not isinstance(instruction.opcode, Opcode):
            self._fault(f"invalid_opcode:{instruction.opcode}")
            return False

        next_ip = ip + 1

        try:
            opcode = instruction.opcode
            if opcode is Opcode.NOP:
                pass
            elif opcode is Opcode.SET:
                self._require_register(instruction.a)
                self.state.registers[instruction.a] = self._wrap(instruction.b)
            elif opcode is Opcode.INC:
                self._require_register(instruction.a)
                self.state.registers[instruction.a] = self._wrap(
                    self.state.registers[instruction.a] + 1
                )
            elif opcode is Opcode.DEC:
                self._require_register(instruction.a)
                self.state.registers[instruction.a] = self._wrap(
                    self.state.registers[instruction.a] - 1
                )
            elif opcode is Opcode.ADD:
                self._require_register(instruction.a)
                self._require_register(instruction.b)
                self.state.registers[instruction.a] = self._wrap(
                    self.state.registers[instruction.a]
                    + self.state.registers[instruction.b]
                )
            elif opcode is Opcode.SUB:
                self._require_register(instruction.a)
                self._require_register(instruction.b)
                self.state.registers[instruction.a] = self._wrap(
                    self.state.registers[instruction.a]
                    - self.state.registers[instruction.b]
                )
            elif opcode is Opcode.LOAD:
                self._require_register(instruction.a)
                self._require_memory_address(instruction.b)
                self.state.registers[instruction.a] = self.state.memory[instruction.b]
            elif opcode is Opcode.STORE:
                self._require_register(instruction.a)
                self._require_memory_address(instruction.b)
                self.state.memory[instruction.b] = self._wrap(
                    self.state.registers[instruction.a]
                )
            elif opcode is Opcode.COPY:
                self._require_register(1)
                source = self.state.registers[1]
                self._require_program_address(source)
                self.state.replication_buffer[source] = self.program[source]
            elif opcode is Opcode.DIVIDE:
                if self.replication_progress() != len(self.program):
                    raise ValueError("division_without_complete_copy")
                self.state.division_requested = True
                self.state.blocked_on_division = True
            elif opcode is Opcode.JUMP:
                self._require_program_address(instruction.a)
                next_ip = instruction.a
            elif opcode is Opcode.JUMP_IF_ZERO:
                self._require_register(0)
                if self.state.registers[0] == 0:
                    self._require_program_address(instruction.a)
                    next_ip = instruction.a
            elif opcode is Opcode.HALT:
                self.state.halted = True

        except ValueError as exc:
            self._fault(str(exc))
            return False

        self.state.instructions_executed += 1
        self.state.instruction_pointer = next_ip
        return True

    def run(self, instruction_budget: int) -> ExecutionResult:
        if instruction_budget < 1:
            raise ValueError("instruction_budget must be positive")

        start_count = self.state.instructions_executed
        while (
            self.state.instructions_executed - start_count < instruction_budget
            and not self.state.halted
            and self.state.fault is None
            and not self.state.blocked_on_division
        ):
            if not self.step():
                break

        executed = self.state.instructions_executed - start_count
        if self.state.fault is not None:
            status: Literal[
                "halted",
                "fault",
                "budget_exhausted",
                "division_requested",
            ] = "fault"
        elif self.state.division_requested:
            status = "division_requested"
        elif self.state.halted:
            status = "halted"
        else:
            status = "budget_exhausted"
        return ExecutionResult(status, executed, self.state.fault)


def instruction_record(instruction: Instruction) -> dict[str, int | str]:
    return {
        "opcode": instruction.opcode.name,
        "a": instruction.a,
        "b": instruction.b,
    }


def program_records(program: tuple[Instruction, ...]) -> list[dict[str, int | str]]:
    return [instruction_record(instruction) for instruction in program]
