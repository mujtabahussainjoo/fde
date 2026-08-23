from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd
import pydeck as pdk
import streamlit as st

from trip_planner.agent import run_trip_planner_agent
from trip_planner.config import get_settings
from trip_planner.services.feedback_store import FeedbackStore
from trip_planner.services.itinerary_store import ItineraryStore
from trip_planner.services.storage import JsonStore
from trip_planner.services.tracing import AgentTracer


settings = get_settings()
logging.basicConfig(level=getattr(logging, settings.app_log_level.upper(), logging.INFO))


ITINERARY_PATH = Path(settings.app_data_dir) / "itineraries.json"
FEEDBACK_PATH = Path(settings.app_data_dir) / "feedback.json"

itinerary_store = ItineraryStore(JsonStore(ITINERARY_PATH))
feedback_store = FeedbackStore(JsonStore(FEEDBACK_PATH))


def ensure_state() -> None:
    defaults = {
        "current_itinerary": None,
        "trace": [],
        "last_saved_id": "",
        "agent_raw": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def build_prompt(destination: str, days: int, interests: list[str], budget: str, extra: str) -> str:
    return (
        "Create a practical itinerary using tool-grounded recommendations. "
        f"Destination: {destination}. Days: {days}. "
        f"Interests: {', '.join(interests) if interests else 'general sightseeing'}. "
        f"Budget style: {budget}. "
        f"User notes: {extra or 'none'}. "
        "Include POIs with coordinates where available."
    )


def run_agent(prompt: str) -> dict[str, Any]:
    tracer = AgentTracer()
    result = run_trip_planner_agent(settings=settings, user_prompt=prompt, tracer=tracer)
    st.session_state["trace"] = result.get("trace", [])
    st.session_state["agent_raw"] = result.get("raw_text", "")
    st.session_state["current_itinerary"] = result.get("itinerary", {})
    return result


def render_map(itinerary: dict[str, Any]) -> None:
    pois = itinerary.get("poi_recommendations", [])
    if not pois:
        st.info("No mappable POIs found yet.")
        return

    frame = pd.DataFrame(pois)
    if frame.empty or "lat" not in frame.columns or "lon" not in frame.columns:
        st.info("POIs are present but missing coordinates.")
        return

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=frame,
        get_position="[lon, lat]",
        get_radius=90,
        get_fill_color=[220, 60, 70, 190],
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=float(frame["lat"].mean()),
        longitude=float(frame["lon"].mean()),
        zoom=12,
        pitch=35,
    )

    tooltip = {
        "html": "<b>{name}</b><br/>{category}<br/>{address}",
        "style": {"color": "white"},
    }

    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip))


def render_itinerary(itinerary: dict[str, Any]) -> None:
    st.subheader(f"Itinerary: {itinerary.get('destination', 'Unknown')}")
    st.write(itinerary.get("summary", ""))

    tips = itinerary.get("travel_tips", [])
    if tips:
        st.markdown("### Travel Tips")
        for tip in tips:
            st.write(f"- {tip}")

    daily_plan = itinerary.get("daily_plan", [])
    if daily_plan:
        st.markdown("### Daily Plan")
        for day in daily_plan:
            title = day.get("title", "Plan")
            day_num = day.get("day", "?")
            with st.expander(f"Day {day_num}: {title}", expanded=False):
                for item in day.get("highlights", []):
                    st.write(f"- {item}")


def save_current_itinerary() -> None:
    itinerary = st.session_state.get("current_itinerary")
    if not itinerary:
        st.warning("No itinerary to save.")
        return
    saved = itinerary_store.save(itinerary)
    st.session_state["last_saved_id"] = saved["id"]
    st.success(f"Saved itinerary: {saved['id']}")


def refinement_prompt(base: dict[str, Any], refinement_text: str) -> str:
    base_json = json.dumps(base, ensure_ascii=True)
    return (
        "Refine this existing itinerary while preserving valid details and grounded recommendations. "
        f"Existing itinerary JSON: {base_json}. "
        f"Refinement request: {refinement_text}."
    )


def main() -> None:
    st.set_page_config(page_title="Trip Planner AI Agent", page_icon="TP", layout="wide")
    ensure_state()

    st.title("Trip Planner AI Agent")
    st.caption("Tool-calling itinerary planner with live data, map visualization, and feedback loop.")

    with st.sidebar:
        st.header("Planner Settings")
        destination = st.text_input("Destination", value="Paris")
        days = st.slider("Trip Length (days)", min_value=1, max_value=14, value=3)
        interests = st.multiselect(
            "Interests",
            options=[
                "museum",
                "attraction",
                "viewpoint",
                "park",
                "restaurant",
                "cafe",
                "shopping",
            ],
            default=["museum", "attraction", "restaurant"],
        )
        budget = st.selectbox("Budget", options=["budget", "mid-range", "luxury"], index=1)
        extra = st.text_area("Notes / Constraints", placeholder="Kids-friendly, no late-night plans, etc.")

        if st.button("Generate Itinerary", use_container_width=True):
            prompt = build_prompt(destination, days, interests, budget, extra)
            result = run_agent(prompt)
            if not result.get("ok"):
                st.warning("Itinerary generated with schema issues. Showing best-effort result.")

        if st.button("Save Current Itinerary", use_container_width=True):
            save_current_itinerary()

    col_a, col_b = st.columns([1.1, 0.9])

    with col_a:
        itinerary = st.session_state.get("current_itinerary")
        if itinerary:
            render_itinerary(itinerary)
        else:
            st.info("Generate an itinerary to get started.")

        st.markdown("### Refine Existing Itinerary")
        refine_text = st.text_input("Refinement request", placeholder="Make this more food-focused and walkable.")
        if st.button("Refine Itinerary"):
            base = st.session_state.get("current_itinerary")
            if not base:
                st.warning("Generate or load an itinerary first.")
            elif not refine_text.strip():
                st.warning("Enter a refinement request.")
            else:
                result = run_agent(refinement_prompt(base, refine_text.strip()))
                if not result.get("ok"):
                    st.warning("Refined itinerary has schema issues. Showing best-effort result.")

        st.markdown("### Load Saved Itineraries")
        saved = itinerary_store.list_all()
        if saved:
            labels = [f"{item['id']} | {item['created_at']}" for item in saved]
            selected = st.selectbox("Saved records", options=list(range(len(labels))), format_func=lambda i: labels[i])
            if st.button("Load Selected Itinerary"):
                st.session_state["current_itinerary"] = saved[selected]["itinerary"]
                st.success("Loaded selected itinerary.")
        else:
            st.caption("No saved itineraries yet.")

    with col_b:
        st.markdown("### Itinerary Map")
        if st.session_state.get("current_itinerary"):
            render_map(st.session_state["current_itinerary"])

        st.markdown("### Feedback")
        last_id = st.session_state.get("last_saved_id", "")
        itinerary_id = st.text_input("Itinerary ID", value=last_id)
        rating = st.slider("Recommendation quality", min_value=1, max_value=5, value=4)
        comments = st.text_area("Feedback comments")
        if st.button("Submit Feedback"):
            if not itinerary_id.strip():
                st.warning("Provide an itinerary ID (save an itinerary first).")
            else:
                feedback_store.save(itinerary_id=itinerary_id.strip(), rating=rating, comments=comments)
                st.success("Feedback saved.")

        st.markdown("### Agent Trace")
        trace = st.session_state.get("trace", [])
        if trace:
            st.json(trace)
        else:
            st.caption("Trace events appear after generation.")

        with st.expander("Raw Agent Output"):
            st.code(st.session_state.get("agent_raw", ""), language="json")


if __name__ == "__main__":
    main()
