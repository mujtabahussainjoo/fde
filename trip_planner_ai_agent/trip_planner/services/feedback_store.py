from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from trip_planner.services.storage import JsonStore


class FeedbackStore:
    def __init__(self, store: JsonStore) -> None:
        self.store = store

    def save(self, itinerary_id: str, rating: int, comments: str) -> dict[str, Any]:
        record = {
            "itinerary_id": itinerary_id,
            "rating": rating,
            "comments": comments,
            "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        self.store.append(record)
        return record

    def list_all(self) -> list[dict[str, Any]]:
        return self.store.read_all()
