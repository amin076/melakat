import json
import unittest
from pathlib import Path

from melakat_desktop import experiment_runner
from melakat_desktop.phase_three_engine import PhaseThreeEngine
from melakat_desktop.phase_three_experiment_support import phase_three_experiment_support
from melakat_desktop.phase_two_vm import PhaseTwoOpcode, PhaseTwoVirtualMachine
from melakat_desktop.vm import Instruction, Opcode, VMConfig, VMState


REPO_ROOT = Path(__file__).resolve().parents[2]
FULL_SPEC = REPO_ROOT / "experiments" / "phase-four" / "resource-sensing-with-movement.json"
PREFLIGHT_SPEC = (
    REPO_ROOT / "experiments" / "phase-four" / "resource-sensing-with-movement-preflight.json"
)
SMOKE_SPEC = REPO_ROOT / "experiments" / "phase-four" / "resource-sensing-with-movement-smoke.json"
CONTROL = "sensing-execution-off-movement-on"
TREATMENT = "sensing-execution-on-movement-on"


class PhaseFourSensingMovementGateTests(unittest.TestCase):
    @staticmethod
    def _load(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_specs_differ_only_in_sensing_execution(self) -> None:
        for path, expected_runs in (
            (FULL_SPEC, 60),
            (PREFLIGHT_SPEC, 16),
            (SMOKE_SPEC, 16),
        ):
            with self.subTest(spec=path.name):
                spec = self._load(path)
                with phase_three_experiment_support():
                    plan = experiment_runner.build_experiment_plan(spec)

                self.assertEqual(plan["run_count"], expected_runs)
                self.assertEqual(
                    [condition["name"] for condition in plan["conditions"]],
                    [CONTROL, TREATMENT],
                )

                base = plan["base_config"]
                self.assertTrue(base["world.resource_sensing_mutation_enabled"])
                self.assertTrue(base["world.movement_enabled"])
                self.assertTrue(base["world.movement_mutation_enabled"])
                self.assertTrue(base["world.atomic_movement_payment_enabled"])
                self.assertEqual(base["mutation.movement_step_rate"], 0.5)
                self.assertEqual(base["world.resource_distribution_mode"], "center_patch")

                effective = []
                for condition in plan["conditions"]:
                    config = dict(base)
                    config.update(condition["overrides"])
                    effective.append(config)

                differing = {
                    key
                    for key in set(effective[0]) | set(effective[1])
                    if effective[0].get(key) != effective[1].get(key)
                }
                self.assertEqual(differing, {"world.resource_sensing_enabled"})
                self.assertFalse(effective[0]["world.resource_sensing_enabled"])
                self.assertTrue(effective[1]["world.resource_sensing_enabled"])

                control_engine = PhaseThreeEngine(effective[0], lambda _event: None)
                treatment_engine = PhaseThreeEngine(effective[1], lambda _event: None)
                for engine in (control_engine, treatment_engine):
                    self.assertTrue(engine.resource_sensing_mutation_enabled)
                    self.assertTrue(engine.movement_enabled)
                    self.assertTrue(engine.movement_mutation_enabled)
                    self.assertTrue(engine.atomic_movement_payment_enabled)
                self.assertFalse(control_engine.resource_sensing_enabled)
                self.assertTrue(treatment_engine.resource_sensing_enabled)

    def test_full_duration_preflight_matches_full_campaign_configuration(self) -> None:
        full = self._load(FULL_SPEC)
        preflight = self._load(PREFLIGHT_SPEC)

        self.assertEqual(preflight["base_config"], full["base_config"])
        self.assertEqual(preflight["conditions"], full["conditions"])
        self.assertEqual(preflight["reproducibility"], full["reproducibility"])
        self.assertEqual(preflight["seeds"]["start"], full["seeds"]["start"])
        self.assertEqual(preflight["seeds"]["count"], 8)
        self.assertEqual(full["seeds"]["count"], 30)
        self.assertEqual(preflight["base_config"]["run.max_ticks"], 2000)

    def test_local_scalar_sensing_can_gate_move_reachability_via_control_flow(self) -> None:
        program = (
            Instruction(PhaseTwoOpcode.SENSE_RESOURCE, a=0),
            Instruction(Opcode.JUMP_IF_ZERO, a=4),
            Instruction(PhaseTwoOpcode.MOVE_X, b=1),
            Instruction(Opcode.HALT),
            Instruction(Opcode.HALT),
        )
        config = VMConfig(word_bits=8, register_count=4, memory_size=8)

        def run(*, sensing_enabled: bool, sensed_resource: float):
            state = VMState(
                registers=[0] * config.register_count,
                memory=[0] * config.memory_size,
                replication_buffer=[None] * len(program),
            )
            movement_calls = []

            def move(axis: str, requested: float):
                movement_calls.append((axis, requested))
                return abs(requested), 0

            vm = PhaseTwoVirtualMachine(
                program,
                config,
                state,
                sense_resource=lambda: sensed_resource,
                move=move,
                sensing_enabled=sensing_enabled,
                movement_enabled=True,
            )
            result = vm.run(5)
            return result, movement_calls, vm.state.registers[0]

        disabled, disabled_moves, disabled_register = run(
            sensing_enabled=False,
            sensed_resource=9.0,
        )
        zero_resource, zero_moves, zero_register = run(
            sensing_enabled=True,
            sensed_resource=0.0,
        )
        positive_resource, positive_moves, positive_register = run(
            sensing_enabled=True,
            sensed_resource=9.0,
        )

        self.assertEqual(disabled_register, 0)
        self.assertEqual(disabled.resource_sense_operations, 0)
        self.assertEqual(disabled.movement_operations, 0)
        self.assertEqual(disabled_moves, [])

        self.assertEqual(zero_register, 0)
        self.assertEqual(zero_resource.resource_sense_operations, 1)
        self.assertEqual(zero_resource.movement_operations, 0)
        self.assertEqual(zero_moves, [])

        self.assertEqual(positive_register, 9)
        self.assertEqual(positive_resource.resource_sense_operations, 1)
        self.assertEqual(positive_resource.movement_operations, 1)
        self.assertEqual(positive_resource.movement_nonzero_operations, 1)
        self.assertEqual(positive_moves, [("x", 1.0)])

        # Sensing changes whether the MOVE instruction is reached. It does not
        # supply a direction: the realized +X request still comes from MOVE_X's
        # fixed immediate operand b=1.

    def test_smoke_campaign_has_sensing_exposure_locomotion_and_atomic_accounting(self) -> None:
        spec = self._load(SMOKE_SPEC)
        with phase_three_experiment_support():
            campaign = experiment_runner.run_experiment(spec, progress=False)

        self.assertTrue(campaign["validation"]["passed"])
        self.assertEqual(campaign["validation"]["expected_runs"], 16)
        self.assertTrue(campaign["validation"]["reproducibility"]["identical"])

        control = [run for run in campaign["runs"] if run["condition"] == CONTROL]
        treatment = [run for run in campaign["runs"] if run["condition"] == TREATMENT]
        self.assertEqual(len(control), 8)
        self.assertEqual(len(treatment), 8)

        control_senses = sum(int(run.get("resource_sense_operations", 0)) for run in control)
        treatment_senses = sum(int(run.get("resource_sense_operations", 0)) for run in treatment)
        self.assertEqual(control_senses, 0)
        self.assertGreater(treatment_senses, 0)

        control_nonzero_moves = sum(
            int(run.get("movement_nonzero_operations", 0)) for run in control
        )
        treatment_nonzero_moves = sum(
            int(run.get("movement_nonzero_operations", 0)) for run in treatment
        )
        self.assertGreater(control_nonzero_moves, 0)
        self.assertGreater(treatment_nonzero_moves, 0)

        for run in campaign["runs"]:
            self.assertTrue(run.get("atomic_movement_payment_enabled"))
            distance = float(run.get("movement_distance", 0.0))
            paid = float(run.get("movement_energy_cost", 0.0))
            self.assertGreaterEqual(paid + 1e-9, distance * 0.1)
            self.assertLessEqual(abs(float(run["energy_balance_error"])), 1e-7)
            self.assertLessEqual(
                abs(float(run["local_resource_balance_error"])),
                1e-7,
            )

        # Smoke success establishes exposure and accounting only. It deliberately
        # makes no assertion that paired ecological/spatial outcomes differ.


if __name__ == "__main__":
    unittest.main()
