import unittest

from melakat_desktop.parameters import CORE_SCHEMA
from melakat_desktop.phase_zero_experiment import (
    aggregate,
    run_replicates,
)


class PhaseZeroExperimentTests(unittest.TestCase):
    def test_replicates_return_reproducible_summaries(self) -> None:
        config = CORE_SCHEMA.defaults()
        config.update(
            {
                "run.max_ticks": 20,
                "population.initial_size": 2,
                "world.initial_energy": 100.0,
            }
        )

        runs = run_replicates(config, [1, 2, 3])
        summary = aggregate(runs)

        self.assertEqual(len(runs), 3)
        self.assertEqual(summary["runs"], 3)
        self.assertTrue(all("energy_balance_error" in run for run in runs))


if __name__ == "__main__":
    unittest.main()
