import unittest

from melakat_desktop.analysis import analyze_summary, compare_artifacts


class AnalysisTests(unittest.TestCase):
    def _summary(self) -> dict:
        return {
            "tick": 10,
            "death_reasons": {"energy_exhausted_execution": 1},
            "genealogy": [
                {
                    "organism_id": 1,
                    "parent_id": None,
                    "lineage_id": 1,
                    "generation": 0,
                    "birth_tick": 0,
                    "death_tick": None,
                    "genome_hash": "aaaa",
                },
                {
                    "organism_id": 2,
                    "parent_id": 1,
                    "lineage_id": 1,
                    "generation": 1,
                    "birth_tick": 4,
                    "death_tick": 8,
                    "genome_hash": "bbbb",
                },
            ],
            "genotype_catalog": [
                {
                    "genome_hash": "aaaa",
                    "first_seen_tick": 0,
                    "genome": [],
                },
                {
                    "genome_hash": "bbbb",
                    "first_seen_tick": 4,
                    "genome": [],
                },
            ],
        }

    def test_analysis_reports_lineages_and_mutations(self) -> None:
        analysis = analyze_summary(self._summary())

        self.assertEqual(len(analysis["lineages"]), 1)
        self.assertEqual(analysis["lineages"][0]["organism_count"], 2)
        self.assertEqual(analysis["lineages"][0]["active_count"], 1)
        self.assertEqual(analysis["mutation_events"], 1)
        self.assertEqual(
            analysis["mutation_map"],
            [
                {
                    "parent_genome_hash": "aaaa",
                    "child_genome_hash": "bbbb",
                    "events": 1,
                }
            ],
        )
        self.assertEqual(analysis["genotypes"][1]["mutated_births"], 1)

    def test_compare_detects_seed_only_difference(self) -> None:
        first = {
            "config": {"run.seed": 1, "run.max_ticks": 10},
            "config_hash": "first",
            "summary": {"active_population": 2},
        }
        second = {
            "config": {"run.seed": 2, "run.max_ticks": 10},
            "config_hash": "second",
            "summary": {"active_population": 3},
        }

        report = compare_artifacts(first, second)

        self.assertFalse(report["same_artifact"])
        self.assertFalse(report["same_config"])
        self.assertTrue(report["same_config_except_seed"])
        self.assertEqual(
            report["metric_differences"][0]["metric"],
            "active_population",
        )


if __name__ == "__main__":
    unittest.main()
