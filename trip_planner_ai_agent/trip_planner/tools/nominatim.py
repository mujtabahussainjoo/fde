from __future__ import annotations

from typing import Any

from trip_planner.config import Settings
from trip_planner.services.http_client import ResilientHttpClient


def geocode_destination(
    client: ResilientHttpClient, settings: Settings, destination: str
) -> dict[str, Any]:
    url = f"{settings.nominatim_base_url}/search"
    data = client.request(
        "GET",
        url,
        params={
            "q": destination,
            "format": "jsonv2",
            "limit": 1,
            "addressdetails": 1,
        },
    )

    if not isinstance(data, list) or not data:
        return {"found": False, "destination": destination}

    best = data[0]
    return {
        "found": True,
        "destination": destination,
        "display_name": best.get("display_name", destination),
        "lat": float(best["lat"]),
        "lon": float(best["lon"]),
        "raw": best,
    }
