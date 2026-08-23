# Trip Planner AI Agent Capstone Project Task

## Goal
Build a production-ready Trip Planner AI application that demonstrates agentic workflows, real-time data integration, and a polished user experience.

## Core Components

### 1) Agent Architecture with Tool Calling
- [ ] Implement OpenAI Responses API with function calling.
- [ ] Define tools for:
  - [ ] POI (Points of Interest) search.
  - [ ] Travel guide retrieval.
- [ ] Add multi-step reasoning and tool orchestration.
- [ ] Add debugging/tracing for agent execution paths.

### 2) Real-Time Data Integration
- [ ] Integrate OpenStreetMap Nominatim API for geocoding.
- [ ] Integrate Overpass API for live POI queries.
- [ ] Add optional Wikivoyage RAG support.
- [ ] Implement robust rate limiting, retries, and error handling.

### 3) User Experience and Feedback Loops
- [ ] Build a Streamlit UI with session state management.
- [ ] Add interactive map visualization using PyDeck.
- [ ] Implement feedback collection for recommendation quality.
- [ ] Add itinerary persistence and refinement workflows.

## Project Objectives Checklist
- [ ] Build a production-ready application using Streamlit.
- [ ] Implement agentic workflows via OpenAI function calling.
- [ ] Integrate multiple external APIs (OpenStreetMap, Wikivoyage).
- [ ] Create interactive visualizations with PyDeck.
- [ ] Design feedback loops to improve recommendations.
- [ ] Handle state management and persistence.
- [ ] Validate and constrain AI outputs for reliability.

## Suggested Milestones
- [ ] Milestone 1: Project scaffold and environment setup.
- [ ] Milestone 2: Tool-calling agent implemented and tested.
- [ ] Milestone 3: External APIs integrated with fault tolerance.
- [ ] Milestone 4: Streamlit + PyDeck interface complete.
- [ ] Milestone 5: Feedback, persistence, and refinement loop complete.
- [ ] Milestone 6: End-to-end validation and demo readiness.

## Prerequisites
- Python fundamentals.
- REST API integration (auth, errors, retries).
- Data science stack familiarity (NumPy, Pandas, scikit-learn).
- AI/ML basics (prompting, RAG).
- OpenAI API usage (Responses API, function calling).
- Streamlit skills (state, callbacks, components).

## Deliverables
- [ ] Working Streamlit app.
- [ ] Tool-calling AI agent with logs/traces.
- [ ] API integration modules (Nominatim, Overpass, optional Wikivoyage).
- [ ] Interactive itinerary map.
- [ ] Feedback and persistence mechanism.
- [ ] README with setup, architecture, and demo steps.

## Definition of Done
- [ ] User can generate and refine itineraries for a destination.
- [ ] Recommendations are grounded in retrieved external data.
- [ ] App handles API failures gracefully.
- [ ] Session state and saved itineraries persist correctly.
- [ ] Demo flow is stable and portfolio-ready.
