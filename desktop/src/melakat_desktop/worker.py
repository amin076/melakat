from __future__ import annotations

import queue
import time
from multiprocessing.queues import Queue
from threading import Event
from typing import Any

from .engine import DemoEngine
from .phase_zero_engine import PhaseZeroEngine
from .protocol import make_event


ENGINE_BACKENDS = {
    "demo": DemoEngine,
    "phase-zero-vm": PhaseZeroEngine,
}


def create_engine(config: dict[str, Any], emit: Any) -> Any:
    backend = str(config.get("run.engine_backend", "phase-zero-vm"))
    try:
        engine_type = ENGINE_BACKENDS[backend]
    except KeyError as exc:
        raise ValueError(f"unknown_engine_backend:{backend}") from exc
    return engine_type(config, emit)


def engine_process_main(
    config: dict[str, Any],
    command_queue: Queue,
    event_queue: Queue,
    stop_event: Event,
) -> None:
    def emit(event: dict[str, Any]) -> None:
        event_queue.put(event)

    engine = create_engine(config, emit)
    running = False
    emit(make_event("ready", snapshot=engine.snapshot(), metrics=engine.metrics()))

    while not stop_event.is_set():
        try:
            command = command_queue.get_nowait()
            name = command.get("name")
            if name in {"start", "resume"}:
                running = not engine.finished
                emit(make_event("status", status="running" if running else "finished"))
            elif name == "pause":
                running = False
                emit(make_event("status", status="paused"))
            elif name == "step":
                engine.step()
                emit(make_event("status", status="finished" if engine.finished else "paused"))
            elif name == "reset":
                engine = create_engine(config, emit)
                running = False
                emit(make_event("reset", snapshot=engine.snapshot(), metrics=engine.metrics()))
            elif name == "stop":
                running = False
                emit(make_event("status", status="stopped"))
                break
        except queue.Empty:
            pass

        if running:
            engine.step()
            if engine.finished:
                running = False
                emit(make_event("status", status="finished"))
            time.sleep(0.03)
        else:
            time.sleep(0.05)

    emit(make_event("stopped", snapshot=engine.snapshot(), metrics=engine.metrics()))
