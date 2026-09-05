import unittest

from melakat_desktop.engine import DemoEngine
from melakat_desktop.parameters import CORE_SCHEMA


class EngineTests(unittest.TestCase):
    def _config(self) -> dict:
        return CORE_SCHEMA.validate(CORE_SCHEMA.defaults())

    def test_same_seed_produces_same_snapshot(self) -> None:
        first_events = []
        second_events = []
        first = DemoEngine(self._config(), first_events.append)
        second = DemoEngine(self._config(), second_events.append)
        for _ in range(20):
            first.step()
            second.step()
        self.assertEqual(first.snapshot(), second.snapshot())
        self.assertEqual(first.metrics(), second.metrics())

    def test_memory_capacity_is_respected(self) -> None:
        config = self._config()
        config["world.memory_capacity"] = 12
        config["population.memory_per_organism"] = 4
        config["population.initial_size"] = 10
        events = []
        engine = DemoEngine(config, events.append)
        for _ in range(100):
            engine.step()
        self.assertLessEqual(engine.metrics()["memory_used"], 12)

    def test_engine_finishes_at_max_ticks(self) -> None:
        config = self._config()
        config["run.max_ticks"] = 3
        events = []
        engine = DemoEngine(config, events.append)
        for _ in range(10):
            engine.step()
        self.assertEqual(engine.tick, 3)
        self.assertTrue(engine.finished)


if __name__ == "__main__":
    unittest.main()
