from __future__ import annotations

import sys
from pathlib import Path

from . import experiment_runner
from .phase_three_experiment_support import (
    is_phase_three_spec,
    phase_three_experiment_support,
)


def _spec_path_from_argv(argv: list[str]) -> Path | None:
    if len(argv) < 3:
        return None
    if argv[1] not in {"run", "validate"}:
        return None
    return Path(argv[2])


def main() -> None:
    spec_path = _spec_path_from_argv(sys.argv)
    if spec_path is None:
        experiment_runner.main()
        return

    spec = experiment_runner.load_experiment_spec(spec_path)
    if not is_phase_three_spec(spec):
        experiment_runner.main()
        return

    with phase_three_experiment_support():
        experiment_runner.main()


if __name__ == "__main__":
    main()
