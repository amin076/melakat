import unittest

from melakat_desktop import experiment_runner
from melakat_desktop.phase_three_contract import PHASE_THREE_WORLD_CONTRACT_VERSION
from melakat_desktop.phase_three_experiment_support import (
    PHASE_THREE_PARAMETERS,
    phase_three_experiment_support,
)


class PhaseThreeExperimentRunnerTests(unittest.TestCase):
    @staticmethod
    def _spec() -> dict:
        return {
            "format": experiment_runner.EXPERIMENT_SPEC_FORMAT,
            "name": "phase-three-runner-smoke",
            "description": "Matched Phase Three uniform-versus-patch smoke campaign.",
            "base_config": {
                "run.engine_backend": "phase-three-vm",
                "run.max_ticks": 60,
                "world.width": 96,
                "world.height": 70,
                "world.spatial_enabled": True,
                "world.local_resources_enabled": True,
                "world.resource_grid_cols": 10,
                "world.resource_grid_rows": 7,
                "world.local_capture_limit": 1.0,
                "world.initial_energy": 1000.0,
                "world.energy_input_per_tick": 20.0,
                "world.organism_actions_enabled": False,
            },
            "seeds": {"start": 1, "count": 2},
            "conditions": [
                {
                    "name": "uniform-control",
                    "overrides": {"world.resource_distribution_mode": "uniform"},
                },
                {
                    "name": "center-patch",
                    "overrides": {"world.resource_distribution_mode": "center_patch"},
                },
            ],
            "reproducibility": {"condition": "uniform-control", "seed": 1},
        }

    def test_phase_three_support_is_scoped_and_does_not_change_phase_two_globals(self) -> None:
        original_known = experiment_runner.KNOWN_PARAMETERS
        original_supported = experiment_runner.SUPPORTED_ENGINES
        original_world_contract = experiment_runner.WORLD_CONTRACT_VERSION

        with phase_three_experiment_support():
            self.assertTrue(PHASE_THREE_PARAMETERS <= experiment_runner.KNOWN_PARAMETERS)
            self.assertIn("phase-three-vm", experiment_runner.SUPPORTED_ENGINES)
            self.assertEqual(
                experiment_runner.WORLD_CONTRACT_VERSION,
                PHASE_THREE_WORLD_CONTRACT_VERSION,
            )

        self.assertEqual(experiment_runner.KNOWN_PARAMETERS, original_known)
        self.assertEqual(experiment_runner.SUPPORTED_ENGINES, original_supported)
        self.assertEqual(experiment_runner.WORLD_CONTRACT_VERSION, original_world_contract)

    def test_plan_injects_phase_three_defaults_only_inside_phase_three_context(self) -> None:
        with phase_three_experiment_support():
            plan = experiment_runner.build_experiment_plan(self._spec())

        self.assertEqual(plan["run_count"], 4)
        self.assertEqual(
            plan["base_config"]["world.resource_distribution_mode"],
            "uniform",
        )
        self.assertEqual(plan["base_config"]["world.resource_patch_fraction"], 0.30)
        self.assertEqual(plan["base_config"]["world.resource_patch_contrast"], 4.0)
        self.assertNotIn(
            "world.resource_distribution_mode",
            experiment_runner.CORE_SCHEMA.defaults(),
        )

    def test_phase_three_campaign_is_reproducible_conservative_and_measured(self) -> None:
        with phase_three_experiment_support():
            campaign = experiment_runner.run_experiment(
                self._spec(),
                seed_count_override=1,
                ticks_override=80,
                progress=False,
            )

        self.assertTrue(campaign["validation"]["passed"])
        self.assertEqual(campaign["validation"]["expected_runs"], 2)
        self.assertTrue(campaign["validation"]["reproducibility"]["identical"])
        self.assertEqual(
            campaign["world_contract_version"],
            PHASE_THREE_WORLD_CONTRACT_VERSION,
        )

        runs = {run["condition"]: run for run in campaign["runs"]}
        uniform = runs["uniform-control"]
        patch = runs["center-patch"]
        self.assertEqual(uniform["resource_distribution_mode"], "uniform")
        self.assertEqual(patch["resource_distribution_mode"], "center_patch")
        self.assertAlmostEqual(uniform["resource_heterogeneity_cv"], 0.0, places=10)
        self.assertGreater(patch["resource_heterogeneity_cv"], 0.0)
        self.assertLessEqual(abs(float(uniform["energy_balance_error"])), 1e-7)
        self.assertLessEqual(abs(float(patch["energy_balance_error"])), 1e-7)
        self.assertLessEqual(abs(float(uniform["local_resource_balance_error"])), 1e-7)
        self.assertLessEqual(abs(float(patch["local_resource_balance_error"])), 1e-7)

        rows = {row["condition"]: row for row in campaign["summary"]["conditions"]}
        self.assertIn("resource_heterogeneity_cv_mean", rows["uniform-control"])
        self.assertIn("resource_heterogeneity_cv_mean", rows["center-patch"])

    def test_invalid_phase_three_patch_parameter_fails_plan_validation(self) -> None:
        spec = self._spec()
        spec["base_config"]["world.resource_patch_fraction"] = 0.0
        with phase_three_experiment_support():
            with self.assertRaisesRegex(
                ValueError,
                "resource_patch_fraction_must_be_in_0_1",
            ):
                experiment_runner.build_experiment_plan(spec)


if __name__ == "__main__":
    unittest.main()
