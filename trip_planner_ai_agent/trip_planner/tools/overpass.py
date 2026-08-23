from __future__ import annotations

from typing import Any

from trip_planner.config import Settings
from trip_planner.services.http_client import ResilientHttpClient


DEFAULT_CATEGORIES = ["museum", "attraction", "viewpoint", "park", "restaurant", "cafe"]


def _build_overpass_query(lat: float, lon: float, radius_m: int, categories: list[str]) -> str:
    clauses = []
    for category in categories:
        safe = category.replace('"', "")
        clauses.append(f'node["tourism"="{safe}"](around:{radius_m},{lat},{lon});')
        clauses.append(f'node["amenity"="{safe}"](around:{radius_m},{lat},{lon});')
        clauses.append(f'way["tourism"="{safe}"](around:{radius_m},{lat},{lon});')
        clauses.append(f'way["amenity"="{safe}"](around:{radius_m},{lat},{lon});')
    joined = "\n".join(clauses)
    return f"""
[out:json][timeout:45];
(
{joined}
);
out center 80;
""".strip()


def search_pois(
    client: ResilientHttpClient,
    settings: Settings,
    lat: float,
    lon: float,
    radius_m: int = 2500,
    categories: list[str] | None = None,
) -> dict[str, Any]:
    categories = categories or DEFAULT_CATEGORIES
    query = _build_overpass_query(lat, lon, radius_m, categories)

    raw = client.request(
        "POST",
        settings.overpass_base_url,
        data={"data": query},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if not isinstance(raw, dict):
        return {"count": 0, "pois": []}

    elements = raw.get("elements", [])
    pois: list[dict[str, Any]] = []

    for item in elements:
        tags = item.get("tags", {})
        name = tags.get("name")
        if not name:
            continue

        poi_lat = item.get("lat")
        poi_lon = item.get("lon")
        center = item.get("center", {})
        if poi_lat is None:
            poi_lat = center.get("lat")
        if poi_lon is None:
            poi_lon = center.get("lon")

        if poi_lat is None or poi_lon is None:
            continue

        pois.append(
            {
                "name": name,
                "lat": float(poi_lat),
                "lon": float(poi_lon),
                "category": tags.get("tourism") or tags.get("amenity") or "unknown",
                "address": tags.get("addr:full")
                or ", ".join(
                    part for part in [tags.get("addr:street"), tags.get("addr:city")] if part
                ),
            }
        )

    # Deduplicate by name + approximate coordinate
    unique: dict[str, dict[str, Any]] = {}
    for poi in pois:
        key = f"{poi['name'].strip().lower()}::{round(poi['lat'], 4)}::{round(poi['lon'], 4)}"
        unique[key] = poi

    final_pois = list(unique.values())
    return {"count": len(final_pois), "pois": final_pois[:60]}
