from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from trip_planner.services.storage import JsonStore


class ItineraryStore:
    def __init__(self, store: JsonStore) -> None:
        self.store = store

    def save(self, itinerary: dict[str, Any]) -> dict[str, Any]:
        record = {
            "id": f"itin-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "itinerary": itinerary,
        }
        self.store.append(record)
        return record

    def list_all(self) -> list[dict[str, Any]]:
        return self.store.read_all()
