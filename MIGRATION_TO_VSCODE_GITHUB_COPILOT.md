# Migration Guide: Cursor ➜ VS Code + GitHub Copilot

This document provides an end‑to‑end, opinionated process to fully migrate your Trip Planner AI project from Cursor to a first‑class VS Code + GitHub Copilot (Chat + Inline + Agent Mode) environment.

---

## 1. Goals of the Migration

- Single consistent dev environment (VS Code workspace)
- Deterministic tasks (debug, run, test, format, lint) via `tasks.json` & launch configs
- Rich AI assistance (Copilot Chat + project rules in `.vscode/copilot.json`)
- Reproducible onboarding (one document, one command path)
- Guardrails: style, architecture, observability, security

---

## 2. Feature Parity Mapping

| Cursor Concept           | VS Code / Copilot Equivalent                               | Status |
| ------------------------ | ---------------------------------------------------------- | ------ |
| Inline AI edits          | Copilot inline completions                                 | ✅     |
| Chat side panel          | GitHub Copilot Chat view                                   | ✅     |
| Project context memory   | `.vscode/copilot.json` rules + Chat `#file` / `@workspace` | ✅     |
| Multi-command agent      | Copilot Chat task style prompts ("Run tests", etc.)        | ✅     |
| Task runner scripts      | `tasks.json` (install/run/test/format)                     | ✅     |
| Multi-service startup    | Launch compound: "Start Full Stack" + new task variant     | ✅     |
| Code templates           | `.vscode/snippets/*.json`                                  | ✅     |
| Environment config hints | `VSCODE_SETUP.md` + this migration guide                   | ✅     |

---

## 3. Prerequisites

- VS Code (latest stable)
- Node.js LTS & npm
- Python 3.10+ (align with FastAPI & Pydantic 2)
- OpenAI + Langfuse credentials ready for `.env`

---

## 4. One-Time Setup

```bash
# Clone (if not already)
git clone <your-repo-url> trip-planner-agent
cd trip-planner-agent

# Python env
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend deps
cd frontend && npm install && cd ..

# Env file
cp env.example .env
# Edit .env and add OPENAI_API_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY
```

Open VS Code:

```bash
code .
```

When prompted, install recommended extensions.

---

## 5. VS Code Assets Added / Updated

| File                                    | Purpose                                                         |
| --------------------------------------- | --------------------------------------------------------------- |
| `.vscode/tasks.json`                    | Deterministic task runner (added full‑stack task)               |
| `.vscode/launch.json`                   | Backend, frontend & compound debugging                          |
| `.vscode/extensions.json`               | Curated extension recommendations & unwanted duplicates removed |
| `.vscode/settings.json`                 | Python formatting, linting, test discovery, exclusions          |
| `.vscode/copilot.json`                  | Project‑specific architectural & style guidance for AI          |
| `.vscode/snippets/`                     | Language scaffolding for common patterns                        |
| `MIGRATION_TO_VSCODE_GITHUB_COPILOT.md` | This guide                                                      |

---

## 6. Running & Debugging

### Tasks (Command Palette → "Tasks: Run Task")

- Install Python Dependencies
- Install Frontend Dependencies
- Start Backend
- Start Frontend
- Start Full Stack (Tasks)
- Run Tests
- Format Python Code
- Lint Python Code

### Launch (Run & Debug panel)

- Start Backend Server (debug FastAPI + LangGraph)
- Debug Trip Planning (focus on workflow file)
- Start Frontend ( Node attach )
- Start Full Stack (compound)

Pick the approach you prefer (Tasks vs Launch). Use compound when you need both.

---

## 7. Copilot Effective Usage

### Useful Prompts

```
Explain the LangGraph workflow in backend/trip_planner_agent.py
Suggest tests for the trip planning orchestration
Refactor API error handling for consistency
Add a new agent node that enriches itinerary with cuisine suggestions
```

### Context Tips

- Use Chat @workspace for repo‑aware reasoning
- Use inline selection + Ctrl+I (or right‑click) for focused refactors
- Reference files explicitly: "Review `backend/trip_planner_agent.py` for logging improvements"

---

## 8. Architectural Guardrails (Reinforced via copilot.json)

1. FastAPI routes: Always type & validate with Pydantic models
2. LangGraph nodes: Pure (no hidden global side effects) & observable (Langfuse trace metadata)
3. Logging: Structured, contextual, never leaking secrets
4. React: Functional components + hooks, minimal local state, custom hooks for data
5. Error surfaces: Consistent JSON shape `{ "success": false, "error": { code, message } }`
6. Secrets: Only loaded from central settings (never hard-coded)

---

## 9. Testing Strategy (Recommended Enhancements)

| Layer       | What to Add                                                |
| ----------- | ---------------------------------------------------------- |
| Unit        | Pure LangGraph node logic (state transforms)               |
| API         | FastAPI route success + error cases (pytest + httpx)       |
| Integration | End‑to‑end plan generation (mock external APIs)            |
| Frontend    | Component render + fetch hook (Jest/React Testing Library) |

Add `tests/` soon to formalize this (see Next Steps).

---

## 10. Observability (Langfuse)

- Ensure env vars present
- Add trace attributes per node: name, duration, inputs size
- Use Copilot prompt: "Instrument trip_planner_agent workflow with Langfuse spans"

---

## 11. Migration Validation Checklist

| Item               | Verify                                              |
| ------------------ | --------------------------------------------------- |
| Copilot Chat works | Ask: "List backend routes"                          |
| Rules loaded       | Chat: "Summarize the copilot.json rules"            |
| Backend runs       | Task or launch: Start Backend                       |
| Frontend runs      | Task or launch: Start Frontend                      |
| Full stack         | Compound or Start Full Stack (Tasks)                |
| Tests run          | Run Tests task (even if currently minimal)          |
| Formatting         | Save a Python file → Black applied                  |
| Linting            | Run flake8 task                                     |
| Observability      | Trigger itinerary request, check Langfuse dashboard |

---

## 12. Security & Hygiene

- Add `.env` to `.gitignore` (confirm) – DO NOT commit secrets
- Rotate keys if previously exposed in Cursor logs
- Keep dependencies updated monthly (pip + npm audit)

---

## 13. Common Pitfalls After Migration

| Issue                               | Fix                                                  |
| ----------------------------------- | ---------------------------------------------------- |
| Copilot not suggesting contextually | Open relevant files & re-ask in Chat with @workspace |
| Wrong Python interpreter            | Check bottom status bar → select `./venv/bin/python` |
| Duplicate Copilot extensions        | Remove legacy `ms-vscode.vscode-github-copilot*` IDs |
| Port collision (3000 / 8000)        | Change in launch/task or export `PORT`               |
| Missing env vars in debug           | Add to `launch.json` env section                     |

---

## 14. Next Steps (Optional Enhancements)

- Add `tests/` scaffolding with pytest + httpx
- Introduce `pre-commit` hooks (black, flake8, isort)
- Add `ruff` for faster linting (can replace flake8/isort)
- Add CI workflow (GitHub Actions) for tests + lint
- Add Jest + React Testing Library for frontend
- Introduce `typed-settings` module for central env var management
- Add Docker dev container for parity / onboarding

---

## 15. Quick Reference Commands

```bash
# Start virtual env
source venv/bin/activate

# Run backend (manual)
python backend/main.py

# Run frontend (manual)
(cd frontend && npm start)

# Run tests
pytest backend -v
```

---

## 16. Support Prompts for Copilot Chat

```
Audit error handling consistency across backend
Suggest improved logging fields for itinerary generation
Propose a test harness for the trip planner pipeline
Generate a React hook for querying /plan API endpoint
```

---

## 17. Confirmation

When all checklist items are green and Copilot responds accurately about architecture details, the migration is considered COMPLETE.

---

**Enjoy your upgraded AI-assisted development workflow in VS Code!**
