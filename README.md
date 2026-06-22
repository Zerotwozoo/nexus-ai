# Nexus AI

**An AI-powered productivity ecosystem** — Chat, notes, tasks, finance, trading, automation, collaboration, and cloud storage, all in one modular workspace.

## Architecture

![Architecture](ARCHITECTURE.md)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15, React 19, TypeScript, TailwindCSS, Framer Motion |
| Backend | FastAPI, Python 3.12, SQLAlchemy 2.0, Pydantic v2 |
| Database | PostgreSQL (pgvector), Redis |
| AI Engine | LangGraph, LiteLLM, OpenAI, Anthropic |
| Infrastructure | Docker, Kubernetes, Terraform |
| CI/CD | GitHub Actions |

## Getting Started

### Prerequisites

- Node.js 20+
- pnpm 9+
- Python 3.12+
- Poetry
- Docker & Docker Compose

### Install

```bash
# Clone the repository
git clone https://github.com/your-org/nexus-ai.git
cd nexus-ai

# Install frontend dependencies
pnpm install

# Install backend dependencies
cd backend
poetry install
cd ..

# Copy environment file
cp .env.example .env
```

### Run (Development)

```bash
# Start infrastructure services
docker compose -f infrastructure/docker/docker-compose.yml up -d

# Start backend
cd backend && poetry run uvicorn src.main:app --reload --port 8000

# Start frontend (in another terminal)
pnpm dev
```

### Run Database Migrations

```bash
cd backend
poetry run alembic upgrade head
```

## Project Structure

```
nexus-ai/
├── packages/          # Shared packages (kernel, ui-system, api-client)
├── apps/web/          # Next.js frontend
├── backend/           # FastAPI backend
├── ai-engine/         # AI sidecar service
└── infrastructure/    # Docker, K8s, Terraform, Monitoring
```

## Modules

- **AI Assistant** — Chat, agents, RAG, memory, multi-agent orchestration
- **Dashboard** — Widgets, analytics, productivity score
- **Notes** — Rich text, markdown, AI summarize/rewrite/translate
- **Tasks** — Kanban, calendar, priority, pomodoro
- **Calendar** — Events, Google sync, AI scheduling
- **Documents** — PDF viewer, OCR, annotations, AI extraction
- **Finance** — Budget, expenses, subscriptions, analytics
- **Trading** — Journal, risk calculator, performance analytics
- **Automation** — Workflow builder, triggers, webhooks
- **Cloud Storage** — Upload, preview, versioning, encryption
- **Password Manager** — AES vault, secure sharing
- **Collaboration** — Workspaces, roles, comments, mentions

## License

MIT
