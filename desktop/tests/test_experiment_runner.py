from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from melakat_desktop.experiment_runner import (
    EXPERIMENT_SPEC_FORMAT,
    build_experiment_plan,
    load_experiment_spec,
    run_experiment,
    write_experiment_outputs,
)


class ExperimentRunnerTests(unittest.TestCase):
    def _spec(self) -> dict:
        return {
            "format": EXPERIMENT_SPEC_FORMAT,
            "name": "runner-smoke",
            "description": "Small deterministic automated experiment test.",
            "base_config": {
                "run.engine_backend": "phase-two-vm",
                "run.max_ticks": 30,
                "world.spatial_enabled": True,
                "world.local_resources_enabled": True,
                "world.organism_actions_enabled": False,
            },
            "seeds": {"start": 1, "count": 2},
            "conditions": [
                {
                    "name": "local",
                    "overrides": {"world.energy_input_per_tick": 10.4},
                }
            ],
            "sweeps": [
                {
                    "name": "energy",
                    "base_overrides": {
                        "world.spatial_enabled": True,
                        "world.local_resources_enabled": True,
                        "world.organism_actions_enabled": False,
                    },
                    "parameter": "world.energy_input_per_tick",
                    "values": [20.0, 40.0],
                }
            ],
        }

    def test_json_spec_loads_and_sweep_expands(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "experiment.json"
            path.write_text(json.dumps(self._spec()), encoding="utf-8")
            loaded = load_experiment_spec(path)
            plan = build_experiment_plan(loaded)
        self.assertEqual(plan["name"], "runner-smoke")
        self.assertEqual(plan["seeds"], [1, 2])
        self.assertEqual(plan["run_count"], 6)
        names = [condition["name"] for condition in plan["conditions"]]
        self.assertEqual(
            names,
            [
                "local",
                "energy__energy_input_per_tick=20.0",
                "energy__energy_input_per_tick=40.0",
            ],
        )

    def test_cli_style_overrides_reduce_campaign_for_ci(self) -> None:
        plan = build_experiment_plan(
            self._spec(),
            seed_count_override=1,
            seed_start_override=7,
            ticks_override=12,
        )
        self.assertEqual(plan["seeds"], [7])
        self.assertEqual(plan["base_config"]["run.max_ticks"], 12)
        self.assertEqual(plan["run_count"], 3)

    def test_unknown_parameter_is_rejected(self) -> None:
        spec = self._spec()
        spec["base_config"]["world.typo_parameter"] = 1
        with self.assertRaisesRegex(ValueError, "unknown_parameters"):
            build_experiment_plan(spec)

    def test_small_campaign_validates_and_is_reproducible(self) -> None:
        campaign = run_experiment(
            self._spec(),
            seed_count_override=1,
            ticks_override=30,
            progress=False,
        )
        self.assertEqual(campaign["validation"]["expected_runs"], 3)
        self.assertEqual(campaign["validation"]["completed_runs"], 3)
        self.assertTrue(campaign["validation"]["passed"])
        self.assertTrue(
            campaign["validation"]["reproducibility"]["identical"]
        )
        self.assertEqual(campaign["summary"]["condition_count"], 3)

    def test_outputs_include_machine_readable_campaign_and_checksums(self) -> None:
        spec = self._spec()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec_path = root / "spec.json"
            spec_path.write_text(json.dumps(spec), encoding="utf-8")
            campaign = run_experiment(
                spec,
                seed_count_override=1,
                ticks_override=20,
                progress=False,
            )
            output = root / "output"
            write_experiment_outputs(output, campaign, spec_path=spec_path)
            expected = {
                "campaign.json",
                "summary.json",
                "validation.json",
                "runs.csv",
                "comparison.csv",
                "provenance.json",
                "SHA256SUMS.txt",
            }
            self.assertEqual({path.name for path in output.iterdir()}, expected)
            validation = json.loads(
                (output / "validation.json").read_text(encoding="utf-8")
            )
            self.assertTrue(validation["passed"])
            manifest = (output / "SHA256SUMS.txt").read_text(encoding="utf-8")
            self.assertIn("campaign.json", manifest)
            self.assertIn("provenance.json", manifest)


if __name__ == "__main__":
    unittest.main()
