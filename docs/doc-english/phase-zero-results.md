# Phase Zero Results

[فارسی](../doc-farsi/phase-zero-results.md) | [Documentation index](../README.md)

## Status

Phase Zero is implemented and validated as a constrained digital execution and reproduction experiment. It is a development validation milestone, not a claim that biological life has been recreated.

The executable backend is:

- Engine: <code>phase-zero-vm-0.2</code>
- Host implementation: <code>Python</code>
- Organism execution: data-only genomes interpreted by a bounded custom VM
- Interface: <code>PySide6</code> desktop application
- Reproducibility: seeded random execution

## What Phase Zero implements

Each active organism has:

- an instruction genome for its current lifecycle;
- finite registers and finite working memory;
- a bounded instruction budget per tick;
- internal energy;
- a position in a homogeneous world;
- a genealogy record;
- an execution state that can halt, fault, or request division.

The engine provides:

- sequential external energy input;
- energy capture and storage;
- computation and maintenance costs;
- reproduction cost and offspring energy transfer;
- finite structural memory allocation;
- blind opcode-substitution mutation;
- heredity, lineages, generations, and genome hashes;
- death by resource exhaustion or VM fault;
- release of remaining organism energy on death;
- serializable snapshots and metrics;
- an energy-balance ledger.

No organism can execute host Python, import modules, access files, use the network, create subprocesses, or call external APIs.

## Executable lifecycle

The default ancestor genome copies its own eight instructions through the VM:

1. initialize the copy counter;
2. initialize the genome index;
3. copy one instruction;
4. advance the index;
5. decrement the remaining counter;
6. jump to division when the counter reaches zero;
7. otherwise loop back to copying;
8. request division.

A successful division creates a child with a copied genome, optional opcode substitution, a new organism identifier, a parent identifier, a generation number, and a lineage assignment.

## Conservation and population invariants

For a run without immigration or emigration:

~~~text
final_population = initial_population + births - deaths
~~~

For the tested eight-instruction genome and eight memory cells per organism:

~~~text
memory_used = active_population × (memory_per_organism + genome_length)
~~~

The energy ledger checks that initial organism energy and environmental input, minus dissipative costs, equal the energy still stored in active organisms and the environment, within floating-point tolerance.

## GUI validation observations

The following observations were made from the desktop application.

### Resource-capacity run

Configuration included:

- maximum ticks: 1000;
- initial population: 12;
- memory capacity: 500;
- memory per organism: 8;
- default genome length: 8.

Observed final values:

~~~text
population = 31
births = 22
deaths = 3
memory_used = 496
instructions_executed = 2274
energy_balance_error ≈ 3.4e-09
~~~

The population and memory values satisfy:

~~~text
12 + 22 - 3 = 31
31 × (8 + 8) = 496
~~~

When the capacity was reached, active organisms could remain waiting at the division boundary because a new organism required 16 memory units while only 4 units were free. This is a documented Phase One design question, not evidence of fabricated metrics.

### Expanded-memory dynamic run

With memory capacity increased to 2000, the simulation continued to execute and population changed over the full 1000 ticks.

One observed run produced:

~~~text
initial_population = 12
population = 43
births = 214
deaths = 183
memory_used = 688
instructions_executed = 13180
faults = 8
energy_balance_error ≈ 4.6e-09
~~~

The invariants remained valid:

~~~text
12 + 214 - 183 = 43
43 × (8 + 8) = 688
~~~

### Paired mutation control

A paired GUI comparison used the same seed, run length, memory capacity, and visible execution and reproduction settings. The mutation rate was the controlled variable.

With substitution rate 0.01:

~~~text
population = 62
births = 170
deaths = 120
memory_used = 992
instructions_executed = 11663
faults = 8
active_genotypes = 3
energy_balance_error ≈ -6e-09
~~~

With substitution rate 0:

~~~text
population = 64
births = 148
deaths = 96
memory_used = 1024
instructions_executed = 10055
faults = 0
active_genotypes = 1
energy_balance_error ≈ -5e-09
~~~

The result supports the intended implementation relationship: nonzero blind mutation can create divergent surviving genotypes and invalid descendants, while removing mutation removes those mutation-induced faults in the paired control.

These observations are implementation evidence. They are not yet a statistical claim about natural selection in biological populations.

## Automated validation

The Phase Zero implementation is covered by tests for:

- finite word arithmetic;
- memory load and store;
- instruction budgets;
- invalid VM operands;
- self-copy and division requests;
- reproduction without a host-level magic reproduction instruction;
- mutation and heredity;
- energy and memory accounting;
- death and resource release;
- deterministic seeded execution;
- replicate aggregation;
- engine backend selection.

The development validation suite contained 19 tests, all passing at the Phase Zero merge point.

## Phase Zero acceptance statement

Phase Zero is accepted as a digital substrate milestone because it demonstrates:

- bounded execution;
- finite and measurable resources;
- self-copy reproduction;
- heritable variation;
- births and deaths;
- divergent lineages or genotypes under mutation;
- reproducible seeded runs;
- conservation checks;
- an observable desktop interface.

It is not accepted as a completed model of biological life. Spatial ecology, environmental heterogeneity, explicit disturbances, cooperation, parasites, learning, and intelligence objectives remain outside this phase.

## Open questions carried into Phase One

1. What should an organism do when replication is complete but memory for a child is unavailable?
2. Should a blocked division request be retried forever, abandoned, reset, or treated as a costly failure?
3. Which metrics should be persisted per tick rather than only summarized at the end?
4. How should historical genotypes and active genotypes be distinguished in the interface?
5. Which parameter ranges produce informative dynamics without hiding a deadlock behind abundant energy?
6. How many seeded replicates are required for each research claim?

Phase One addresses these questions through measurement, reproducibility, protocol design, and carefully gated rule changes.
