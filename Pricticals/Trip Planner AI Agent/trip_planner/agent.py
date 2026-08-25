from __future__ import annotations

import json
from typing import Any

from openai import OpenAI

from trip_planner.config import Settings
from trip_planner.schemas import validate_itinerary
from trip_planner.services.http_client import ResilientHttpClient
from trip_planner.services.tracing import AgentTracer
from trip_planner.tools.nominatim import geocode_destination
from trip_planner.tools.overpass import search_pois
from trip_planner.tools.wikivoyage import get_travel_guide


def _tool_schemas() -> list[dict[str, Any]]:
    return [
        {
            "type": "function",
            "name": "geocode_destination",
            "description": "Geocode a destination name into coordinates using OpenStreetMap Nominatim.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {"type": "string"},
                },
                "required": ["destination"],
                "additionalProperties": False,
            },
        },
        {
            "type": "function",
            "name": "search_pois",
            "description": "Search nearby points of interest from Overpass API.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {"type": "number"},
                    "lon": {"type": "number"},
                    "radius_m": {"type": "integer", "default": 2500},
                    "categories": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": ["lat", "lon"],
                "additionalProperties": False,
            },
        },
        {
            "type": "function",
            "name": "get_travel_guide",
            "description": "Fetch a destination summary from Wikivoyage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {"type": "string"},
                },
                "required": ["destination"],
                "additionalProperties": False,
            },
        },
    ]


def _system_prompt() -> str:
    return (
        "You are a production-grade Trip Planner AI. "
        "Use tools before making recommendations. "
        "Always ground recommendations in retrieved tool data. "
        "Return final output ONLY as minified JSON with fields: "
        "destination, summary, travel_tips (array), daily_plan (array of {day,title,highlights}), "
        "poi_recommendations (array of objects with name,lat,lon,category,address when available)."
    )


def _dispatch_tool(
    tool_name: str,
    args: dict[str, Any],
    http_client: ResilientHttpClient,
    settings: Settings,
) -> dict[str, Any]:
    if tool_name == "geocode_destination":
        return geocode_destination(http_client, settings, args["destination"])
    if tool_name == "search_pois":
        return search_pois(
            http_client,
            settings,
            lat=float(args["lat"]),
            lon=float(args["lon"]),
            radius_m=int(args.get("radius_m", 2500)),
            categories=list(args.get("categories", [])) or None,
        )
    if tool_name == "get_travel_guide":
        return get_travel_guide(http_client, settings, args["destination"])
    return {"error": f"Unknown tool: {tool_name}"}


def _extract_text_from_response(response: Any) -> str:
    output_text = getattr(response, "output_text", "")
    if output_text:
        return output_text

    chunks: list[str] = []
    for item in getattr(response, "output", []) or []:
        if getattr(item, "type", "") == "message":
            for part in getattr(item, "content", []) or []:
                text_value = getattr(part, "text", None)
                if text_value:
                    chunks.append(text_value)
    return "\n".join(chunks)


def run_trip_planner_agent(
    *,
    settings: Settings,
    user_prompt: str,
    tracer: AgentTracer,
    max_steps: int = 6,
) -> dict[str, Any]:
    if not settings.openai_api_key:
        tracer.add("config", "OPENAI_API_KEY missing, returning fallback response")
        return {
            "ok": True,
            "itinerary": {
                "destination": "Unknown",
                "summary": "Set OPENAI_API_KEY to enable the tool-calling planner.",
                "travel_tips": [
                    "Add your OPENAI_API_KEY in .env",
                    "Retry from the Streamlit interface",
                ],
                "daily_plan": [],
                "poi_recommendations": [],
            },
            "trace": tracer.to_dict(),
            "raw_text": "",
        }

    client = OpenAI(api_key=settings.openai_api_key)
    http_client = ResilientHttpClient(settings)
    tools = _tool_schemas()

    tracer.add("agent", "Creating initial response", {"model": settings.openai_model})
    response = client.responses.create(
        model=settings.openai_model,
        tools=tools,
        input=[
            {"role": "system", "content": _system_prompt()},
            {"role": "user", "content": user_prompt},
        ],
    )

    for step in range(1, max_steps + 1):
        function_calls = [
            item for item in (getattr(response, "output", []) or []) if getattr(item, "type", "") == "function_call"
        ]

        if not function_calls:
            tracer.add("agent", "No more function calls", {"step": step})
            break

        tracer.add("agent", "Executing function calls", {"step": step, "count": len(function_calls)})
        tool_outputs: list[dict[str, Any]] = []

        for call in function_calls:
            tool_name = getattr(call, "name", "")
            call_id = getattr(call, "call_id", "")
            raw_args = getattr(call, "arguments", "{}")
            try:
                args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
            except json.JSONDecodeError:
                args = {}

            tracer.add("tool", f"Calling {tool_name}", {"args": args})
            try:
                tool_result = _dispatch_tool(tool_name, args, http_client, settings)
            except Exception as exc:  # noqa: BLE001
                tool_result = {"error": str(exc), "tool": tool_name}

            tracer.add("tool", f"Completed {tool_name}", {"has_error": "error" in tool_result})
            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": call_id,
                    "output": json.dumps(tool_result),
                }
            )

        response = client.responses.create(
            model=settings.openai_model,
            previous_response_id=response.id,
            tools=tools,
            input=tool_outputs,
        )

    raw_text = _extract_text_from_response(response).strip()
    tracer.add("agent", "Final response received", {"raw_text_length": len(raw_text)})

    itinerary_payload: dict[str, Any]
    try:
        itinerary_payload = json.loads(raw_text)
        if not isinstance(itinerary_payload, dict):
            itinerary_payload = {"destination": "Unknown", "summary": raw_text}
    except json.JSONDecodeError:
        itinerary_payload = {
            "destination": "Unknown",
            "summary": raw_text or "No itinerary generated.",
            "travel_tips": [],
            "daily_plan": [],
            "poi_recommendations": [],
        }

    ok, validated, validation_error = validate_itinerary(itinerary_payload)
    if not ok:
        tracer.add("validation", "Itinerary schema validation failed", {"error": validation_error})

    return {
        "ok": ok,
        "itinerary": validated,
        "trace": tracer.to_dict(),
        "raw_text": raw_text,
        "validation_error": validation_error,
    }
