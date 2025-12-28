<div align="center">

# Trip Planner Agent

AI‑powered multi‑agent trip planning with FastAPI + LangGraph backend, React frontend, structured logging, and optional Langfuse observability.

![status](https://img.shields.io/badge/status-active-success) ![python](https://img.shields.io/badge/python-3.11+-blue) ![license](https://img.shields.io/badge/license-MIT-lightgrey)

</div>

---

## ⚡ Overview

The system orchestrates specialized agents (research, budget, itinerary, accommodation, coordinator) using LangGraph to produce a consolidated travel plan. A single POST request yields a structured result containing summary, itinerary placeholders, recommendations, and metadata. The frontend collects user inputs and renders results with quick‑action utilities.

---

## 🔑 Key Features

| Category                  | Highlights                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------- |
| Multi‑Agent Orchestration | LangGraph workflow with sequential agent pipeline                                     |
| AI Integration            | LangChain OpenAI model (lazy init + mockable for tests)                               |
| Observability (optional)  | Langfuse callback handler + diagnostic endpoints                                      |
| API Surface               | FastAPI with `/plan-trip`, `/health`, `/version`, `/config`, reference data endpoints |
| Frontend                  | React + Tailwind (form + results panel + export/share helpers)                        |
| Quality Gates             | Ruff, Black, Flake8, pre‑commit hooks, smoke + health tests                           |
| Logging                   | Structured (JSON optional) with level & env control                                   |

---

## 🗂 Project Structure (Essential Files Only)

```
trip-planner-agent/
├── backend/
│   ├── main.py                # FastAPI app + endpoints
│   ├── trip_planner_agent.py  # LangGraph workflow & agents
│   ├── logging_config.py      # Structured logging setup
│   ├── settings.py            # Centralized config
│   ├── version.py             # Service version constant
│   └── tests/
│       ├── test_health.py
│       └── test_plan_trip_smoke.py
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── components/TripResults.js
│   └── .env.development
├── requirements.txt
├── dev-requirements.txt
├── ruff.toml
├── .pre-commit-config.yaml
├── env.example
└── README.md
```

---

## � Prerequisites

| Tool           | Version                     |
| -------------- | --------------------------- |
| Python         | 3.11+                       |
| Node.js        | 18+                         |
| OpenAI API Key | Required for real LLM calls |
| Langfuse Keys  | Optional (observability)    |

---

## ⚙️ Environment Configuration

Root `.env` (copy from `env.example`):

```env
OPENAI_API_KEY=sk-...
LANGFUSE_SECRET_KEY=...
LANGFUSE_PUBLIC_KEY=...
LANGFUSE_HOST=https://cloud.langfuse.com
APP_ENV=local
LOG_LEVEL=INFO
LOG_JSON=false
```

Frontend `frontend/.env.development`:

```env
REACT_APP_API_BASE=http://localhost:8000
```

---

## 🚀 Setup & Run

Backend:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r dev-requirements.txt
uvicorn backend.main:app --reload
```

Frontend (new terminal):

```bash
cd frontend
npm install
npm start
```

Visit: `http://localhost:3000` (UI) and `http://localhost:8000/docs` (API docs)

---

## � Endpoints (Summary)

| Method | Path            | Purpose                        |
| ------ | --------------- | ------------------------------ |
| GET    | `/`             | Root sanity message            |
| GET    | `/health`       | Status + version + environment |
| GET    | `/version`      | Service version                |
| GET    | `/config`       | Non‑sensitive config snapshot  |
| POST   | `/plan-trip`    | Generate trip plan (core)      |
| GET    | `/destinations` | Static sample destinations     |
| GET    | `/interests`    | Static list of interests       |

Interactive docs: Swagger (`/docs`), ReDoc (`/redoc`).

---

## 🧠 Request / Response Contract (`POST /plan-trip`)

Request (JSON):

```json
{
  "destination": "Paris",
  "duration": 5,
  "budget": 2500,
  "interests": ["art", "food"],
  "start_date": "2025-06-01",
  "end_date": "2025-06-06",
  "accommodation_type": "hotel",
  "transportation_type": "flight"
}
```

Successful Response (abridged):

```json
{
  "success": true,
  "data": {
    "final_plan": { "summary": "..." },
    "destination": "Paris",
    "duration": 5,
    "budget": 2500,
    "messages": ["Research completed...", "Budget analysis completed..."],
    "workflow_id": "uuid"
  },
  "error": null
}
```

---

## 🧪 Testing & Quality

Run all backend tests:

```bash
pytest -q backend
```

Pre‑commit (after `pre-commit install`): triggers ruff, black, flake8, smoke tests.

CI (GitHub Actions) enforces: ruff → black --check → flake8 → pytest.

---

## 📦 Tooling Summary

| Tool       | Purpose                        |
| ---------- | ------------------------------ |
| Ruff       | Fast lint + import ordering    |
| Black      | Deterministic formatting       |
| Flake8     | Supplemental lint rules        |
| Pytest     | Test execution                 |
| Pre‑commit | Local quality gate             |
| Langfuse   | (Optional) tracing + analytics |

Structured logging: set `LOG_JSON=true` for JSON output.

---

## � Observability (Optional)

If Langfuse keys are present, callbacks attach automatically and traces become visible in the dashboard (workflow + model calls). Without keys, the system still runs (graceful degradation).

Diagnostic endpoints: `/health`, `/config` help verify environment & version quickly.

---

## 🧱 Architecture Notes

Sequence: User request → FastAPI route → build `TripRequest` → LangGraph pipeline (agents sequential) → Accumulate messages → Final coordinator summary → Response model.

LLM access is centralized via `get_llm()` (lazy; easily monkeypatched for tests).

Logging configured early; secrets never logged; config snapshot redacts values (booleans only for presence).

---

## 🧩 Extending

Add a new agent:

1. Create tool or pure function.
2. Add node to graph in `trip_planner_agent.py`.
3. Insert edge sequence before `coordinator_agent`.
4. Adjust final state extraction if producing new artifacts.

Add an endpoint:

1. Define Pydantic model (request / response) if needed.
2. Implement route in `main.py`.
3. Add tests.
4. Document in table above.

---

## 🚀 Deployment Quick Notes

Recommended: containerize with multi‑stage build (Python slim + Node build). Ensure you pass env vars at runtime and set `--workers` for Uvicorn (e.g., `--workers 2` for light loads). Configure CORS origins explicitly in production.

---

## 🤝 Contributing

1. Fork & branch (feat/<slug>)
2. Install dev deps + pre-commit
3. Add / update tests
4. Ensure `pytest` + linters pass locally
5. Open PR with summary + screenshots (if UI change)

---

## 📄 License

MIT – see LICENSE if present or add one before distribution.

---

## 🗺 Future Ideas

- Real external data sources (flights / hotels)
- Caching + rate limiting
- User auth + saved itineraries
- Cost / token usage dashboard
- Coverage reporting & Codecov integration

---

## ❓ Support

1. `/health` / `/config` for quick diagnostics
2. Check API docs at `/docs`
3. Run smoke test: `pytest backend/tests/test_plan_trip_smoke.py -q`
4. Verify env vars loaded (`printenv | grep OPENAI`)

---

Happy planning! 🌍✈️
