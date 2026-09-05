from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LocalResourceField:
    width: float
    height: float
    cols: int
    rows: int

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("resource_field_extent_must_be_positive")
        if self.cols < 1 or self.rows < 1:
            raise ValueError("resource_field_grid_must_be_positive")
        self.values = [0.0] * (self.cols * self.rows)
        self.initial_resource = 0.0
        self.input_resource = 0.0
        self.captured_resource = 0.0
        self.released_resource = 0.0

    def _cell(self, x: float, y: float) -> tuple[int, int]:
        bounded_x = min(max(float(x), 0.0), self.width)
        bounded_y = min(max(float(y), 0.0), self.height)
        col = min(self.cols - 1, int((bounded_x / self.width) * self.cols))
        row = min(self.rows - 1, int((bounded_y / self.height) * self.rows))
        return col, row

    def _index(self, x: float, y: float) -> int:
        col, row = self._cell(x, y)
        return row * self.cols + col

    def seed_uniform(self, total: float) -> None:
        total = max(0.0, float(total))
        per_cell = total / len(self.values)
        self.values = [per_cell] * len(self.values)
        self.initial_resource = total
        self.input_resource = 0.0
        self.captured_resource = 0.0
        self.released_resource = 0.0

    def renew_uniform(self, total: float) -> None:
        total = max(0.0, float(total))
        if total <= 0.0:
            return
        per_cell = total / len(self.values)
        for index in range(len(self.values)):
            self.values[index] += per_cell
        self.input_resource += total

    def capture(self, x: float, y: float, requested: float) -> float:
        requested = max(0.0, float(requested))
        index = self._index(x, y)
        captured = min(self.values[index], requested)
        self.values[index] -= captured
        self.captured_resource += captured
        return captured

    def release(self, x: float, y: float, amount: float) -> None:
        amount = max(0.0, float(amount))
        if amount <= 0.0:
            return
        self.values[self._index(x, y)] += amount
        self.released_resource += amount

    def at(self, x: float, y: float) -> float:
        return self.values[self._index(x, y)]

    def total(self) -> float:
        return sum(self.values)

    def minimum(self) -> float:
        return min(self.values, default=0.0)

    def balance_error(self) -> float:
        expected = (
            self.initial_resource
            + self.input_resource
            + self.released_resource
            - self.captured_resource
        )
        return expected - self.total()

    def snapshot(self) -> dict[str, object]:
        return {
            "cols": self.cols,
            "rows": self.rows,
            "width": self.width,
            "height": self.height,
            "values": [round(value, 6) for value in self.values],
            "total": round(self.total(), 6),
            "minimum": round(self.minimum(), 6),
            "balance_error": round(self.balance_error(), 10),
        }

    def ledger(self) -> dict[str, float]:
        return {
            "resource_initial": round(self.initial_resource, 6),
            "resource_input": round(self.input_resource, 6),
            "resource_captured": round(self.captured_resource, 6),
            "resource_released_on_death": round(self.released_resource, 6),
            "resource_total": round(self.total(), 6),
        }
