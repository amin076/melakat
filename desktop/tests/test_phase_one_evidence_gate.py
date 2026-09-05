import unittest

from melakat_desktop.parameters import CORE_SCHEMA
from melakat_desktop.phase_one_evidence import (
    EVIDENCE_CAMPAIGN_FORMAT,
    REQUIRED_CONTROL_NAMES,
    compact_run_record,
    run_evidence_campaign,
    validate_campaign,
)
from melakat_desktop.phase_zero_experiment import CONTROL_PRESETS


class PhaseOneEvidenceGateTests(unittest.TestCase):
    def test_required_controls_include_reproduction_cost_zero(self) -> None:
        self.assertEqual(
            set(REQUIRED_CONTROL_NAMES),
            {
                "baseline",
                "mutation_zero",
                "abundant_energy",
                "abundant_memory",
                "maintenance_zero",
                "reproduction_cost_zero",
            },
        )
        self.assertEqual(set(CONTROL_PRESETS), set(REQUIRED_CONTROL_NAMES))
        self.assertEqual(
            CONTROL_PRESETS["reproduction_cost_zero"]["reproduction.cost"],
            0.0,
        )

    def test_compact_record_keeps_provenance_and_checksum(self) -> None:
        run = {
            "control": "baseline",
            "seed": 7,
            "config_hash": "abc123",
            "engine_version": "phase-zero-vm-0.2",
            "measurement_version": "phase-one-measurement-0.1",
            "tick": 20,
            "active_population": 3,
            "births": 2,
            "deaths": 0,
            "max_population": 3,
            "active_genotypes": 1,
            "historical_genotypes": 1,
            "active_lineages": 1,
            "lineage_count": 1,
            "genotype_count": 1,
            "mutation_events": 0,
            "faults": 0,
            "blocked_divisions": 0,
            "waiting_for_memory": 0,
            "waiting_for_energy": 0,
            "energy_pool": 10.0,
            "memory_used": 48,
            "free_memory": 452,
            "energy_balance_error": 0.0,
            "history": [{"tick": 0}],
            "genealogy": [{"organism_id": 1}],
        }

        record = compact_run_record(run)

        self.assertEqual(record["seed"], 7)
        self.assertEqual(record["config_hash"], "abc123")
        self.assertEqual(len(record["result_checksum"]), 64)
        self.assertNotIn("history", record)
        self.assertNotIn("genealogy", record)

    def test_validation_passes_complete_synthetic_campaign(self) -> None:
        seeds = [1, 2]
        run_template = {
            "seed": 1,
            "config_hash": "hash",
            "result_checksum": "a" * 64,
            "tick": 10,
            "active_population": 1,
            "births": 0,
            "deaths": 0,
            "memory_used": 16,
            "energy_balance_error": 0.0,
        }
        controls = {
            name: {
                "runs": [
                    {**run_template, "seed": seed, "control": name}
                    for seed in seeds
                ]
            }
            for name in REQUIRED_CONTROL_NAMES
        }
        sweeps = {
            f"parameter-{index}": {
                "cases": {
                    str(case): {
                        "runs": [
                            {
                                **run_template,
                                "seed": seed,
                                "control": f"parameter-{index}={case}",
                            }
                            for seed in seeds
                        ]
                    }
                    for case in range(3)
                }
            }
            for index in range(9)
        }
        campaign = {
            "format": EVIDENCE_CAMPAIGN_FORMAT,
            "seed_list": seeds,
            "protocol": {
                "runs_per_condition": 2,
                "energy_balance_tolerance": 1e-7,
            },
            "controls": controls,
            "sweeps": sweeps,
        }

        validation = validate_campaign(campaign)

        self.assertTrue(validation["passed"])
        self.assertEqual(validation["control_conditions"], 6)
        self.assertEqual(validation["sensitivity_parameters"], 9)
        self.assertEqual(validation["sensitivity_cases"], 27)
        self.assertEqual(validation["total_runs"], 66)

    def test_validation_rejects_invariant_failure(self) -> None:
        campaign = {
            "format": EVIDENCE_CAMPAIGN_FORMAT,
            "seed_list": [1],
            "protocol": {
                "runs_per_condition": 1,
                "energy_balance_tolerance": 1e-7,
            },
            "controls": {
                name: {
                    "runs": [
                        {
                            "control": name,
                            "seed": 1,
                            "config_hash": "hash",
                            "result_checksum": "a" * 64,
                            "tick": 10,
                            "active_population": 1,
                            "births": 0,
                            "deaths": 0,
                            "memory_used": 16,
                            "energy_balance_error": 1e-3,
                        }
                    ]
                }
                for name in REQUIRED_CONTROL_NAMES
            },
            "sweeps": {
                f"parameter-{index}": {
                    "cases": {
                        str(case): {
                            "runs": [
                                {
                                    "control": f"parameter-{index}={case}",
                                    "seed": 1,
                                    "config_hash": "hash",
                                    "result_checksum": "a" * 64,
                                    "tick": 10,
                                    "active_population": 1,
                                    "births": 0,
                                    "deaths": 0,
                                    "memory_used": 16,
                                    "energy_balance_error": 0.0,
                                }
                            ]
                        }
                        for case in range(3)
                    }
                }
                for index in range(9)
            },
        }

        validation = validate_campaign(campaign)

        self.assertFalse(validation["passed"])
        self.assertGreater(validation["energy_invariant_failures"], 0)

    def test_real_smoke_campaign_passes(self) -> None:
        config = CORE_SCHEMA.defaults()
        config.update(
            {
                "run.max_ticks": 2,
                "population.initial_size": 1,
                "world.initial_energy": 100.0,
            }
        )

        campaign = run_evidence_campaign(config, [3])

        self.assertTrue(campaign["validation"]["passed"])
        self.assertTrue(campaign["reproducibility_check"]["identical"])
        self.assertEqual(campaign["validation"]["total_runs"], 33)


if __name__ == "__main__":
    unittest.main()
