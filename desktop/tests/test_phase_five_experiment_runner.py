from __future__ import annotations

import unittest

from melakat_desktop import experiment_runner
from melakat_desktop.parameters import CORE_SCHEMA
from melakat_desktop.phase_five_engine import PhaseFiveEngine
from melakat_desktop.phase_five_experiment_support import (
    PHASE_FIVE_ENGINE_BACKEND,
    phase_five_experiment_support,
)
from melakat_desktop.worker import create_engine


class PhaseFiveExperimentRunnerTests(unittest.TestCase):
    def _spec(self) -> dict:
        return {
            "format": "melakat-experiment-spec-0.1",
            "name": "phase-five-test",
            "base_config": {
                "run.engine_backend": "phase-five-vm",
                "run.max_ticks": 150,
                "population.initial_size": 3,
                "population.initial_energy": 35.0,
                "world.memory_capacity": 500,
                "world.initial_energy": 1000.0,
                "world.energy_input_per_tick": 15.0,
                "mutation.substitution_rate": 0.0,
            },
            "seeds": {"start": 1, "count": 2},
            "conditions": [
                {
                    "name": "structural-off",
                    "overrides": {"mutation.structural_event_rate": 0.0},
                },
                {
                    "name": "duplication-on",
                    "overrides": {
                        "mutation.structural_event_rate": 1.0,
                        "mutation.structural_duplication_probability": 1.0,
                    },
                },
            ],
            "reproducibility": {"condition": "structural-off", "seed": 1},
        }

    def test_phase_five_support_is_scoped(self) -> None:
        original_schema = experiment_runner.CORE_SCHEMA
        original_supported = experiment_runner.SUPPORTED_ENGINES
        self.assertNotIn(PHASE_FIVE_ENGINE_BACKEND, original_supported)
        with phase_five_experiment_support():
            self.assertIn(PHASE_FIVE_ENGINE_BACKEND, experiment_runner.SUPPORTED_ENGINES)
            self.assertIn(
                "mutation.structural_event_rate",
                {spec.path for spec in experiment_runner.CORE_SCHEMA.specs},
            )
        self.assertIs(experiment_runner.CORE_SCHEMA, original_schema)
        self.assertIs(experiment_runner.SUPPORTED_ENGINES, original_supported)

    def test_plan_injects_phase_five_structural_defaults(self) -> None:
        with phase_five_experiment_support():
            plan = experiment_runner.build_experiment_plan(self._spec())
        self.assertEqual(plan["base_config"]["mutation.structural_event_rate"], 0.0)
        self.assertEqual(
            plan["base_config"]["mutation.structural_duplication_probability"],
            0.5,
        )

    def test_small_phase_five_campaign_is_reproducible_and_measured(self) -> None:
        with phase_five_experiment_support():
            campaign = experiment_runner.run_experiment(self._spec(), progress=False)
        self.assertTrue(campaign["validation"]["passed"])
        self.assertTrue(campaign["validation"]["reproducibility"]["identical"])
        self.assertEqual(len(campaign["runs"]), 4)
        treatment = [
            run for run in campaign["runs"] if run["condition"] == "duplication-on"
        ]
        self.assertTrue(treatment)
        self.assertTrue(
            all("structural_mutation_operations" in run for run in treatment)
        )
        self.assertTrue(any(run["variable_length_births"] > 0 for run in treatment))

    def test_worker_exposes_phase_five_backend(self) -> None:
        config = CORE_SCHEMA.defaults()
        config["run.engine_backend"] = "phase-five-vm"
        engine = create_engine(config, lambda _event: None)
        self.assertIsInstance(engine, PhaseFiveEngine)


if __name__ == "__main__":
    unittest.main()
