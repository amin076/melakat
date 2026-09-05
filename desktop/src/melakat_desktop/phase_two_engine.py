from __future__ import annotations

from typing import Any, Callable

from .phase_zero_engine import PhaseZeroEngine
from .world_contract import WORLD_CONTRACT_VERSION


class PhaseTwoEngine(PhaseZeroEngine):
    """P2.1 contract wrapper around the frozen Phase One reference engine.

    No spatial law is active in P2.1. The wrapper intentionally delegates all
    scientific state transitions to PhaseZeroEngine so the homogeneous control
    keeps the exact Phase One execution and RNG sequence. P2.2 will introduce
    the first independently tested spatial mechanism.
    """

    engine_version = "phase-two-vm-0.1"
    world_contract_version = WORLD_CONTRACT_VERSION

    def __init__(
        self,
        config: dict[str, Any],
        emit: Callable[[dict[str, Any]], None],
    ):
        self.spatial_enabled = bool(config.get("world.spatial_enabled", False))
        if self.spatial_enabled:
            raise ValueError(
                "spatial_rules_not_implemented:p2.2_required"
            )
        super().__init__(config, emit)

    def snapshot(self) -> dict[str, Any]:
        snapshot = super().snapshot()
        snapshot["world_contract_version"] = self.world_contract_version
        snapshot["spatial_enabled"] = self.spatial_enabled
        return snapshot

    def metrics(self) -> dict[str, Any]:
        metrics = super().metrics()
        metrics["world_contract_version"] = self.world_contract_version
        metrics["spatial_enabled"] = self.spatial_enabled
        return metrics
