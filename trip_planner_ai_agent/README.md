# Trip Planner AI Agent

Production-ready capstone project built with Python + Streamlit.

## Features
- OpenAI Responses API with function calling and multi-step tool orchestration
- Real-time geocoding via Nominatim
- Live POI search via Overpass API
- Optional Wikivoyage retrieval for destination context
- Retry, timeout, and rate-limit aware HTTP client
- Streamlit UI with session state and itinerary refinement loop
- PyDeck interactive map visualization
- JSON-based itinerary persistence and user feedback storage
- Agent execution trace logging for debugging
- Output schema validation for reliability

## Project Structure

```text
trip_planner_ai_agent/
  app.py
  requirements.txt
  .env.example
  data/
  trip_planner/
    agent.py
    config.py
    schemas.py
    services/
      http_client.py
      tracing.py
      storage.py
      itinerary_store.py
      feedback_store.py
    tools/
      nominatim.py
      overpass.py
      wikivoyage.py
```

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
cp .env.example .env
# then edit .env and set OPENAI_API_KEY
```

4. Run the app:

```bash
streamlit run app.py
```

## Demo Flow

1. Enter destination, trip duration, interests, and constraints.
2. Click Generate Itinerary.
3. Review daily plan and POIs on map.
4. Save itinerary.
5. Submit feedback for quality.
6. Refine itinerary with additional instructions.
7. Inspect trace logs for tool-calling path.

## Reliability Notes
- HTTP calls include retries and exponential backoff.
- Basic handling for API 429 and transient failures.
- Itinerary output validated with Pydantic schema.
- If schema validation fails, app still shows best-effort output and trace.
