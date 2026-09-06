import unittest

from melakat_desktop.parameters import CORE_SCHEMA
from melakat_desktop.phase_three_contract import (
    PHASE_THREE_ENGINE_VERSION,
    PHASE_THREE_MEASUREMENT_VERSION,
    PHASE_THREE_WORLD_CONTRACT,
    PHASE_THREE_WORLD_CONTRACT_VERSION,
)
from melakat_desktop.phase_three_engine import PhaseThreeEngine
from melakat_desktop.phase_two_engine import PhaseTwoEngine
from melakat_desktop.resources import LocalResourceField
from melakat_desktop.worker import create_engine


class PhaseThreeEnvironmentTests(unittest.TestCase):
    @staticmethod
    def config(mode: str = "uniform", *, ticks: int = 100) -> dict:
        config = CORE_SCHEMA.defaults()
        config.update(
            {
                "run.engine_backend": "phase-three-vm",
                "run.max_ticks": ticks,
                "run.seed": 7,
                "run.emit_snapshots": False,
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
                "world.resource_distribution_mode": mode,
                "world.resource_patch_fraction": 0.30,
                "world.resource_patch_contrast": 4.0,
            }
        )
        return CORE_SCHEMA.validate(config)

    @staticmethod
    def run(engine) -> None:
        while not engine.finished:
            engine.step()

    def test_phase_three_contract_defines_one_new_causal_mechanism(self) -> None:
        self.assertEqual(
            PHASE_THREE_WORLD_CONTRACT_VERSION,
            "phase-three-environment-0.1",
        )
        self.assertEqual(PHASE_THREE_ENGINE_VERSION, "phase-three-vm-0.1")
        self.assertEqual(
            PHASE_THREE_MEASUREMENT_VERSION,
            "phase-three-measurement-0.1",
        )
        mechanism = PHASE_THREE_WORLD_CONTRACT["new_causal_mechanism"]
        self.assertEqual(mechanism["name"], "spatial_resource_heterogeneity")
        self.assertEqual(mechanism["control"], "uniform")
        self.assertEqual(mechanism["first_intervention"], "center_patch")

    def test_worker_exposes_phase_three_backend(self) -> None:
        engine = create_engine(self.config(), lambda _event: None)
        self.assertIsInstance(engine, PhaseThreeEngine)

    def test_weighted_resource_allocation_is_conservative(self) -> None:
        field = LocalResourceField(width=20, height=10, cols=4, rows=2)
        weights = [1.0, 1.0, 4.0, 4.0, 1.0, 1.0, 4.0, 4.0]
        field.seed_weighted(100.0, weights)
        self.assertAlmostEqual(field.total(), 100.0, places=10)
        self.assertAlmostEqual(field.balance_error(), 0.0, places=10)
        self.assertGreater(field.maximum(), field.minimum())

        field.renew_weighted(12.5, weights)
        self.assertAlmostEqual(field.total(), 112.5, places=10)
        self.assertAlmostEqual(field.input_resource, 12.5, places=10)
        self.assertAlmostEqual(field.balance_error(), 0.0, places=10)

    def test_center_patch_changes_distribution_not_total_initial_resource(self) -> None:
        uniform = PhaseThreeEngine(self.config("uniform"), lambda _event: None)
        patchy = PhaseThreeEngine(self.config("center_patch"), lambda _event: None)
        assert uniform.resource_field is not None
        assert patchy.resource_field is not None

        self.assertAlmostEqual(
            uniform.resource_field.total(),
            patchy.resource_field.total(),
            places=10,
        )
        self.assertAlmostEqual(uniform.resource_field.total(), 1000.0, places=10)
        self.assertAlmostEqual(uniform.resource_field.coefficient_of_variation(), 0.0, places=10)
        self.assertGreater(patchy.resource_field.coefficient_of_variation(), 0.0)
        self.assertGreater(patchy.resource_field.maximum(), patchy.resource_field.minimum())

    def test_uniform_phase_three_control_preserves_phase_two_dynamics(self) -> None:
        phase_three_config = self.config("uniform", ticks=150)
        phase_two_config = dict(phase_three_config)
        phase_two_config["run.engine_backend"] = "phase-two-vm"
        phase_two_config.pop("world.resource_distribution_mode")
        phase_two_config.pop("world.resource_patch_fraction")
        phase_two_config.pop("world.resource_patch_contrast")

        phase_two = PhaseTwoEngine(phase_two_config, lambda _event: None)
        phase_three = PhaseThreeEngine(phase_three_config, lambda _event: None)
        self.run(phase_two)
        self.run(phase_three)

        keys = (
            "tick",
            "active_population",
            "births",
            "deaths",
            "max_population",
            "historical_genotypes",
            "active_lineages",
            "max_generation",
            "instructions_executed",
            "faults",
            "energy_pool",
            "memory_used",
            "free_memory",
            "energy_balance_error",
            "local_resource_total",
            "local_resource_minimum",
            "local_resource_balance_error",
            "death_reasons",
            "ledger",
            "genealogy",
            "genotype_catalog",
        )
        phase_two_summary = phase_two.summary()
        phase_three_summary = phase_three.summary()
        for key in keys:
            self.assertEqual(phase_two_summary[key], phase_three_summary[key], key)

        assert phase_two.resource_field is not None
        assert phase_three.resource_field is not None
        self.assertEqual(phase_two.resource_field.values, phase_three.resource_field.values)

    def test_patchy_run_is_deterministic_and_conservative(self) -> None:
        first = PhaseThreeEngine(self.config("center_patch", ticks=200), lambda _event: None)
        second = PhaseThreeEngine(self.config("center_patch", ticks=200), lambda _event: None)
        self.run(first)
        self.run(second)

        self.assertEqual(first.summary(), second.summary())
        self.assertLessEqual(abs(first.energy_balance_error()), 1e-7)
        assert first.resource_field is not None
        self.assertLessEqual(abs(first.resource_field.balance_error()), 1e-7)
        self.assertGreater(first.metrics()["resource_heterogeneity_cv"], 0.0)

    def test_heterogeneity_requires_local_resources(self) -> None:
        config = self.config("center_patch")
        config["world.local_resources_enabled"] = False
        with self.assertRaisesRegex(
            ValueError,
            "heterogeneous_resource_distribution_requires_local_resources",
        ):
            PhaseThreeEngine(config, lambda _event: None)


if __name__ == "__main__":
    unittest.main()
