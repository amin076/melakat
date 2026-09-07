from __future__ import annotations

from typing import Any

PHASE_THREE_WORLD_CONTRACT_VERSION = "phase-three-environment-0.1"
PHASE_THREE_ENGINE_VERSION = "phase-three-vm-0.1"
PHASE_THREE_MOVEMENT_ENCODING_ENGINE_VERSION = "phase-three-vm-0.2"
PHASE_THREE_MEASUREMENT_VERSION = "phase-three-measurement-0.2"
PHASE_TWO_FROZEN_WORLD_CONTRACT_VERSION = "phase-two-spatial-0.7"
PHASE_TWO_FROZEN_ENGINE_VERSION = "phase-two-vm-0.7"
PHASE_TWO_FROZEN_MEASUREMENT_VERSION = "phase-two-measurement-0.1"

PHASE_THREE_WORLD_CONTRACT: dict[str, Any] = {
    "version": PHASE_THREE_WORLD_CONTRACT_VERSION,
    "engine_version": PHASE_THREE_ENGINE_VERSION,
    "measurement_version": PHASE_THREE_MEASUREMENT_VERSION,
    "scientific_question": (
        "Holding total resource input and other Phase Two rules fixed, does spatial "
        "heterogeneity in resource placement change population and lineage dynamics?"
    ),
    "frozen_reference": {
        "world_contract": PHASE_TWO_FROZEN_WORLD_CONTRACT_VERSION,
        "engine": PHASE_TWO_FROZEN_ENGINE_VERSION,
        "measurement": PHASE_TWO_FROZEN_MEASUREMENT_VERSION,
        "rule": "Phase Two code and accepted evidence remain a frozen reference.",
    },
    "new_causal_mechanism": {
        "name": "spatial_resource_heterogeneity",
        "control": "uniform",
        "first_intervention": "center_patch",
        "conservation": (
            "Initial resource and per-tick resource input totals are unchanged; only "
            "their spatial allocation across existing resource cells changes."
        ),
    },
    "center_patch": {
        "geometry": "axis-aligned central rectangle measured as a fraction of world extent",
        "contrast": "cells inside the patch receive a multiplicative allocation weight",
        "randomness": "none; patch geometry is deterministic and identical across matched seeds",
    },
    "later_interventions": {
        "movement_step_encoding": {
            "engine_version": PHASE_THREE_MOVEMENT_ENCODING_ENGINE_VERSION,
            "config": "mutation.movement_step_rate",
            "default": 0.0,
            "scope": (
                "Optional Phase Three-only mutation of the signed immediate on existing "
                "MOVE_X/MOVE_Y instructions. A zero rate preserves the accepted Phase Three "
                "0.1 hereditary representation exactly."
            ),
        }
    },
    "preserved_absences": [
        "resource diffusion",
        "organism-produced environmental resources",
        "predation",
        "cooperation rules",
        "explicit fitness objective",
        "host-selected successful organisms",
        "machine learning",
    ],
    "comparison_rule": (
        "Phase Three experiments must use matched seeds and hold total resource input, "
        "initial conditions, mutation, reproduction, VM, memory and movement settings "
        "constant unless a later intervention explicitly changes one of them."
    ),
}
