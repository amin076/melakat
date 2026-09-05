import random
import unittest

from melakat_desktop.parameters import CORE_SCHEMA
from melakat_desktop.phase_zero_engine import (
    PhaseZeroEngine,
    mutate_genome,
)


class PhaseZeroEngineTests(unittest.TestCase):
    def _config(self) -> dict:
        config = CORE_SCHEMA.defaults()
        config.update(
            {
                "run.max_ticks": 40,
                "population.initial_size": 1,
                "world.initial_energy": 100.0,
                "world.energy_input_per_tick": 20.0,
                "execution.instructions_per_tick": 8,
                "execution.instruction_cost": 0.01,
                "execution.maintenance_cost": 0.01,
                "reproduction.cost": 1.0,
                "reproduction.offspring_energy": 2.0,
                "mutation.substitution_rate": 0.0,
            }
        )
        return config

    def test_engine_reproduces_without_a_reproduce_instruction(self) -> None:
        events: list[dict] = []
        engine = PhaseZeroEngine(self._config(), events.append)

        for _ in range(40):
            if engine.finished:
                break
            engine.step()

        self.assertGreater(engine.births, 0)
        self.assertGreater(engine.max_population, 1)
        self.assertTrue(any(event["name"] == "organism_born" for event in events))

    def test_mutation_is_seeded_and_heritable_data(self) -> None:
        genome = PhaseZeroEngine.default_genome()
        mutated = mutate_genome(genome, random.Random(7), 1.0)

        self.assertEqual(len(mutated), len(genome))
        self.assertNotEqual(mutated, genome)

    def test_energy_and_memory_accounting(self) -> None:
        engine = PhaseZeroEngine(self._config(), lambda event: None)

        for _ in range(20):
            engine.step()

        self.assertAlmostEqual(engine.energy_balance_error(), 0.0, places=8)
        self.assertLessEqual(
            engine.metrics()["memory_used"],
            self._config()["world.memory_capacity"],
        )

    def test_death_releases_memory_and_energy(self) -> None:
        config = self._config()
        config.update(
            {
                "population.initial_energy": 0.0,
                "world.initial_energy": 0.0,
                "world.energy_input_per_tick": 0.0,
                "execution.maintenance_cost": 1.0,
                "run.max_ticks": 1,
            }
        )
        engine = PhaseZeroEngine(config, lambda event: None)

        engine.step()

        self.assertEqual(engine.metrics()["active_population"], 0)
        self.assertEqual(engine.metrics()["memory_used"], 0)
        self.assertEqual(engine.metrics()["deaths"], 1)

    def test_same_seed_is_reproducible(self) -> None:
        first = PhaseZeroEngine(self._config(), lambda event: None)
        second = PhaseZeroEngine(self._config(), lambda event: None)

        for _ in range(20):
            first.step()
            second.step()

        self.assertEqual(first.summary(), second.summary())


if __name__ == "__main__":
    unittest.main()
