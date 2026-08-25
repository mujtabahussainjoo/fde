from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class TraceEvent:
    event_type: str
    message: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )


class AgentTracer:
    def __init__(self, logger: logging.Logger | None = None) -> None:
        self.events: list[TraceEvent] = []
        self.logger = logger or logging.getLogger("trip_planner.agent")

    def add(self, event_type: str, message: str, payload: dict[str, Any] | None = None) -> None:
        event = TraceEvent(event_type=event_type, message=message, payload=payload or {})
        self.events.append(event)
        self.logger.info("[%s] %s | %s", event.event_type, event.message, event.payload)

    def to_dict(self) -> list[dict[str, Any]]:
        return [
            {
                "timestamp": e.timestamp,
                "event_type": e.event_type,
                "message": e.message,
                "payload": e.payload,
            }
            for e in self.events
        ]
