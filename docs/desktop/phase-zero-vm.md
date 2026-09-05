# Phase Zero VM Contract

[فارسی](phase-zero-vm.fa.md) | [Documentation index](../README.md)

This document defines the executable virtual-machine and engine contract used by the current Phase Zero backend.

## Safety boundary

The VM interprets data-only instruction records. Organisms cannot provide Python source, import modules, access the host filesystem or network, create subprocesses, or call host APIs.

The Python process is the simulator and interpreter. It is not part of the organism genome.

## VM state

Each organism VM has:

- a finite instruction pointer;
- a finite register set;
- finite word arithmetic;
- finite working memory;
- a replication buffer;
- halted, faulted, division-requested, and blocked-on-division state;
- an instruction counter.

Every tick has a bounded instruction budget. Invalid registers, addresses, and program jumps become explicit VM faults.

## Opcode contract

| Opcode | Meaning |
| --- | --- |
| <code>NOP</code> | Do nothing |
| <code>SET</code> | Set register <code>a</code> to immediate value <code>b</code> |
| <code>INC</code> | Increment register <code>a</code> |
| <code>DEC</code> | Decrement register <code>a</code> |
| <code>ADD</code> | Add register <code>b</code> into register <code>a</code> |
| <code>SUB</code> | Subtract register <code>b</code> from register <code>a</code> |
| <code>LOAD</code> | Load memory address <code>b</code> into register <code>a</code> |
| <code>STORE</code> | Store register <code>a</code> into memory address <code>b</code> |
| <code>COPY</code> | Copy the program instruction selected by register 1 |
| <code>DIVIDE</code> | Request division after the replication buffer is complete |
| <code>JUMP</code> | Jump to an instruction index |
| <code>JUMP_IF_ZERO</code> | Jump when register zero is zero |
| <code>HALT</code> | Stop this VM |

Arithmetic wraps at the configured finite word size.

## Default ancestor

The default eight-instruction ancestor is a minimal self-copying program. It uses register zero as a countdown and register one as the instruction index.

It does not invoke a special host-level reproduction function. It copies instructions through the VM and reaches the <code>DIVIDE</code> opcode only after the replication buffer is complete.

## Engine rules around the VM

The Phase Zero engine adds:

- sequential environmental energy input;
- per-organism energy capture;
- instruction and maintenance costs;
- reproduction cost;
- offspring initial energy;
- finite structural allocation for working memory and genome;
- blind opcode-substitution mutation;
- heredity and lineage tracking;
- death on energy exhaustion or VM fault;
- release of organism energy on death;
- genealogy and conservation metrics.

The baseline world is homogeneous and well mixed. It has no spatial interaction, fixed lifespan rule, explicit fitness function, learning, machine learning, attack, cooperation, or injected parasite.

## Observed validation

The GUI validation reached 1000 ticks with dynamic births, deaths, continued instruction execution, and near-zero energy-balance error when memory capacity was increased to 2000.

The paired mutation control produced:

- faults and three active genotypes with substitution rate 0.01;
- zero faults and one active genotype with substitution rate 0.

The results satisfy population and memory invariants documented in the Phase Zero results document.

## Known boundary

At memory capacity 500, the default allocation is:

~~~text
memory_per_organism + genome_length = 8 + 8 = 16
~~~

The maximum active population is therefore 31, leaving 4 unused units. A completed replicator can wait at <code>DIVIDE</code> while insufficient memory remains for a child.

This behavior is observable and reproducible. Phase One must define whether the pending division is retried, reset, charged, queued, or converted into another explicit rule.

## Testing contract

The VM and engine tests cover:

- finite arithmetic;
- memory operations;
- instruction budgets;
- invalid operands;
- self-copy and division;
- reproduction;
- mutation and heredity;
- energy and memory accounting;
- death and resource release;
- deterministic seeded execution.

Any opcode or lifecycle change must update the tests, the English document, and the matching Farsi document.
