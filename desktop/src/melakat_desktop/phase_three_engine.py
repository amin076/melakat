from __future__ import annotations

from typing import Any, Callable

from .phase_three_contract import (
    PHASE_THREE_ENGINE_VERSION,
    PHASE_THREE_MEASUREMENT_VERSION,
    PHASE_THREE_WORLD_CONTRACT_VERSION,
)
from .phase_two_engine import PhaseTwoEngine
from .protocol import make_event

SUPPORTED_RESOURCE_DISTRIBUTIONS = {"uniform", "center_patch"}


class PhaseThreeEngine(PhaseTwoEngine):
    """First Phase Three reference engine.

    Phase Three preserves the Phase Two VM, reproduction, spatial topology,
    resource capture, movement and accounting rules. The first intervention
    changes only how the same total initial and incoming local resource is
    allocated across the existing grid.
    """

    engine_version = PHASE_THREE_ENGINE_VERSION
    measurement_version = PHASE_THREE_MEASUREMENT_VERSION
    world_contract_version = PHASE_THREE_WORLD_CONTRACT_VERSION

    def __init__(
        self,
        config: dict[str, Any],
        emit: Callable[[dict[str, Any]], None],
    ):
        self.resource_distribution_mode = str(
            config.get("world.resource_distribution_mode", "uniform")
        )
        if self.resource_distribution_mode not in SUPPORTED_RESOURCE_DISTRIBUTIONS:
            raise ValueError(
                f"unsupported_resource_distribution:{self.resource_distribution_mode}"
            )

        self.resource_patch_fraction = float(
            config.get("world.resource_patch_fraction", 0.30)
        )
        self.resource_patch_contrast = float(
            config.get("world.resource_patch_contrast", 4.0)
        )
        if not 0.0 < self.resource_patch_fraction <= 1.0:
            raise ValueError("resource_patch_fraction_must_be_in_0_1")
        if self.resource_patch_contrast < 1.0:
            raise ValueError("resource_patch_contrast_must_be_at_least_one")

        self.resource_weights: list[float] = []
        super().__init__(config, emit)

        if self.resource_distribution_mode != "uniform":
            if self.resource_field is None:
                raise ValueError(
                    "heterogeneous_resource_distribution_requires_local_resources"
                )
            self.resource_weights = self._build_center_patch_weights()
            self.resource_field.redistribute_weighted(self.resource_weights)
            # Replace the uniform initialization sample created by Phase Two with
            # the actual Phase Three starting state. No Phase Two code is changed.
            self.history = []
            self._record_history(force=True)

    def _build_center_patch_weights(self) -> list[float]:
        if self.resource_field is None:
            return []

        cols = self.resource_field.cols
        rows = self.resource_field.rows
        half_fraction = self.resource_patch_fraction / 2.0
        weights: list[float] = []
        inside_indices: list[int] = []
        closest_index = 0
        closest_distance = float("inf")

        for row in range(rows):
            y = (row + 0.5) / rows
            for col in range(cols):
                x = (col + 0.5) / cols
                index = row * cols + col
                dx = abs(x - 0.5)
                dy = abs(y - 0.5)
                distance = dx * dx + dy * dy
                if distance < closest_distance:
                    closest_distance = distance
                    closest_index = index
                inside = dx <= half_fraction and dy <= half_fraction
                if inside:
                    inside_indices.append(index)
                weights.append(self.resource_patch_contrast if inside else 1.0)

        # Very small patch fractions on coarse grids could otherwise select no
        # cell. Keep the intervention defined and deterministic by selecting the
        # single cell whose center is closest to the world center.
        if not inside_indices and weights:
            weights[closest_index] = self.resource_patch_contrast

        return weights

    def _resource_allocation_cv(self) -> float:
        """CV of the imposed renewal weights, not the evolving resource state."""

        if self.resource_distribution_mode == "uniform" or not self.resource_weights:
            return 0.0
        mean = sum(self.resource_weights) / len(self.resource_weights)
        if mean <= 0.0:
            return 0.0
        variance = sum(
            (weight - mean) ** 2 for weight in self.resource_weights
        ) / len(self.resource_weights)
        return variance ** 0.5 / mean

    def step(self) -> None:
        # The uniform Phase Three control deliberately delegates to the exact
        # Phase Two step path. Only heterogeneous renewal uses new dynamics.
        if self.resource_field is None or self.resource_distribution_mode == "uniform":
            super().step()
            return
        if self.finished:
            return
        maximum_ticks = int(self.config["run.max_ticks"])
        if self.tick >= maximum_ticks:
            self._finish("max_ticks")
            return

        self.tick += 1
        energy_input = float(self.config["world.energy_input_per_tick"])
        self.resource_field.renew_weighted(energy_input, self.resource_weights)
        self.ledger["energy_input"] += energy_input
        self.emit(
            make_event(
                "resource_renewed",
                amount=round(energy_input, 6),
                resource_total=round(self.resource_field.total(), 6),
                resource_distribution_mode=self.resource_distribution_mode,
            )
        )

        schedule = self._active()
        self.rng.shuffle(schedule)
        for organism in schedule:
            if organism.alive:
                organism.age += 1
                self._execute_one(organism)

        self.max_population = max(self.max_population, len(self._active()))
        self._record_history()
        if self.emit_snapshots:
            self.emit(
                make_event("tick", snapshot=self.snapshot(), metrics=self.metrics())
            )
        if self.tick >= maximum_ticks:
            self._finish("max_ticks")

    def snapshot(self) -> dict[str, Any]:
        snapshot = super().snapshot()
        snapshot["resource_distribution_mode"] = self.resource_distribution_mode
        if self.resource_field is not None:
            snapshot["resource_distribution"] = {
                "mode": self.resource_distribution_mode,
                "patch_fraction": round(self.resource_patch_fraction, 6),
                "patch_contrast": round(self.resource_patch_contrast, 6),
                "allocation_cv": round(self._resource_allocation_cv(), 6),
            }
        return snapshot

    def metrics(self) -> dict[str, Any]:
        metrics = super().metrics()
        metrics["resource_distribution_mode"] = self.resource_distribution_mode
        metrics["resource_allocation_cv"] = round(
            self._resource_allocation_cv(), 6
        )
        if self.resource_field is not None:
            # This is the observed resource-field state after organism capture,
            # death release and renewal. It is distinct from allocation_cv.
            metrics["resource_heterogeneity_cv"] = round(
                self.resource_field.coefficient_of_variation(), 6
            )
            metrics["local_resource_maximum"] = round(
                self.resource_field.maximum(), 6
            )
        else:
            metrics["resource_heterogeneity_cv"] = 0.0
            metrics["local_resource_maximum"] = 0.0
        return metrics
