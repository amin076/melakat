# Phase Two World Contract 0.1

[فارسی](phase-two-world-contract-0.1.fa.md) | [Phase Two roadmap](../doc-english/phase-two-roadmap.md)

## Identity

- World contract: `phase-two-spatial-0.1`
- Compatibility engine: `phase-two-vm-0.1`
- Frozen reference engine: `phase-zero-vm-0.2`
- Measurement contract: `phase-one-measurement-0.1`
- Spatial run artifact: `melakat-run-artifact-0.2`

This contract is the P2.1 transition layer. It does not activate a spatial law. Its purpose is to make timing, coordinates, versioning, persistence, and baseline compatibility explicit before P2.2 adds topology.

## P2.1 compatibility mode

`world.spatial_enabled` defaults to `false`.

When it is false, `phase-two-vm-0.1` delegates all scientific state transitions to the frozen Phase One reference engine. P2.1 may add version metadata but must not change the RNG sequence, organism execution, energy accounting, memory accounting, mutation, reproduction, birth, or death.

Setting `world.spatial_enabled=true` is rejected with `spatial_rules_not_implemented:p2.2_required`. This prevents an undocumented partial spatial mode.

## Coordinates and units

The world has two abstract coordinate dimensions.

- `x` is bounded by the configured interval from `0` to `world.width`.
- `y` is bounded by the configured interval from `0` to `world.height`.
- The coordinate unit is an `abstract_world_unit`; it is not a metre, cell diameter, or biological distance.

Phase One already stored random `x` and `y` values for organisms. Under P2.1 compatibility mode those values remain state and remain checksum-covered, but they have no causal effect on execution, energy, memory, reproduction, mutation, birth, or death.

P2.2 must define the first active boundary model before coordinates can affect dynamics.

## Tick and event order

The reference model is sequential, not simultaneous.

For each tick:

1. increment the tick and add `world.energy_input_per_tick` to the global energy pool;
2. capture the currently active organism list and shuffle it with the seeded RNG;
3. for each still-living scheduled organism, increment age;
4. capture up to one energy unit from the global pool;
5. charge maintenance; insufficient energy causes immediate death for that organism;
6. if a division request is already pending, retry that division and end this organism's work for the tick; otherwise execute the bounded VM instruction slice;
7. charge the VM execution cost; insufficient energy causes immediate death;
8. convert a VM fault into a recorded death;
9. if VM execution requested division, attempt division using the documented memory and energy checks;
10. after the sequential schedule, update maximum population, record history when due, emit an optional snapshot, and finish when the tick limit is reached.

Therefore organisms later in the shuffled schedule can observe resource state changed by organisms earlier in the same tick. P2.1 does not reinterpret this as a simultaneous world.

## Environment update

The environment update happens once at tick start and currently consists only of global energy input. There is no local resource field, diffusion, movement, deposit, or local consumption in P2.1.

## Boundary and movement semantics

- active boundary model: none while spatial rules are disabled;
- movement: not implemented in P2.1;
- local sensing: not implemented in P2.1;
- local resource exchange: not implemented in P2.1.

P2.2 must introduce exactly one tested boundary model before any alternative boundary behavior is added.

## Precision and conservation

Energy is maintained internally with Python floating-point values without ledger rounding. Serialized metrics round selected values for output only. The Phase One evidence-gate tolerance remains `1e-7` for energy balance.

Memory is counted in exact nonnegative integer units. Active allocated memory must not exceed `world.memory_capacity`.

A future local resource field requires its own source/sink ledger and conservation tolerance; P2.1 does not silently reuse the global-energy tolerance for an undefined resource.

## State and artifact format

P2.1 snapshots and metrics add:

- `world_contract_version`;
- `spatial_enabled`.

A result carrying a world-contract version is exported as `melakat-run-artifact-0.2`. The loader continues to accept `melakat-run-artifact-0.1`, so archived Phase One results remain reloadable and comparable.

The exact validated configuration and `config_hash` remain part of every new result. Adding `world.spatial_enabled` changes the configuration hash by design even when the value is false; scientific baseline equivalence is therefore checked with a separately frozen scientific-state fingerprint rather than by requiring identical configuration hashes.

## Frozen baseline compatibility evidence

Before P2.1 engine changes, the merged Phase One reference was executed for `2000` ticks with `seed=1`.

- reference run config hash: `7d6516f717c33885`;
- full scientific summary fingerprint, excluding only the top-level configuration hash: `ffafec2384fff475494f706163c2c59ee59c19ff71b4492f2778a231f033b13a`;
- final snapshot fingerprint: `594d01654ac43d06245b18556b08394773cb848f62fdfd108a1f6abbf4eef112`.

The P2.1 compatibility test normalizes only new configuration/version metadata. History, genealogy, genotype records, VM state, organism coordinates, ledger values, and final snapshot scientific state remain checksum-covered.

## P2.1 exit condition

P2.1 passes only if:

- the contract and tick order are test-covered;
- `world.spatial_enabled` defaults to false;
- an attempt to enable undeveloped spatial rules fails explicitly;
- the `phase-two-vm` backend is independently selectable;
- disabled spatial mode reproduces the frozen Phase One scientific and snapshot fingerprints;
- new artifacts carry the world-contract version while old `0.1` artifacts remain loadable;
- unit tests and syntax compilation pass.

Passing P2.1 authorizes work on P2.2. It is not evidence that spatial dynamics exist yet.
