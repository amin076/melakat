from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def make_command(name: str, **payload: Any) -> dict[str, Any]:
    return {"type": "command", "name": name, "payload": payload}


def make_event(name: str, **payload: Any) -> dict[str, Any]:
    return {
        "type": "event",
        "name": name,
        "payload": payload,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
