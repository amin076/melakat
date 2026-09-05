import csv
import json
import tempfile
import unittest
from pathlib import Path

from melakat_desktop.artifacts import (
    RUN_ARTIFACT_FORMAT,
    config_hash,
    load_run_artifact,
    make_run_artifact,
    write_history_csv,
    write_json,
    write_summary_csv,
)


class ArtifactTests(unittest.TestCase):
    def test_config_hash_is_order_independent(self) -> None:
        first = {"alpha": 1, "nested": {"beta": True}}
        second = {"nested": {"beta": True}, "alpha": 1}

        self.assertEqual(config_hash(first), config_hash(second))

    def test_artifact_and_csv_exports_are_readable(self) -> None:
        config = {"run.max_ticks": 5, "run.seed": 7}
        summary = {
            "seed": 7,
            "config_hash": config_hash(config),
            "engine_version": "phase-zero-vm-0.2",
            "measurement_version": "phase-one-measurement-0.1",
            "tick": 5,
            "active_population": 2,
            "births": 1,
            "deaths": 0,
            "max_population": 2,
            "active_genotypes": 1,
            "historical_genotypes": 1,
            "active_lineages": 1,
            "max_generation": 1,
            "instructions_executed": 10,
            "faults": 0,
            "blocked_divisions": 0,
            "waiting_for_memory": 0,
            "waiting_for_energy": 0,
            "energy_pool": 10.0,
            "memory_used": 32,
            "free_memory": 8,
            "energy_balance_error": 0.0,
            "history": [
                {
                    "tick": 0,
                    "active_population": 1,
                    "births": 0,
                    "deaths": 0,
                    "max_population": 1,
                    "active_genotypes": 1,
                    "historical_genotypes": 1,
                    "active_lineages": 1,
                    "max_generation": 0,
                    "instructions_executed": 0,
                    "faults": 0,
                    "blocked_divisions": 0,
                    "waiting_for_memory": 0,
                    "waiting_for_energy": 0,
                    "energy_pool": 10.0,
                    "memory_used": 16,
                    "free_memory": 24,
                    "energy_balance_error": 0.0,
                },
                {
                    "tick": 5,
                    "active_population": 2,
                    "births": 1,
                    "deaths": 0,
                    "max_population": 2,
                    "active_genotypes": 1,
                    "historical_genotypes": 1,
                    "active_lineages": 1,
                    "max_generation": 1,
                    "instructions_executed": 10,
                    "faults": 0,
                    "blocked_divisions": 0,
                    "waiting_for_memory": 0,
                    "waiting_for_energy": 0,
                    "energy_pool": 10.0,
                    "memory_used": 32,
                    "free_memory": 8,
                    "energy_balance_error": 0.0,
                },
            ],
        }
        summary["control"] = "baseline"
        artifact = make_run_artifact(config, summary)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            json_path = root / "nested" / "run.json"
            summary_path = root / "nested" / "summary.csv"
            history_path = root / "nested" / "history.csv"

            write_json(json_path, artifact)
            write_summary_csv(summary_path, [summary])
            write_history_csv(history_path, [summary])

            loaded = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(loaded["format"], RUN_ARTIFACT_FORMAT)
            self.assertEqual(loaded["config_hash"], config_hash(config))
            self.assertIn("analysis", loaded["summary"])
            self.assertEqual(loaded["summary"]["mutation_events"], 0)
            self.assertEqual(
                load_run_artifact(json_path),
                loaded,
            )

            with summary_path.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["control"], "baseline")
            self.assertEqual(rows[0]["seed"], "7")

            with history_path.open(encoding="utf-8", newline="") as handle:
                history_rows = list(csv.DictReader(handle))
            self.assertEqual(len(history_rows), 2)
            self.assertEqual(history_rows[-1]["tick"], "5")


if __name__ == "__main__":
    unittest.main()
