from __future__ import annotations

import random
import unittest

from melakat_desktop.parameters import CORE_SCHEMA
from melakat_desktop.phase_five_engine import (
    PhaseFiveEngine,
    apply_structural_mutation,
    derive_structural_seed,
)
from melakat_desktop.vm import Instruction, Opcode


class PhaseFiveStructuralMutationTests(unittest.TestCase):
    def test_duplication_adds_exactly_one_identical_instruction(self) -> None:
        genome = (
            Instruction(Opcode.NOP),
            Instruction(Opcode.INC, a=2, b=7),
            Instruction(Opcode.DEC, a=1, b=9),
        )
        result = apply_structural_mutation(
            genome,
            random.Random(7),
            event_rate=1.0,
            duplication_probability=1.0,
        )
        self.assertTrue(result.committed)
        self.assertEqual(result.kind, "duplication")
        self.assertEqual(len(result.genome), len(genome) + 1)
        self.assertEqual(result.length_delta, 1)
        self.assertIsNotNone(result.index)
        index = int(result.index)
        self.assertEqual(result.genome[index], genome[index])
        self.assertEqual(result.genome[index + 1], genome[index])

    def test_deletion_removes_exactly_one_instruction(self) -> None:
        genome = tuple(Instruction(Opcode.NOP, a=index) for index in range(4))
        result = apply_structural_mutation(
            genome,
            random.Random(9),
            event_rate=1.0,
            duplication_probability=0.0,
        )
        self.assertTrue(result.committed)
        self.assertEqual(result.kind, "deletion")
        self.assertEqual(len(result.genome), len(genome) - 1)
        self.assertEqual(result.length_delta, -1)

    def test_deletion_rejects_empty_genome(self) -> None:
        genome = (Instruction(Opcode.NOP),)
        result = apply_structural_mutation(
            genome,
            random.Random(1),
            event_rate=1.0,
            duplication_probability=0.0,
        )
        self.assertTrue(result.attempted)
        self.assertTrue(result.rejected)
        self.assertFalse(result.committed)
        self.assertEqual(result.genome, genome)
        self.assertEqual(result.length_delta, 0)

    def test_structural_positions_are_uniform_within_sampling_tolerance(self) -> None:
        genome = tuple(Instruction(Opcode.NOP, a=index) for index in range(4))
        rng = random.Random(12345)
        counts = [0, 0, 0, 0]
        trials = 20_000
        for _ in range(trials):
            result = apply_structural_mutation(
                genome,
                rng,
                event_rate=1.0,
                duplication_probability=1.0,
            )
            counts[int(result.index)] += 1
        fractions = [count / trials for count in counts]
        for fraction in fractions:
            self.assertGreater(fraction, 0.235)
            self.assertLess(fraction, 0.265)

    def test_structural_rng_seed_is_deterministic_versioned_and_separate(self) -> None:
        self.assertEqual(derive_structural_seed(17), derive_structural_seed(17))
        self.assertNotEqual(derive_structural_seed(17), derive_structural_seed(18))
        self.assertNotEqual(derive_structural_seed(17), 17)

    def _blocked_engine(self) -> PhaseFiveEngine:
        config = CORE_SCHEMA.defaults()
        config.update(
            {
                "run.seed": 21,
                "run.max_ticks": 300,
                "population.initial_size": 1,
                "population.initial_energy": 100.0,
                "world.initial_energy": 1000.0,
                "world.energy_input_per_tick": 10.0,
                "world.memory_capacity": 22,
                "mutation.substitution_rate": 0.0,
                "mutation.structural_event_rate": 1.0,
                "mutation.structural_duplication_probability": 1.0,
            }
        )
        return PhaseFiveEngine(config, lambda _event: None)

    def test_memory_block_uses_structurally_changed_child_length(self) -> None:
        engine = self._blocked_engine()
        parent = engine.organisms[0]
        for _ in range(200):
            engine.step()
            if parent.pending_child_genome is not None:
                break
        self.assertIsNotNone(parent.pending_child_genome)
        self.assertEqual(len(parent.genome), 14)
        self.assertEqual(len(parent.pending_child_genome), 15)
        self.assertEqual(parent.reproduction_block_reason, "memory")
        self.assertEqual(engine._allocation_for_genome(parent.pending_child_genome), 23)
        self.assertEqual(engine.structural_mutation_operations, 1)
        self.assertEqual(engine.instruction_duplication_operations, 1)

    def test_blocked_pending_child_is_stable_and_not_remutated(self) -> None:
        engine = self._blocked_engine()
        parent = engine.organisms[0]
        for _ in range(200):
            engine.step()
            if parent.pending_child_genome is not None:
                break
        first_genome = parent.pending_child_genome
        first_event = engine._pending_structural_events[parent.organism_id]
        first_count = engine.structural_mutation_operations
        for _ in range(10):
            engine.step()
        self.assertEqual(parent.pending_child_genome, first_genome)
        self.assertEqual(engine._pending_structural_events[parent.organism_id], first_event)
        self.assertEqual(engine.structural_mutation_operations, first_count)

    def test_structural_campaign_records_variable_length_births_and_conserves_energy(self) -> None:
        config = CORE_SCHEMA.defaults()
        config.update(
            {
                "run.seed": 3,
                "run.max_ticks": 500,
                "population.initial_size": 4,
                "population.initial_energy": 40.0,
                "world.memory_capacity": 1000,
                "world.initial_energy": 2000.0,
                "world.energy_input_per_tick": 20.0,
                "mutation.substitution_rate": 0.0,
                "mutation.structural_event_rate": 1.0,
                "mutation.structural_duplication_probability": 1.0,
            }
        )
        events: list[dict] = []
        engine = PhaseFiveEngine(config, events.append)
        while not engine.finished:
            engine.step()
        summary = engine.summary()
        self.assertGreater(summary["structural_mutation_operations"], 0)
        self.assertEqual(
            summary["structural_mutation_operations"],
            summary["instruction_duplication_operations"],
        )
        self.assertGreater(summary["variable_length_births"], 0)
        self.assertGreater(summary["genome_length_maximum"], 14)
        self.assertLessEqual(abs(summary["energy_balance_error"]), 1e-7)
        proposed = [event for event in events if event["type"] == "structural_mutation_proposed"]
        born = [event for event in events if event["type"] == "organism_born"]
        self.assertTrue(proposed)
        self.assertTrue(any(event.get("structural_mutation_committed") for event in born))

    def test_structural_replay_is_deterministic(self) -> None:
        config = CORE_SCHEMA.defaults()
        config.update(
            {
                "run.seed": 31,
                "run.max_ticks": 300,
                "population.initial_size": 3,
                "world.memory_capacity": 700,
                "mutation.substitution_rate": 0.01,
                "mutation.structural_event_rate": 0.2,
                "mutation.structural_duplication_probability": 0.5,
            }
        )
        first = PhaseFiveEngine(config, lambda _event: None)
        second = PhaseFiveEngine(config, lambda _event: None)
        while not first.finished:
            first.step()
        while not second.finished:
            second.step()
        self.assertEqual(first.summary(), second.summary())


if __name__ == "__main__":
    unittest.main()
