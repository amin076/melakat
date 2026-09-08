# Phase Five Structural Event-Rate Calibration

This directory records Gate 5C, an **exposure-only** calibration used to choose the structural mutation event rate before the full Phase Five causal campaign.

The pre-registered rule selected the lowest candidate that produced:

- at least 16 committed structural events;
- exposure in at least 6 of 8 runs;
- at least 4 duplications;
- at least 4 deletions;
- valid invariants and identical deterministic replay.

No genome-size, population, survival, reproduction, lineage, or preferred evolutionary outcome was permitted to influence rate selection.

| Rate | Committed | Exposed | Duplication | Deletion | Decision |
| ---: | ---: | ---: | ---: | ---: | --- |
| `0.01` | 11 | 6/8 | 6 | 5 | FAIL |
| `0.025` | 26 | 7/8 | 12 | 14 | **SELECTED** |
| `0.05` | 50 | 8/8 | 23 | 27 | PASS, not selected |
| `0.10` | 83 | 8/8 | 37 | 46 | PASS, not selected |

The frozen Gate 5D treatment rate is therefore `0.025`.

See `calibration-decision.json` for the machine-readable decision record and `docs/phase-5/phase-five-completion-report.md` for the full interpretation.
