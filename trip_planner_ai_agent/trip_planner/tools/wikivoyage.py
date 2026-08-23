from __future__ import annotations

from typing import Any

from trip_planner.config import Settings
from trip_planner.services.http_client import ResilientHttpClient


def get_travel_guide(
    client: ResilientHttpClient, settings: Settings, destination: str
) -> dict[str, Any]:
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "titles": destination,
        "redirects": 1,
    }
    raw = client.request("GET", settings.wikivoyage_api_url, params=params)

    if not isinstance(raw, dict):
        return {"found": False, "destination": destination, "summary": ""}

    pages = raw.get("query", {}).get("pages", {})
    for page in pages.values():
        extract = page.get("extract", "").strip()
        title = page.get("title", destination)
        if extract:
            return {
                "found": True,
                "destination": destination,
                "title": title,
                "summary": extract[:4000],
            }

    return {"found": False, "destination": destination, "summary": ""}
