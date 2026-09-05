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
    JUMP = 8
    JUMP_IF_ZERO = 9
    HALT = 10


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
    halted: bool = False
    fault: str | None = None
    instructions_executed: int = 0


@dataclass(frozen=True)
class ExecutionResult:
    status: Literal["halted", "fault", "budget_exhausted"]
    instructions_executed: int
    fault: str | None


class VirtualMachine:
    """Small bounded VM for Phase Zero experiments.

    Organisms provide data-only programs. Python code is never part of a
    program; this interpreter executes only the explicit Instruction values.
    """

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
        )
        if len(self.state.registers) != config.register_count:
            raise ValueError("state register count does not match VMConfig")
        if len(self.state.memory) != config.memory_size:
            raise ValueError("state memory size does not match VMConfig")

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

    def _fault(self, message: str) -> None:
        self.state.fault = message

    def step(self) -> bool:
        if self.state.halted or self.state.fault is not None:
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
        jumped = False

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
            elif opcode is Opcode.JUMP:
                if not 0 <= instruction.a < len(self.program):
                    raise ValueError(f"invalid_jump_target:{instruction.a}")
                next_ip = instruction.a
                jumped = True
            elif opcode is Opcode.JUMP_IF_ZERO:
                self._require_register(0)
                if self.state.registers[0] == 0:
                    if not 0 <= instruction.a < len(self.program):
                        raise ValueError(f"invalid_jump_target:{instruction.a}")
                    next_ip = instruction.a
                    jumped = True
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
        ):
            if not self.step():
                break

        executed = self.state.instructions_executed - start_count
        if self.state.fault is not None:
            status: Literal["halted", "fault", "budget_exhausted"] = "fault"
        elif self.state.halted:
            status = "halted"
        else:
            status = "budget_exhausted"
        return ExecutionResult(status, executed, self.state.fault)
