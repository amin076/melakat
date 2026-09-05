# Phase Zero VM — first execution substrate

This document records the first executable VM layer for Melakat. It is deliberately small. It is not a claim that the final digital-life rules have been decided.

## Current contract

Each organism owns:

- a data-only genome represented by a tuple of Instruction values;
- a finite set of integer registers;
- finite working memory;
- an instruction pointer;
- a halted or faulted state;
- a cumulative instruction counter.

The Python host interprets the genome through VirtualMachine. Organisms do not provide Python code, imports, filesystem access, network access, subprocess calls, or host-runtime calls.

## Instruction set in vm-0.1

| Instruction | Meaning |
| --- | --- |
| NOP | Do nothing |
| SET | Set register a to immediate value b |
| INC | Increment register a |
| DEC | Decrement register a |
| ADD | Add register b into register a |
| SUB | Subtract register b from register a |
| LOAD | Load memory address b into register a |
| STORE | Store register a into memory address b |
| JUMP | Jump to an instruction index |
| JUMP_IF_ZERO | Jump when register zero is zero |
| HALT | Stop this VM |

All arithmetic wraps at the configured finite word_bits. Every execution receives an instruction budget. Invalid addresses and registers become explicit VM faults.

## Engine boundary

PhaseZeroEngine adds:

- sequential external energy input;
- maintenance and instruction costs;
- finite population memory accounting;
- age and energy death;
- serializable snapshots and metrics.

It intentionally does not yet implement:

- reproduction;
- mutation;
- genome copying;
- environmental sensing;
- spatial interaction;
- a final biological interpretation of energy;
- scientific Experiment 0 claims.

Those rules must be specified, tested, and documented before they become part of the engine.

## Next implementation order

1. Connect PhaseZeroEngine to the existing worker through an explicit engine backend selector.
2. Add immutable genome records and serialization.
3. Specify reproduction and copying costs.
4. Add substitution mutation with deterministic seeded tests.
5. Add snapshot/replay tests.
6. Add an inspector for instruction pointer, registers, memory, and faults.
