# Phase Five — Genome Evolvability Without a Complexity Reward

## Status

**Design-only scientific contract. No Phase Five engine code is authorized by this document yet.**

Phase Four is closed. Phase Five begins a new causal question: can genome length itself become a heritable, evolvable state variable without the host rewarding long genomes, assigning a fitness score, or prescribing a target complexity?

The first Phase Five implementation must be a new opt-in backend. Frozen Phase Zero–Four engines, experiment specifications and accepted evidence must remain reproducible and unchanged.

## Scientific question

> Can Melakat remove its current fixed-length representational bottleneck so that blind structural mutations can create shorter and longer self-replicating genomes whose fate is determined only by the existing computational world constraints?

A positive Phase Five result would establish **heritable variable genome length and structural evolvability**. It would not establish increasing complexity, adaptation, intelligence, open-ended evolution, or biological equivalence.

## Why simple indels cannot be added directly to the current VM

The current representation contains two artificial length locks.

1. The ancestral copy loop hard-codes the genome length (`SET R0, 8`). A child whose length changes will inherit a copy loop that still attempts the old count.
2. Control flow uses absolute jump addresses. An insertion or deletion can shift code while leaving jump operands unchanged, breaking otherwise unrelated flow control.

A third limitation amplifies this brittleness: ordinary blind substitution changes opcodes but preserves the instruction operands, so a length mutation cannot normally repair the hard-coded copy count or shifted absolute jump targets.

Therefore, enabling insertion/deletion on the current representation would mostly test catastrophic representation brittleness, not evolvability.

This design lesson is consistent with classic digital-evolution systems. Tierra deliberately used template-based indirect addressing, and Avida uses template/head-based addressing specifically so insertions and deletions do not automatically invalidate absolute code positions. Avida and Aevol both support length-changing mutation operators, but they do so in representations designed to tolerate genome-size changes.

## Phase Five design principles

1. **No complexity reward.** No term may reward genome length, instruction count, novelty, diversity, or a human-defined task.
2. **No host-written strategy.** The host provides only substrate-level replication and addressing affordances.
3. **Existing costs remain real.** Longer genomes consume more world memory and require more copying/execution. No extra anti-growth penalty is required merely because a genome is longer.
4. **Genome length is not complexity.** Length is measured as a structural state variable only.
5. **One new causal mechanism at a time.** Robust representation comes before structural mutation; single-instruction events come before segment-scale rearrangements.
6. **Frozen backends stay frozen.** Phase Five behavior lives in a separate engine/VM contract.
7. **Determinism and accounting remain first-class.** Structural mutation must be reproducible, auditable and compatible with energy/memory conservation.
8. **No post-hoc promotion.** Exposure calibration may tune event frequency, but must not select a rate because it produces larger genomes or a desirable ecological outcome.

## Decision 1 — Introduce an indel-tolerant replication substrate before structural mutation

Phase Five should add a minimal new replication/addressing layer rather than modifying the semantics of the frozen `COPY`, `JUMP`, or `DIVIDE` instructions in older engines.

### 1A. Sequential copy head

Add a Phase-Five-only sequential copy primitive, provisionally named `COPY_NEXT`.

Conceptual semantics:

- each organism has a replication read position initialized to the beginning of its own genome for a new replication lifecycle;
- `COPY_NEXT` copies exactly one current genome instruction into the daughter buffer and advances that read position;
- after the final instruction is copied, the VM exposes a completion state to ordinary control flow;
- the instruction does **not** divide automatically and does not decide whether reproduction is beneficial;
- `DIVIDE` still remains an explicit genome instruction and still requires a complete copied daughter proposal.

The daughter buffer for the Phase Five VM should be dynamic rather than pre-sized to a hard-coded parent length. This removes the artificial requirement that the genome know its size as an 8-bit literal.

The preferred completion interface is a simple VM-visible condition (for example the existing condition register convention) rather than a `COPY_ALL` operation. The genome must still execute a loop and an explicit `DIVIDE`.

### 1B. Template-based indirect flow control

Absolute jumps remain available for legacy semantics, but the new Phase Five ancestor must not depend on them for its replication loop.

Introduce two neutral template-forming no-ops, provisionally `NOP_A` and `NOP_B`, plus the minimum template-search jump operations required for a loop and an exit branch.

A template is a short consecutive sequence of `NOP_A`/`NOP_B`. A jump reads its following template and searches within the organism's own genome for the complementary template. Direct execution of the NOPs has no state effect.

This gives evolution an address representation that survives insertions/deletions outside the relevant template instead of embedding absolute instruction indexes in control flow.

The exact template-search failure behavior, maximum template length, search direction and circular/non-circular semantics must be frozen in the Phase Five VM contract before mutation experiments begin.

### Why not only add `GENOME_LENGTH`?

A self-length instruction would solve the hard-coded copy count but not the absolute-jump problem, and an 8-bit register would also impose an artificial 255-instruction ceiling unless the hardware changed. A sequential copy head plus indirect addressing solves both core brittleness problems without defining a preferred genome size.

## Decision 2 — First expansion operator: single-instruction tandem duplication

Phase Five should **not** begin with arbitrary random-instruction insertion.

Melakat instructions contain an opcode plus operands (`a`, `b`). A random insertion therefore requires the host to invent a distribution over opcode and operand values. That distribution would be an additional design choice and could dominate viability.

Instead, the first length-increasing operator will be a blind **single-instruction tandem duplication**:

1. choose one instruction index uniformly from the proposed child genome;
2. copy that complete instruction, including its operands;
3. insert the duplicate immediately after the source instruction.

This increases length by exactly one without the host inventing a new instruction payload. Existing blind opcode substitution remains the source of semantic divergence, so a duplicated instruction can later change independently.

This is a structural affordance, not a statement that duplication is advantageous.

## Decision 3 — First contraction operator: single-instruction deletion

The first length-decreasing operator will:

1. choose one instruction index uniformly;
2. remove exactly that instruction;
3. reject only a transition to an empty genome as a substrate-invalid state.

No attempt should be made to protect replication instructions, templates, sensing instructions, movement instructions, or any host-defined "essential" region. Deleting a critical instruction is allowed to be lethal.

## Decision 4 — At most one structural event per daughter proposal in the first gate

Initial Phase Five structural mutation uses a per-division event model:

- `mutation.structural_event_rate`: probability that one structural event is proposed for a daughter;
- `mutation.structural_duplication_probability`: conditional probability that the event is duplication; otherwise it is deletion.

Only one structural event may occur in the initial gate. This avoids confounding the first evidence campaign with multiple simultaneous length changes.

Planned isolated conditions can hold total event rate fixed while selecting:

- structural OFF;
- duplication-only;
- deletion-only;
- balanced duplication/deletion.

A later phase may study per-site rates, multiple events, large indels or segment rearrangements. They are not part of the first Phase Five evidence gate.

## Decision 5 — Structural mutation uses an independent deterministic RNG stream

Structural-event draws should use a derived, versioned RNG stream separate from the historical mutation/spatial streams.

Reason: enabling a new operator should not perturb legacy random draws merely because an extra random number was requested. After a structural mutation changes a genome, trajectories may of course diverge naturally.

The stream derivation/version must be recorded in provenance.

## Mutation ordering

For the first Phase Five contract:

1. successful self-copy produces the normal daughter proposal;
2. the existing substitution channel is applied according to its registered semantics;
3. at most one Phase Five structural event is applied;
4. the resulting child genome becomes the stable pending daughter proposal;
5. memory and energy eligibility are evaluated using that resulting genome;
6. if reproduction is blocked, the same pending genome must be retried rather than re-mutated.

This preserves the existing rule that a blocked division does not repeatedly reroll mutations.

## Natural costs — no explicit genome-size fitness term

Phase Five must not add a size-dependent fitness score.

Existing substrate costs already provide physical consequences:

- live-memory allocation is `working memory + genome length`;
- longer genomes occupy more of the finite world memory capacity;
- a sequential self-copy requires more `COPY_NEXT` executions for longer genomes;
- execution already costs energy per instruction;
- longer replication can therefore take more ticks and energy;
- shorter genomes may be faster/cheaper but can lose necessary functionality.

These trade-offs are enough to let selection act without telling the system whether larger or smaller is "better".

## Phase Five staged evidence plan

### Gate 5A — Representation robustness

Structural mutation remains OFF.

Required demonstrations:

- the new ancestor self-replicates for multiple generations;
- manually constructed viable genomes of different lengths can self-replicate using the same replication logic;
- adding/removing a neutral instruction outside a replication-critical template does not fail merely because absolute addresses shifted;
- copied instruction count equals the current genome length;
- `DIVIDE` cannot commit an incomplete copy;
- deterministic replay passes;
- all frozen Phase Zero–Four tests and checksums remain unchanged.

Passing 5A authorizes structural mutation implementation.

### Gate 5B — Structural mutation mechanics

Run small deterministic tests and smoke campaigns with single-instruction duplication/deletion.

Required demonstrations:

- duplication changes length by exactly `+1`;
- deletion changes length by exactly `-1` except that an empty genome is rejected;
- mutation positions are unbiased over available instruction indexes;
- parent/child genome hashes and lengths are recorded;
- pending blocked daughters remain stable;
- child memory allocation reflects mutated genome length;
- no conservation or atomic-accounting regression;
- structural event counts are exported to both JSON and CSV artifacts.

No persistence or complexity result is required to pass this mechanics gate.

### Gate 5C — Exposure calibration

Use a predeclared small set of candidate per-division structural event rates.

Calibration may choose the **lowest** candidate that produces sufficient structural-event exposure while passing integrity/reproducibility gates. Calibration must not choose a rate because it yields genome expansion, higher population, longer-lived lineages, or another favorable outcome.

The selected rate and full-campaign duration are frozen before outcome interpretation.

### Gate 5D — Full variable-genome campaign

The first inferential campaign compares matched seeds under a frozen Phase Five substrate.

Primary structural endpoints:

- structural events attempted/committed by type;
- parent-to-child genome-length delta;
- mean, median, minimum and maximum genome length;
- genome-length variance;
- number of distinct genome lengths;
- births with non-ancestral genome length;
- structurally changed offspring that later reproduce at least once;
- persistence duration/generation depth of non-ancestral-length lineages.

Primary cost/accounting endpoints:

- genome memory occupied;
- replication copy operations;
- execution energy spent during replication;
- reproduction latency where measurable;
- memory-blocked divisions;
- total live memory and free memory.

Population/genotype/ecological metrics remain secondary.

Matched-seed uncertainty intervals must be reported. A non-zero mean genome-length difference is not enough by itself to claim greater evolvability or complexity.

## Interpretation boundaries

### Allowed if the mechanism works

- "Melakat supports heritable variable-length genomes."
- "Blind structural mutation generated shorter/longer descendants."
- "Some structural variants persisted/reproduced under the existing world constraints" — only if directly evidenced.

### Not allowed from Phase Five alone

- "complexity increased";
- "larger genomes are more advanced";
- "adaptation increased";
- "intelligence emerged";
- "open-ended evolution was achieved";
- "gene duplication evolved new biological functions".

Genome length is a prerequisite for a larger search space, not a complexity metric.

## Deferred mechanisms

### Arbitrary random insertion

Deferred until Melakat has an explicit, audited rule for generating an inserted instruction's operands. We should not silently let host-side operand sampling become an evolutionary bias.

### Segment duplication/deletion

Deferred until single-instruction structural events pass their evidence gate. Segment events change multiple correlated instructions and can cause large memory jumps, so they deserve a separate causal gate.

### Inversion, translocation, recombination, crossover

Out of scope for initial Phase Five.

### General operand mutation

Potentially important for future evolvability, but separate from the first structural-length intervention. The existing movement-step operand mutation remains its own historical mechanism.

## Measurements to add before scientific use

The Phase Five measurement contract should include at least:

- `genome_length_mean`
- `genome_length_median`
- `genome_length_minimum`
- `genome_length_maximum`
- `genome_length_variance`
- `distinct_genome_lengths`
- `structural_mutation_operations`
- `instruction_duplication_operations`
- `instruction_deletion_operations`
- `structural_mutation_rejected_operations`
- `variable_length_births`
- `variable_length_reproducing_offspring`
- `replication_copy_operations`
- `genome_memory_used`

Event records should include parent length, child length, mutation type, source/deletion index, generation, parent/child IDs and genotype hashes where applicable.

## Engineering boundary

Phase Five must be implemented as a new versioned contract/backend. It must not silently redefine:

- Phase Zero `VirtualMachine`;
- frozen Phase One mutation semantics;
- frozen Phase Two VM;
- accepted Phase Three atomic movement behavior;
- accepted Phase Four sensing/movement evidence.

The first implementation PR after this design contract should contain the Phase Five VM/representation robustness work only. Structural mutation should enter in a subsequent PR after Gate 5A passes.

## External design precedents

- Thomas S. Ray, Tierra: evolved machine code used template-based addressing to reduce brittleness under mutation and support evolvable self-replication.
- Ofria & Wilke, Avida: template/head-based addressing avoids absolute memory positions that would be disrupted by insertions/deletions; Avida supports point, insertion and deletion mutation channels.
- Gupta et al. (2016), *Evolution of Genome Size in Asexual Digital Organisms*: digital-evolution experiments show genome size is an evolutionary outcome shaped by mutation regime and selection, and larger size must not be treated as a direct synonym for complexity.
- Aevol: explicitly models substitutions, small indels, duplications, deletions and other rearrangements while treating mutation as sequence change without an a priori beneficial effect.

Useful references:

- https://people.scs.carleton.ca/~soma/biosec/readings/tierra.pdf
- https://cse.msu.edu/~ofria/pubs/2004OfriaEtAl.pdf
- https://github.com/devosoft/avida/blob/master/avida-core/support/config/avida.cfg
- https://pmc.ncbi.nlm.nih.gov/articles/PMC4867773/
- https://www.aevol.fr/model-description/detailed/

## Phase Five definition of done

Phase Five is complete only when:

1. a length-robust self-replication representation is implemented and evidenced;
2. single-instruction duplication/deletion are auditable and independently controllable;
3. variable genome lengths are generated and inherited in full matched-seed campaigns;
4. memory, execution, reproduction and conservation accounting remain valid;
5. deterministic replay passes;
6. full artifacts and paired analyses are archived;
7. scientific conclusions explicitly distinguish genome-length evolvability from complexity.

Until those gates pass, Melakat should not claim that genome complexity itself is evolving.
