from __future__ import annotations

import random
from dataclasses import dataclass
from enum import IntEnum
from typing import Callable, Literal

from .vm import Instruction, Opcode, VMConfig, VMState, VirtualMachine


class PhaseTwoOpcode(IntEnum):
    SENSE_RESOURCE = 100
    MOVE_X = 101
    MOVE_Y = 102


@dataclass(frozen=True)
class PhaseTwoExecutionResult:
    status: Literal[
        "halted",
        "fault",
        "budget_exhausted",
        "division_requested",
    ]
    instructions_executed: int
    fault: str | None
    resource_sense_operations: int
    movement_operations: int
    movement_nonzero_operations: int
    movement_zero_step_operations: int
    movement_distance: float
    boundary_contacts: int


def mutate_phase_two_genome(
    genome: tuple[Instruction, ...],
    rng: random.Random,
    rate: float,
    *,
    sensing_enabled: bool = True,
    movement_enabled: bool = True,
) -> tuple[Instruction, ...]:
    """Blind substitution across the Phase Zero + Phase Two opcode alphabets.

    This function is used only when Phase Two organism actions are explicitly
    enabled. The frozen Phase One engine continues to use its historical
    ``mutate_genome`` implementation and opcode set.
    """

    result: list[Instruction] = []
    opcodes: list[IntEnum] = [*list(Opcode)]
    if sensing_enabled:
        opcodes.append(PhaseTwoOpcode.SENSE_RESOURCE)
    if movement_enabled:
        opcodes.extend((PhaseTwoOpcode.MOVE_X, PhaseTwoOpcode.MOVE_Y))
    for instruction in genome:
        if rng.random() < rate:
            alternatives = [opcode for opcode in opcodes if opcode != instruction.opcode]
            instruction = Instruction(
                opcode=rng.choice(alternatives),  # type: ignore[arg-type]
                a=instruction.a,
                b=instruction.b,
            )
        result.append(instruction)
    return tuple(result)


class PhaseTwoVirtualMachine:
    """Environment-aware extension that leaves the Phase Zero VM untouched."""

    def __init__(
        self,
        program: tuple[Instruction, ...],
        config: VMConfig,
        state: VMState,
        *,
        sense_resource: Callable[[], float],
        move: Callable[[str, float], tuple[float, int]],
        sensing_enabled: bool = True,
        movement_enabled: bool = True,
    ) -> None:
        self.program = program
        self.config = config
        self.state = state
        self.sense_resource = sense_resource
        self.move = move
        self.sensing_enabled = bool(sensing_enabled)
        self.movement_enabled = bool(movement_enabled)
        self.resource_sense_operations = 0
        self.movement_operations = 0
        self.movement_nonzero_operations = 0
        self.movement_zero_step_operations = 0
        self.movement_distance = 0.0
        self.boundary_contacts = 0

    @property
    def modulus(self) -> int:
        return 1 << self.config.word_bits

    def _require_register(self, index: int) -> None:
        if not 0 <= index < self.config.register_count:
            raise ValueError(f"invalid_register:{index}")

    def _signed_immediate(self, value: int) -> int:
        wrapped = int(value) % self.modulus
        midpoint = self.modulus // 2
        return wrapped - self.modulus if wrapped >= midpoint else wrapped

    def step(self) -> bool:
        if self.state.halted or self.state.fault is not None or self.state.blocked_on_division:
            return False
        ip = self.state.instruction_pointer
        if not 0 <= ip < len(self.program):
            self.state.fault = f"instruction_pointer_out_of_bounds:{ip}"
            return False

        instruction = self.program[ip]
        if isinstance(instruction.opcode, PhaseTwoOpcode):
            try:
                if instruction.opcode is PhaseTwoOpcode.SENSE_RESOURCE:
                    if self.sensing_enabled:
                        self._require_register(instruction.a)
                        sensed = max(0.0, float(self.sense_resource()))
                        quantized = min(self.modulus - 1, int(round(sensed)))
                        self.state.registers[instruction.a] = quantized
                        self.resource_sense_operations += 1
                elif instruction.opcode in {
                    PhaseTwoOpcode.MOVE_X,
                    PhaseTwoOpcode.MOVE_Y,
                }:
                    if self.movement_enabled:
                        axis = "x" if instruction.opcode is PhaseTwoOpcode.MOVE_X else "y"
                        requested = float(self._signed_immediate(instruction.b))
                        distance, contacts = self.move(axis, requested)
                        realized_distance = max(0.0, float(distance))
                        self.movement_operations += 1
                        if realized_distance > 0.0:
                            self.movement_nonzero_operations += 1
                        else:
                            self.movement_zero_step_operations += 1
                        self.movement_distance += realized_distance
                        self.boundary_contacts += max(0, int(contacts))
            except ValueError as exc:
                self.state.fault = str(exc)
                return False
            self.state.instructions_executed += 1
            self.state.instruction_pointer = ip + 1
            return True

        # Base instructions retain the exact Phase Zero semantics.
        base_vm = VirtualMachine(self.program, self.config, self.state)
        return base_vm.step()

    def run(self, instruction_budget: int) -> PhaseTwoExecutionResult:
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
            status = "fault"
        elif self.state.division_requested:
            status = "division_requested"
        elif self.state.halted:
            status = "halted"
        else:
            status = "budget_exhausted"
        return PhaseTwoExecutionResult(
            status=status,  # type: ignore[arg-type]
            instructions_executed=executed,
            fault=self.state.fault,
            resource_sense_operations=self.resource_sense_operations,
            movement_operations=self.movement_operations,
            movement_nonzero_operations=self.movement_nonzero_operations,
            movement_zero_step_operations=self.movement_zero_step_operations,
            movement_distance=self.movement_distance,
            boundary_contacts=self.boundary_contacts,
        )
