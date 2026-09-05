from __future__ import annotations

import queue
import time
from multiprocessing.queues import Queue
from threading import Event
from typing import Any

from .engine import DemoEngine
from .protocol import make_event


def engine_process_main(
    config: dict[str, Any],
    command_queue: Queue,
    event_queue: Queue,
    stop_event: Event,
) -> None:
    def emit(event: dict[str, Any]) -> None:
        event_queue.put(event)

    engine = DemoEngine(config, emit)
    running = False
    emit(make_event("ready", snapshot=engine.snapshot(), metrics=engine.metrics()))

    while not stop_event.is_set():
        try:
            command = command_queue.get_nowait()
            name = command.get("name")
            if name == "start" or name == "resume":
                running = True
                emit(make_event("status", status="running"))
            elif name == "pause":
                running = False
                emit(make_event("status", status="paused"))
            elif name == "step":
                engine.step()
                emit(make_event("status", status="paused"))
            elif name == "reset":
                engine = DemoEngine(config, emit)
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
            time.sleep(0.03)
        else:
            time.sleep(0.05)

    emit(make_event("stopped", snapshot=engine.snapshot(), metrics=engine.metrics()))
