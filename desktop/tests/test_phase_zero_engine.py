import unittest

from melakat_desktop.parameters import CORE_SCHEMA
from melakat_desktop.phase_zero_engine import PhaseZeroEngine


class PhaseZeroEngineTests(unittest.TestCase):
    def test_engine_executes_bounded_vm_work(self) -> None:
        config = CORE_SCHEMA.defaults()
        config.update(
            {
                "run.max_ticks": 2,
                "population.initial_size": 2,
                "execution.instructions_per_tick": 4,
            }
        )
        events: list[dict] = []
        engine = PhaseZeroEngine(config, events.append)

        engine.step()

        self.assertEqual(engine.tick, 1)
        self.assertEqual(engine.metrics()["active_population"], 2)
        self.assertEqual(engine.metrics()["instructions_executed"], 8)
        self.assertEqual(engine.snapshot()["engine_version"], "phase-zero-vm-0.1")

        engine.step()

        self.assertTrue(engine.finished)
        self.assertEqual(engine.tick, 2)
        self.assertTrue(any(event["type"] == "finished" for event in events))


if __name__ == "__main__":
    unittest.main()
