from __future__ import annotations

import hashlib
import math
import random
from collections.abc import Iterable
from typing import Any

SPATIAL_OCCUPANCY_GRID_SIZE = 10
SPATIAL_RNG_STREAM = "offspring-placement-v1"


def derive_spatial_seed(seed: int, world_contract_version: str) -> int:
    """Derive a stable RNG seed for spatial-only stochastic decisions.

    Phase Two keeps this stream separate from the historical engine RNG so
    spatial placement cannot silently change scheduler or mutation randomness.
    """

    payload = f"{int(seed)}:{world_contract_version}:{SPATIAL_RNG_STREAM}"
    digest = hashlib.sha256(payload.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def reflect_coordinate(value: float, maximum: float) -> float:
    """Reflect a continuous coordinate into the closed interval [0, maximum]."""

    maximum = float(maximum)
    if maximum <= 0.0:
        raise ValueError("reflective boundary maximum must be positive")

    period = 2.0 * maximum
    wrapped = float(value) % period
    if wrapped <= maximum:
        return wrapped
    return period - wrapped


def local_radial_position(
    *,
    parent_x: float,
    parent_y: float,
    radius: float,
    width: float,
    height: float,
    rng: random.Random,
) -> tuple[float, float, int]:
    """Place an offspring uniformly by area inside a radius around its parent.

    Any attempted crossing of the rectangular world is reflected. The returned
    contact count records how many coordinate axes crossed a boundary before
    reflection (0, 1, or 2 for this placement event).
    """

    radius = max(0.0, float(radius))
    angle = 2.0 * math.pi * rng.random()
    distance = radius * math.sqrt(rng.random())
    raw_x = float(parent_x) + distance * math.cos(angle)
    raw_y = float(parent_y) + distance * math.sin(angle)

    contacts = int(raw_x < 0.0 or raw_x > width) + int(
        raw_y < 0.0 or raw_y > height
    )
    return (
        reflect_coordinate(raw_x, width),
        reflect_coordinate(raw_y, height),
        contacts,
    )


def population_spatial_metrics(
    organisms: Iterable[Any],
    *,
    width: float,
    height: float,
    neighborhood_radius: float,
    grid_size: int = SPATIAL_OCCUPANCY_GRID_SIZE,
) -> dict[str, float | int]:
    """Measure continuous-space occupancy and local crowding for active organisms."""

    active = [organism for organism in organisms if organism.alive]
    if not active:
        return {
            "mean_local_neighbors": 0.0,
            "mean_nearest_neighbor_distance": 0.0,
            "occupied_spatial_bins": 0,
            "spatial_occupancy_fraction": 0.0,
        }

    radius = max(0.0, float(neighborhood_radius))
    neighbor_counts: list[int] = []
    nearest_distances: list[float] = []

    for index, organism in enumerate(active):
        distances = [
            math.hypot(
                organism.x - other.x,
                organism.y - other.y,
            )
            for other_index, other in enumerate(active)
            if other_index != index
        ]
        neighbor_counts.append(sum(distance <= radius for distance in distances))
        nearest_distances.append(min(distances) if distances else 0.0)

    grid_size = max(1, int(grid_size))
    width = float(width)
    height = float(height)
    occupied: set[tuple[int, int]] = set()
    for organism in active:
        x_index = min(
            grid_size - 1,
            max(0, int((organism.x / width) * grid_size)),
        )
        y_index = min(
            grid_size - 1,
            max(0, int((organism.y / height) * grid_size)),
        )
        occupied.add((x_index, y_index))

    return {
        "mean_local_neighbors": round(
            sum(neighbor_counts) / len(neighbor_counts),
            6,
        ),
        "mean_nearest_neighbor_distance": round(
            sum(nearest_distances) / len(nearest_distances),
            6,
        ),
        "occupied_spatial_bins": len(occupied),
        "spatial_occupancy_fraction": round(
            len(occupied) / float(grid_size * grid_size),
            6,
        ),
    }
