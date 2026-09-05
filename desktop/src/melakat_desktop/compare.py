from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analysis import compare_artifacts
from .artifacts import load_run_artifact, write_json


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare two Melakat run artifacts."
    )
    parser.add_argument("first", type=Path)
    parser.add_argument("second", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    first = load_run_artifact(args.first)
    second = load_run_artifact(args.second)
    report = compare_artifacts(first, second)

    if args.output:
        write_json(args.output, report)
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
