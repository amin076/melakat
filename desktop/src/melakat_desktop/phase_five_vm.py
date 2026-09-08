from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Literal

from .phase_five_contract import PHASE_FIVE_TEMPLATE_MAX_LENGTH
from .vm import Instruction, Opcode, VMConfig, VMState


class PhaseFiveOpcode(IntEnum):
    """Phase-Five-only evolvability primitives.

    Values are deliberately outside the frozen Phase Zero/Two opcode ranges.
    """

    NOP_A = 200
    NOP_B = 201
    COPY_NEXT = 202
    JUMP_TEMPLATE = 203
    JUMP_TEMPLATE_IF_ZERO = 204


TEMPLATE_OPCODES = {PhaseFiveOpcode.NOP_A, PhaseFiveOpcode.NOP_B}


@dataclass
class PhaseFiveVMState(VMState):
    replication_read_position: int = 0


@dataclass(frozen=True)
class PhaseFiveExecutionResult:
    status: Literal[
        "halted",
        "fault",
        "budget_exhausted",
        "division_requested",
    ]
    instructions_executed: int
    fault: str | None
    replication_copy_operations: int
    template_jump_operations: int


class PhaseFiveVirtualMachine:
    """Length-robust VM used only by the Phase Five backend.

    Phase Five does not alter the frozen VM. It introduces a sequential copy
    head and template-addressed jumps so the ancestral replication program does
    not encode its own length or absolute loop targets.
    """

    def __init__(
        self,
        program: tuple[Instruction, ...],
        config: VMConfig,
        state: PhaseFiveVMState | None = None,
    ) -> None:
        if not program:
            raise ValueError("phase_five_program_must_be_nonempty")
        self.program = program
        self.config = config
        self.state = state or PhaseFiveVMState(
            registers=[0] * config.register_count,
            memory=[0] * config.memory_size,
            replication_buffer=[],
        )
        if len(self.state.registers) != config.register_count:
            raise ValueError("state register count does not match VMConfig")
        if len(self.state.memory) != config.memory_size:
            raise ValueError("state memory size does not match VMConfig")
        if not 0 <= self.state.replication_read_position <= len(program):
            raise ValueError("invalid_replication_read_position")
        self.replication_copy_operations = 0
        self.template_jump_operations = 0

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
        self.state.replication_buffer = []
        self.state.replication_read_position = 0
        self.state.halted = False
        self.state.fault = None
        self.state.division_requested = False
        self.state.blocked_on_division = False
        self.state.instructions_executed = 0

    def replication_progress(self) -> int:
        return sum(item is not None for item in self.state.replication_buffer)

    def copied_genome(self) -> tuple[Instruction, ...] | None:
        if len(self.state.replication_buffer) != len(self.program):
            return None
        if any(item is None for item in self.state.replication_buffer):
            return None
        return tuple(item for item in self.state.replication_buffer if item is not None)

    def _ensure_buffer_index(self, index: int) -> None:
        while len(self.state.replication_buffer) <= index:
            self.state.replication_buffer.append(None)

    @staticmethod
    def _complement(template: tuple[PhaseFiveOpcode, ...]) -> tuple[PhaseFiveOpcode, ...]:
        return tuple(
            PhaseFiveOpcode.NOP_B
            if opcode is PhaseFiveOpcode.NOP_A
            else PhaseFiveOpcode.NOP_A
            for opcode in template
        )

    def _inline_template(
        self,
        jump_ip: int,
    ) -> tuple[tuple[PhaseFiveOpcode, ...], int]:
        index = jump_ip + 1
        template: list[PhaseFiveOpcode] = []
        while index < len(self.program):
            opcode = self.program[index].opcode
            if opcode not in TEMPLATE_OPCODES:
                break
            if len(template) >= PHASE_FIVE_TEMPLATE_MAX_LENGTH:
                raise ValueError("template_too_long")
            template.append(PhaseFiveOpcode(opcode))
            index += 1
        if not template:
            raise ValueError("template_missing")
        return tuple(template), index

    def _find_complementary_template(
        self,
        template: tuple[PhaseFiveOpcode, ...],
        *,
        search_start: int,
        excluded_start: int,
        excluded_end: int,
    ) -> int:
        target = self._complement(template)
        length = len(target)
        size = len(self.program)
        for offset in range(size):
            start = (search_start + offset) % size
            end = start + length
            # Templates themselves never wrap around the physical end of the
            # genome. Search order is circular, target matching is contiguous.
            if end > size:
                continue
            if start < excluded_end and end > excluded_start:
                continue
            candidate = tuple(self.program[index].opcode for index in range(start, end))
            if candidate == target:
                return end % size
        raise ValueError("complementary_template_not_found")

    def _template_jump(self, ip: int, *, conditional_zero: bool) -> int:
        template, after_inline = self._inline_template(ip)
        if conditional_zero:
            self._require_register(0)
            if self.state.registers[0] != 0:
                return after_inline
        destination = self._find_complementary_template(
            template,
            search_start=after_inline % len(self.program),
            excluded_start=ip + 1,
            excluded_end=after_inline,
        )
        self.template_jump_operations += 1
        return destination

    def _copy_next(self) -> None:
        self._require_register(0)
        source = self.state.replication_read_position
        if source >= len(self.program):
            self.state.registers[0] = 0
            return
        self._ensure_buffer_index(source)
        self.state.replication_buffer[source] = self.program[source]
        self.state.replication_read_position += 1
        self.replication_copy_operations += 1
        self.state.registers[0] = (
            0 if self.state.replication_read_position >= len(self.program) else 1
        )

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
        next_ip = ip + 1
        try:
            opcode = instruction.opcode
            if isinstance(opcode, PhaseFiveOpcode):
                if opcode in TEMPLATE_OPCODES:
                    pass
                elif opcode is PhaseFiveOpcode.COPY_NEXT:
                    self._copy_next()
                elif opcode is PhaseFiveOpcode.JUMP_TEMPLATE:
                    next_ip = self._template_jump(ip, conditional_zero=False)
                elif opcode is PhaseFiveOpcode.JUMP_TEMPLATE_IF_ZERO:
                    next_ip = self._template_jump(ip, conditional_zero=True)
                else:
                    raise ValueError(f"invalid_phase_five_opcode:{opcode}")
            elif not isinstance(opcode, Opcode):
                raise ValueError(f"invalid_opcode:{opcode}")
            elif opcode is Opcode.NOP:
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
                self._ensure_buffer_index(source)
                self.state.replication_buffer[source] = self.program[source]
            elif opcode is Opcode.DIVIDE:
                if self.copied_genome() is None:
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

    def run(self, instruction_budget: int) -> PhaseFiveExecutionResult:
        if instruction_budget < 1:
            raise ValueError("instruction_budget must be positive")
        start_count = self.state.instructions_executed
        start_copies = self.replication_copy_operations
        start_jumps = self.template_jump_operations
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
        return PhaseFiveExecutionResult(
            status=status,
            instructions_executed=executed,
            fault=self.state.fault,
            replication_copy_operations=self.replication_copy_operations - start_copies,
            template_jump_operations=self.template_jump_operations - start_jumps,
        )
