from __future__ import annotations

import hashlib
import math
import random
from collections.abc import Iterable
from typing import Any

SPATIAL_OCCUPANCY_GRID_SIZE = 10
SPATIAL_RNG_STREAM = "offspring-placement-v1"
SUPPORTED_BOUNDARIES = ("reflective", "toroidal")


def derive_spatial_seed(seed: int, world_contract_version: str) -> int:
    payload = f"{int(seed)}:{world_contract_version}:{SPATIAL_RNG_STREAM}"
    digest = hashlib.sha256(payload.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def reflect_coordinate(value: float, maximum: float) -> float:
    maximum = float(maximum)
    if maximum <= 0.0:
        raise ValueError("reflective boundary maximum must be positive")
    period = 2.0 * maximum
    wrapped = float(value) % period
    if wrapped <= maximum:
        return wrapped
    return period - wrapped


def toroidal_coordinate(value: float, maximum: float) -> float:
    maximum = float(maximum)
    if maximum <= 0.0:
        raise ValueError("toroidal boundary maximum must be positive")
    return float(value) % maximum


def apply_boundary(
    value: float,
    maximum: float,
    model: str,
) -> tuple[float, int]:
    contacted = int(float(value) < 0.0 or float(value) > float(maximum))
    if model == "reflective":
        return reflect_coordinate(value, maximum), contacted
    if model == "toroidal":
        return toroidal_coordinate(value, maximum), contacted
    raise ValueError(f"unsupported_boundary_model:{model}")


def local_radial_position(
    *,
    parent_x: float,
    parent_y: float,
    radius: float,
    width: float,
    height: float,
    rng: random.Random,
    boundary_model: str = "reflective",
) -> tuple[float, float, int]:
    radius = max(0.0, float(radius))
    angle = 2.0 * math.pi * rng.random()
    distance = radius * math.sqrt(rng.random())
    raw_x = float(parent_x) + distance * math.cos(angle)
    raw_y = float(parent_y) + distance * math.sin(angle)
    x, x_contact = apply_boundary(raw_x, width, boundary_model)
    y, y_contact = apply_boundary(raw_y, height, boundary_model)
    return x, y, x_contact + y_contact


def local_neighbor_count(
    organism: Any,
    organisms: Iterable[Any],
    radius: float,
) -> int:
    radius = max(0.0, float(radius))
    return sum(
        other.alive
        and other.organism_id != organism.organism_id
        and math.hypot(organism.x - other.x, organism.y - other.y) <= radius
        for other in organisms
    )


def population_spatial_metrics(
    organisms: Iterable[Any],
    *,
    width: float,
    height: float,
    neighborhood_radius: float,
    grid_size: int = SPATIAL_OCCUPANCY_GRID_SIZE,
) -> dict[str, float | int]:
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
            math.hypot(organism.x - other.x, organism.y - other.y)
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
        x_index = min(grid_size - 1, max(0, int((organism.x / width) * grid_size)))
        y_index = min(grid_size - 1, max(0, int((organism.y / height) * grid_size)))
        occupied.add((x_index, y_index))

    return {
        "mean_local_neighbors": round(sum(neighbor_counts) / len(neighbor_counts), 6),
        "mean_nearest_neighbor_distance": round(
            sum(nearest_distances) / len(nearest_distances), 6
        ),
        "occupied_spatial_bins": len(occupied),
        "spatial_occupancy_fraction": round(
            len(occupied) / float(grid_size * grid_size), 6
        ),
    }
