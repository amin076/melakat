import unittest

from melakat_desktop.engine import DemoEngine
from melakat_desktop.parameters import CORE_SCHEMA
from melakat_desktop.phase_zero_engine import PhaseZeroEngine
from melakat_desktop.worker import create_engine


class WorkerBackendTests(unittest.TestCase):
    def test_phase_zero_is_default_backend(self) -> None:
        config = CORE_SCHEMA.defaults()
        engine = create_engine(config, lambda event: None)
        self.assertIsInstance(engine, PhaseZeroEngine)

    def test_demo_backend_remains_available(self) -> None:
        config = CORE_SCHEMA.defaults()
        config["run.engine_backend"] = "demo"
        engine = create_engine(config, lambda event: None)
        self.assertIsInstance(engine, DemoEngine)


if __name__ == "__main__":
    unittest.main()
