import unittest

from melakat_desktop.parameters import CORE_SCHEMA
from melakat_desktop.phase_zero_experiment import (
    aggregate,
    run_control_suite,
    run_replicates,
    run_sensitivity_sweep,
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
        self.assertTrue(all("config_hash" in run for run in runs))
        self.assertIn("mean_blocked_divisions", summary)
        self.assertIn("mean_historical_genotypes", summary)

    def test_control_suite_reuses_the_same_seed_set(self) -> None:
        config = CORE_SCHEMA.defaults()
        config["run.max_ticks"] = 5

        controls = run_control_suite(config, [4, 5])

        self.assertEqual(
            {len(result["runs"]) for result in controls.values()},
            {2},
        )
        self.assertEqual(
            {
                run["seed"]
                for result in controls.values()
                for run in result["runs"]
            },
            {4, 5},
        )
        self.assertTrue(
            all(
                run["control"] == control
                for control, result in controls.items()
                for run in result["runs"]
            )
        )

    def test_sensitivity_sweep_reuses_seed_set(self) -> None:
        config = CORE_SCHEMA.defaults()
        config["run.max_ticks"] = 2

        sweeps = run_sensitivity_sweep(config, [7])

        self.assertIn("mutation.substitution_rate", sweeps)
        cases = sweeps["mutation.substitution_rate"]["cases"]
        self.assertEqual(set(cases), {"0.0", "0.01", "0.05"})
        self.assertTrue(
            all(len(case["runs"]) == 1 for case in cases.values())
        )
        self.assertTrue(
            all(
                run["control"].startswith(
                    "mutation.substitution_rate="
                )
                for case in cases.values()
                for run in case["runs"]
            )
        )


if __name__ == "__main__":
    unittest.main()
