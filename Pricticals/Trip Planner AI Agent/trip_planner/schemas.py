from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, ValidationError


class DailyPlanItem(BaseModel):
    day: int = Field(ge=1)
    title: str
    highlights: list[str] = Field(default_factory=list)


class ItineraryResponse(BaseModel):
    destination: str
    summary: str
    travel_tips: list[str] = Field(default_factory=list)
    daily_plan: list[DailyPlanItem] = Field(default_factory=list)
    poi_recommendations: list[dict[str, Any]] = Field(default_factory=list)


def validate_itinerary(payload: dict[str, Any]) -> tuple[bool, dict[str, Any], str]:
    try:
        parsed = ItineraryResponse(**payload)
        return True, parsed.model_dump(), ""
    except ValidationError as exc:
        return False, payload, str(exc)
