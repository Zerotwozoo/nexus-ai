# Nexus AI — Architecture Document

## Executive Summary

Nexus AI is a modular, AI-first productivity ecosystem architected for horizontal scalability. Each domain module is designed as an independent bounded context, communicating through well-defined contracts, enabling future extraction into microservices.

---

## 1. Architectural Decisions & Trade-offs

### Monorepo (Turborepo + pnpm workspaces)
- **Why:** Shared TypeScript types, UI components, ESLint/Prettier configs, and API client generation across frontend and backend reduce duplication
- **Trade-off:** Larger clone size, but negligible vs. cross-repo coordination overhead
- **Tool:** Turborepo provides granular caching + parallel task execution

### Clean Architecture (Hexagonal) Layers
```
Domain (entities + use-cases) ← Application (ports) ← Infrastructure (adapters)
```
- **Why:** Business logic is framework-agnostic. Testing domains requires zero infrastructure
- **Pattern:** Use-case interactors orchestrate domain objects via repository interfaces

### Vertical Slice Modules
- Each feature (Notes, Tasks, Finance, etc.) is a package with its own domain, API, and UI
- Slices share only through Kernel (shared kernel: base types, common utilities)
- Enables independent deployment + parallel team ownership

### API Versioning (URL prefix: /api/v1/)
- Long-term stability. Old versions deprecated via middleware, never broken

### CQRS + Event Sourcing (limited)
- Commands write to primary DB → emit domain events → async projections update read-models
- Used where audit/log/replay matters: Finance, Trading, Automation

### Backend: FastAPI + Python 3.12
- Async-native, Pydantic v2 for validation/serialization
- **Why not Go/Rust:** AI/ML ecosystem lock-in, LangChain, RAG pipelines, NumPy. FastAPI perf is sufficient with async + uvloop

### Frontend: Next.js 15 App Router (RSC + Server Actions)
- **Why:** React Server Components eliminate client JS for static/dynamic content. Server Actions enable mutation without API boilerplate
- State: Zustand (lightweight) + TanStack Query (server state) + zustand/context for auth/ui

### Database: PostgreSQL + Redis
- PostgreSQL: JSONB for flexible schemas (Notes, Automation rules), tsvector for full-text search, partitioning for Trading/Finance time-series
- Redis: Session cache, rate-limit counters, WebSocket pub/sub, BullMQ job queue

### AI Engine: LangGraph + LiteLLM + RAG
- LangGraph for multi-agent orchestration (stateful graphs)
- LiteLLM for provider-agnostic LLM calls (OpenAI, Anthropic, local models)
- RAG: pgvector (Postgres extension) for HNSW-indexed embeddings

### Security First, Developer Experience Always
- JWT access/refresh token rotation (15m / 7d)
- All secrets vaulted via HashiCorp Vault or env vars (bound to K8s secrets)
- RBAC enforced at API gateway middleware + domain layer guard clauses

---

## 2. Complete Folder Structure

```
nexus-ai/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── cd.yml
│       └── release.yml
├── packages/
│   ├── kernel/
│   │   ├── src/
│   │   │   ├── types/           # Domain-agnostic base types
│   │   │   ├── errors/          # Base error classes
│   │   │   ├── utils/           # Shared utilities
│   │   │   └── constants/       # Global constants
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── ui-system/
│   │   ├── src/
│   │   │   ├── atoms/           # Button, Input, Icon, Badge, Avatar, Spinner
│   │   │   ├── molecules/       # Card, Dropdown, Modal, Drawer, Toast
│   │   │   ├── organisms/       # Sidebar, Dock, CommandPalette, SearchBar
│   │   │   ├── templates/       # PageLayout, AuthLayout, WorkspaceLayout
│   │   │   ├── animations/      # Framer Motion presets
│   │   │   └── tokens/          # Colors, spacing, typography, shadows
│   │   ├── tailwind.config.ts
│   │   └── package.json
│   ├── api-client/
│   │   ├── src/
│   │   │   ├── generated/       # OpenAPI → TypeScript
│   │   │   ├── hooks/           # TanStack Query hooks per domain
│   │   │   └── websocket/       # WS connection manager
│   │   └── package.json
│   └── config-eslint/
├── apps/
│   ├── web/                     # Next.js 15 (App Router)
│   │   ├── src/
│   │   │   ├── app/
│   │   │   │   ├── (auth)/      # login, register, forgot-password, 2fa
│   │   │   │   ├── (dashboard)/ # Main workspace layout
│   │   │   │   ├── (marketing)/ # Landing, pricing, about
│   │   │   │   └── api/         # Next.js API route proxies
│   │   │   ├── modules/
│   │   │   │   ├── ai-assistant/     # Chat, agents, RAG
│   │   │   │   ├── dashboard/        # Widgets, analytics
│   │   │   │   ├── notes/            # Rich text, markdown
│   │   │   │   ├── tasks/            # Kanban, calendar, pomodoro
│   │   │   │   ├── calendar/         # Events, sync, scheduling
│   │   │   │   ├── documents/        # PDF, Office, OCR, annotations
│   │   │   │   ├── finance/          # Budget, expenses, analytics
│   │   │   │   ├── trading/          # Journal, risk, perf analytics
│   │   │   │   ├── news/             # Intelligence, sentiment
│   │   │   │   ├── automation/       # Workflow builder, triggers
│   │   │   │   ├── collaboration/    # Workspace, comments, mentions
│   │   │   │   ├── cloud-storage/    # Upload, preview, versioning
│   │   │   │   ├── passwords/        # Vault, encryption, sharing
│   │   │   │   └── marketplace/      # Plugins, SDK, integrations
│   │   │   ├── components/     # Shared Next.js components
│   │   │   ├── hooks/          # Shared hooks
│   │   │   └── lib/            # Utilities, API client instance
│   │   ├── public/
│   │   ├── package.json
│   │   └── next.config.ts
│   └── mobile/                 # Future: React Native / Expo
├── backend/
│   ├── src/
│   │   ├── kernel/             # Shared kernel (BaseModel, errors, utils)
│   │   ├── config/             # Environment, logging, db, redis
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── auth/       # endpoints, schemas, dependencies
│   │   │   │   ├── ai/
│   │   │   │   ├── dashboard/
│   │   │   │   ├── notes/
│   │   │   │   ├── tasks/
│   │   │   │   ├── calendar/
│   │   │   │   ├── documents/
│   │   │   │   ├── finance/
│   │   │   │   ├── trading/
│   │   │   │   ├── news/
│   │   │   │   ├── automation/
│   │   │   │   ├── collaboration/
│   │   │   │   ├── storage/
│   │   │   │   ├── passwords/
│   │   │   │   ├── marketplace/
│   │   │   │   └── admin/
│   │   │   └── deps.py         # Dependency injection container
│   │   ├── domain/             # Domain entities & use-cases
│   │   │   ├── ai/
│   │   │   ├── dashboard/
│   │   │   ├── notes/
│   │   │   ├── tasks/
│   │   │   └── ... (per module)
│   │   ├── application/        # Use-case interactors
│   │   │   ├── auth/
│   │   │   ├── ai/
│   │   │   └── ...
│   │   ├── infrastructure/     # Adapters
│   │   │   ├── database/       # SQLAlchemy, migrations, repositories
│   │   │   ├── cache/          # Redis adapter
│   │   │   ├── storage/        # S3 adapter
│   │   │   ├── ai/             # LangChain, embeddings, RAG
│   │   │   ├── auth/           # JWT, OAuth, OIDC
│   │   │   ├── search/         # Elasticsearch / pgvector
│   │   │   ├── queue/          # Celery / BullMQ bridge
│   │   │   ├── notifications/  # Email, push, webhook
│   │   │   └── payment/        # Stripe adapter
│   │   └── main.py             # FastAPI app factory
│   ├── alembic/                # DB migrations
│   ├── tests/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── poetry.lock
├── ai-engine/
│   ├── agents/                 # LangGraph agent definitions
│   ├── tools/                  # Tool definitions (calculator, search, coding)
│   ├── memory/                 # Long-term, episodic, semantic memory
│   ├── rag/                    # Chunking, embedding, retrieval pipelines
│   ├── workflows/              # Multi-agent orchestration DAGs
│   ├── server.py               # gRPC / FastAPI sidecar
│   ├── Dockerfile
│   └── pyproject.toml
├── infrastructure/
│   ├── docker/
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.prod.yml
│   │   └── docker-compose.ai.yml
│   ├── k8s/
│   │   ├── namespaces/
│   │   ├── deployments/
│   │   ├── services/
│   │   ├── ingresses/
│   │   └── pvcs/
│   ├── terraform/
│   │   ├── modules/
│   │   ├── staging/
│   │   └── production/
│   └── monitoring/
│       ├── prometheus/
│       ├── grafana/
│       └── loki/
├── .env.example
├── .gitignore
├── .prettierrc
├── .eslintrc.js
├── turbo.json
├── package.json (root - pnpm workspaces)
├── pnpm-workspace.yaml
└── README.md
```

---

## 3. Database Schema (PostgreSQL)

### Core / Auth

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    display_name VARCHAR(100),
    avatar_url TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    is_2fa_enabled BOOLEAN DEFAULT FALSE,
    two_factor_secret TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- OAuth Accounts
CREATE TABLE oauth_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL, -- google, github, microsoft
    provider_user_id VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(provider, provider_user_id)
);

-- Sessions
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    refresh_token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    revoked_at TIMESTAMPTZ
);

-- Workspaces
CREATE TABLE workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    plan VARCHAR(20) DEFAULT 'free', -- free, pro, business, enterprise
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Workspace Members
CREATE TABLE workspace_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member', -- owner, admin, member, viewer
    permissions JSONB DEFAULT '[]',
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(workspace_id, user_id)
);

-- API Keys
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100),
    key_hash VARCHAR(255) NOT NULL,
    scopes JSONB DEFAULT '[]',
    last_used_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### AI Assistant

```sql
-- AI Conversations
CREATE TABLE ai_conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    title TEXT,
    model VARCHAR(50) DEFAULT 'gpt-4o',
    system_prompt TEXT,
    metadata JSONB DEFAULT '{}',
    token_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- AI Messages
CREATE TABLE ai_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES ai_conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- user, assistant, system, tool
    content TEXT NOT NULL,
    tool_calls JSONB,
    tool_call_id VARCHAR(255),
    attachments JSONB DEFAULT '[]',
    tokens INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- AI Memory
CREATE TABLE ai_memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    key VARCHAR(255) NOT NULL,
    value TEXT NOT NULL,
    type VARCHAR(50) DEFAULT 'fact', -- fact, preference, episodic, semantic
    importance REAL DEFAULT 0.5,
    embedding VECTOR(1536),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index
CREATE INDEX idx_ai_memories_embedding ON ai_memories USING ivfflat (embedding vector_cosine_ops);
```

### Notes

```sql
CREATE TABLE notes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    author_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) DEFAULT 'Untitled',
    content TEXT,
    content_plain TEXT,
    content_json JSONB,
    note_type VARCHAR(20) DEFAULT 'document', -- document, canvas, whiteboard
    icon VARCHAR(50),
    cover_url TEXT,
    color VARCHAR(20),
    is_published BOOLEAN DEFAULT FALSE,
    is_archived BOOLEAN DEFAULT FALSE,
    is_template BOOLEAN DEFAULT FALSE,
    version INTEGER DEFAULT 1,
    parent_id UUID REFERENCES notes(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE note_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(20)
);

CREATE TABLE note_tag_map (
    note_id UUID REFERENCES notes(id) ON DELETE CASCADE,
    tag_id UUID REFERENCES note_tags(id) ON DELETE CASCADE,
    PRIMARY KEY (note_id, tag_id)
);

CREATE TABLE note_backlinks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID REFERENCES notes(id) ON DELETE CASCADE,
    target_id UUID REFERENCES notes(id) ON DELETE CASCADE,
    context TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE note_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    note_id UUID REFERENCES notes(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    version INTEGER NOT NULL,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Tasks

```sql
CREATE TABLE task_lists (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    color VARCHAR(20),
    icon VARCHAR(50),
    view_type VARCHAR(20) DEFAULT 'kanban',
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    list_id UUID REFERENCES task_lists(id) ON DELETE CASCADE,
    assignee_id UUID REFERENCES users(id) ON DELETE SET NULL,
    created_by UUID REFERENCES users(id),
    title VARCHAR(500) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'backlog', -- backlog, todo, in_progress, review, done
    priority VARCHAR(10) DEFAULT 'medium', -- urgent, high, medium, low
    labels JSONB DEFAULT '[]',
    due_date TIMESTAMPTZ,
    start_date TIMESTAMPTZ,
    estimated_minutes INTEGER,
    sort_order REAL,
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_rule TEXT, -- RRULE
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE task_subtasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE pomodoro_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
    duration_minutes INTEGER DEFAULT 25,
    break_minutes INTEGER DEFAULT 5,
    completed_pomodoros INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'completed',
    started_at TIMESTAMPTZ,
    ended_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Calendar

```sql
CREATE TABLE calendar_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    creator_id UUID REFERENCES users(id),
    title VARCHAR(300) NOT NULL,
    description TEXT,
    location TEXT,
    is_all_day BOOLEAN DEFAULT FALSE,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    timezone VARCHAR(50) DEFAULT 'UTC',
    recurrence_rule TEXT,
    google_event_id VARCHAR(255),
    calendar_provider VARCHAR(20), -- google, outlook, internal
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE calendar_attendees (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id UUID REFERENCES calendar_events(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    email VARCHAR(255),
    status VARCHAR(20) DEFAULT 'pending', -- accepted, declined, tentative, pending
    UNIQUE(event_id, user_id)
);
```

### Finance

```sql
CREATE TABLE finance_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(30) DEFAULT 'checking', -- checking, savings, credit, cash, investment
    currency VARCHAR(3) DEFAULT 'USD',
    balance DECIMAL(15,2) DEFAULT 0,
    is_archived BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE finance_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    icon VARCHAR(50),
    color VARCHAR(20),
    type VARCHAR(10) NOT NULL, -- income, expense, transfer
    parent_id UUID REFERENCES finance_categories(id)
);

CREATE TABLE finance_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID REFERENCES finance_accounts(id) ON DELETE CASCADE,
    category_id UUID REFERENCES finance_categories(id),
    created_by UUID REFERENCES users(id),
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    description TEXT,
    merchant VARCHAR(200),
    type VARCHAR(10) NOT NULL, -- income, expense, transfer
    status VARCHAR(20) DEFAULT 'cleared', -- pending, cleared, reconciled
    date DATE NOT NULL,
    is_recurring BOOLEAN DEFAULT FALSE,
    recurrence_rule TEXT,
    tags JSONB DEFAULT '[]',
    receipt_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE budgets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    category_id UUID REFERENCES finance_categories(id),
    name VARCHAR(100) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    period VARCHAR(20) DEFAULT 'monthly', -- weekly, monthly, yearly
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    provider VARCHAR(100),
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    billing_cycle VARCHAR(20) DEFAULT 'monthly',
    next_billing_date DATE,
    category VARCHAR(100),
    logo_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Trading

```sql
CREATE TABLE trading_journal (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    instrument VARCHAR(20) NOT NULL, -- BTCUSD, AAPL, EURUSD
    trade_type VARCHAR(10) NOT NULL, -- long, short
    entry_price DECIMAL(15,5) NOT NULL,
    exit_price DECIMAL(15,5),
    quantity DECIMAL(15,5) NOT NULL,
    stop_loss DECIMAL(15,5),
    take_profit DECIMAL(15,5),
    fees DECIMAL(10,2) DEFAULT 0,
    pnl DECIMAL(15,2),
    pnl_percent DECIMAL(8,2),
    setup VARCHAR(500),
    tags JSONB DEFAULT '[]',
    emotion_before VARCHAR(50),
    emotion_after VARCHAR(50),
    screenshot_url TEXT,
    lesson TEXT,
    entry_time TIMESTAMPTZ NOT NULL,
    exit_time TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE trading_strategies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    rules JSONB,
    performance JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Documents

```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    uploaded_by UUID REFERENCES users(id),
    original_name VARCHAR(500) NOT NULL,
    storage_key TEXT NOT NULL,
    mime_type VARCHAR(100),
    size_bytes BIGINT,
    page_count INTEGER,
    ocr_text TEXT,
    ai_summary TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE document_annotations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    page_number INTEGER,
    annotation_type VARCHAR(20), -- highlight, underline, comment, drawing
    coordinates JSONB,
    content TEXT,
    color VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Automation

```sql
CREATE TABLE automation_workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    trigger_type VARCHAR(50) NOT NULL,
    trigger_config JSONB NOT NULL,
    steps JSONB NOT NULL, -- ordered array of action definitions
    is_active BOOLEAN DEFAULT TRUE,
    last_run_at TIMESTAMPTZ,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE automation_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID REFERENCES automation_workflows(id) ON DELETE CASCADE,
    triggered_by UUID REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'success',
    input JSONB,
    output JSONB,
    error_message TEXT,
    duration_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Cloud Storage

```sql
CREATE TABLE storage_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    uploaded_by UUID REFERENCES users(id),
    name VARCHAR(500) NOT NULL,
    storage_key TEXT NOT NULL,
    mime_type VARCHAR(100),
    size_bytes BIGINT,
    checksum VARCHAR(64),
    is_encrypted BOOLEAN DEFAULT FALSE,
    parent_id UUID REFERENCES storage_files(id) ON DELETE CASCADE,
    is_folder BOOLEAN DEFAULT FALSE,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE storage_shares (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_id UUID REFERENCES storage_files(id) ON DELETE CASCADE,
    shared_by UUID REFERENCES users(id),
    shared_with UUID REFERENCES users(id),
    permission VARCHAR(20) DEFAULT 'view', -- view, edit, admin
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Password Manager

```sql
CREATE TABLE password_vault_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    url TEXT,
    username_encrypted TEXT NOT NULL,
    password_encrypted TEXT NOT NULL,
    notes_encrypted TEXT,
    otp_secret_encrypted TEXT,
    category VARCHAR(50),
    tags JSONB DEFAULT '[]',
    strength_score INTEGER,
    last_used_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### News Intelligence

```sql
CREATE TABLE news_articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    url TEXT UNIQUE,
    source VARCHAR(200),
    author VARCHAR(200),
    content TEXT,
    summary TEXT,
    sentiment REAL,
    topics JSONB DEFAULT '[]',
    entities JSONB DEFAULT '[]',
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE news_bookmarks (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    article_id UUID REFERENCES news_articles(id) ON DELETE CASCADE,
    folder VARCHAR(100) DEFAULT 'default',
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, article_id)
);
```

### Collaboration

```sql
CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    author_id UUID REFERENCES users(id),
    resource_type VARCHAR(50) NOT NULL, -- note, task, document, event
    resource_id UUID NOT NULL,
    parent_id UUID REFERENCES comments(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE mentions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    comment_id UUID REFERENCES comments(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    resource_type VARCHAR(50),
    resource_id UUID,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE activity_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50),
    resource_id UUID,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 4. API Endpoints Design (REST + WebSocket)

### Auth `/api/v1/auth`
```
POST   /register                        # Create account
POST   /login                           # Login -> tokens
POST   /refresh                         # Refresh access token
POST   /logout                          # Revoke refresh token
POST   /verify-email                    # Verify email with code
POST   /forgot-password                 # Send reset email
POST   /reset-password                  # Reset with token
POST   /oauth/{provider}                # OAuth login (Google, GitHub)
POST   /2fa/enable                      # Enable 2FA
POST   /2fa/verify                      # Verify 2FA code
GET    /me                              # Current user profile
PATCH  /me                              # Update profile
```

### AI Assistant `/api/v1/ai`
```
WebSocket /chat/{conversation_id}       # Streaming conversation
POST   /conversations                   # Create conversation
GET    /conversations                   # List conversations
GET    /conversations/{id}              # Get conversation
DELETE /conversations/{id}              # Delete conversation
POST   /conversations/{id}/messages     # Send message (non-streaming)
POST   /generate                        # Single prompt completion
POST   /summarize                       # Summarize text
POST   /translate                       # Translate text
POST   /rewrite                         # Rewrite text
POST   /analyze-sentiment               # Sentiment analysis
POST   /extract-entities                # NER extraction
POST   /classify                        # Text classification
GET    /memory                          # Get user memories
POST   /memory                          # Store memory
DELETE /memory/{id}                     # Delete memory
```

### Dashboard `/api/v1/dashboard`
```
GET    /widgets                         # Get user's widgets
PUT    /widgets                         # Update widget layout
GET    /analytics                       # Dashboard analytics
GET    /activity                        # Recent activity
GET    /insights                        # AI-powered insights
```

### Notes `/api/v1/notes`
```
GET    /notes                           # List notes (paginated, filtered)
POST   /notes                           # Create note
GET    /notes/{id}                      # Get note (with content)
PATCH  /notes/{id}                      # Update note
DELETE /notes/{id}                      # Soft delete
POST   /notes/{id}/restore              # Restore from archive
GET    /notes/{id}/versions             # Version history
POST   /notes/{id}/versions/{v}/restore # Restore version
GET    /notes/{id}/backlinks            # Backlinks
GET    /tags                            # List workspace tags
POST   /tags                            # Create tag
POST   /notes/{id}/ai/summarize         # AI summarize
POST   /notes/{id}/ai/rewrite           # AI rewrite
POST   /notes/{id}/ai/translate         # AI translate
POST   /search                          # Full-text search notes
```

### Tasks `/api/v1/tasks`
```
GET    /lists                           # Task lists
POST   /lists                           # Create list
GET    /tasks                           # List tasks (filterable)
POST   /tasks                           # Create task
GET    /tasks/{id}                      # Get task
PATCH  /tasks/{id}                      # Update task
DELETE /tasks/{id}                      # Delete task
POST   /tasks/{id}/subtasks             # Add subtask
PATCH  /tasks/{id}/subtasks/{sid}       # Update subtask
DELETE /tasks/{id}/subtasks/{sid}       # Delete subtask
POST   /tasks/{id}/move                 # Move task (drag-drop)
POST   /pomodoro/start                  # Start pomodoro
POST   /pomodoro/stop                   # Stop pomodoro
GET    /pomodoro/stats                  # Pomodoro analytics
```

### Calendar `/api/v1/calendar`
```
GET    /events                          # List events (date range)
POST   /events                          # Create event
GET    /events/{id}                     # Get event
PATCH  /events/{id}                     # Update event
DELETE /events/{id}                     # Delete event
POST   /events/{id}/attendees           # Add attendee
DELETE /events/{id}/attendees/{uid}     # Remove attendee
POST   /sync/google                     # Trigger Google sync
GET    /availability                    # Get user availability
POST   /ai/schedule                     # AI scheduling assistant
```

### Finance `/api/v1/finance`
```
GET    /accounts                        # List accounts
POST   /accounts                        # Create account
PATCH  /accounts/{id}                   # Update account
GET    /transactions                    # List transactions
POST   /transactions                    # Create transaction
PATCH  /transactions/{id}               # Update transaction
DELETE /transactions/{id}               # Delete transaction
POST   /transactions/import             # CSV import
GET    /categories                      # List categories
POST   /categories                      # Create category
GET    /budgets                         # List budgets
POST   /budgets                         # Create budget
PUT    /budgets/{id}                    # Update budget
GET    /subscriptions                   # List subscriptions
POST   /subscriptions                   # Add subscription
PATCH  /subscriptions/{id}              # Update subscription
DELETE /subscriptions/{id}              # Delete subscription
GET    /analytics/overview              # Financial overview
GET    /analytics/spending              # Spending breakdown
GET    /analytics/trends                # Trends over time
GET    /analytics/forecast              # AI spending forecast
```

### Trading `/api/v1/trading`
```
GET    /journal                         # List trades (paginated)
POST   /journal                         # Record new trade
PATCH  /journal/{id}                    # Update trade
DELETE /journal/{id}                    # Delete trade
GET    /stats                           # Performance stats
GET    /stats/winrate                   # Win rate analysis
GET    /stats/rr                        # Risk/Reward analysis
GET    /stats/equity-curve              # Equity curve data
GET    /strategies                      # List strategies
POST   /strategies                      # Create strategy
PATCH  /strategies/{id}                 # Update strategy
DELETE /strategies/{id}                 # Delete strategy
GET    /economic-calendar               # Economic events
GET    /risk/calculate                  # Risk calculator
```

### Documents `/api/v1/documents`
```
GET    /documents                       # List documents
POST   /documents/upload                # Upload document
GET    /documents/{id}                  # Download/document info
DELETE /documents/{id}                  # Delete document
POST   /documents/{id}/ocr              # Run OCR
POST   /documents/{id}/summarize        # AI summary
POST   /documents/{id}/extract          # AI extraction
GET    /documents/{id}/annotations      # Get annotations
POST   /documents/{id}/annotations      # Add annotation
DELETE /documents/{id}/annotations/{a}  # Delete annotation
```

### Automation `/api/v1/automation`
```
GET    /workflows                       # List workflows
POST   /workflows                       # Create workflow
GET    /workflows/{id}                  # Get workflow
PATCH  /workflows/{id}                  # Update workflow
DELETE /workflows/{id}                  # Delete workflow
POST   /workflows/{id}/trigger          # Manual trigger
GET    /workflows/{id}/logs             # Execution logs
GET    /integrations                    # Available integrations
POST   /integrations/{provider}/auth    # OAuth for integration
```

### Storage `/api/v1/storage`
```
GET    /files                           # List files/folders
POST   /files/upload                    # Upload file
POST   /files/folder                    # Create folder
GET    /files/{id}                      # File metadata
GET    /files/{id}/download             # Download (presigned URL)
PATCH  /files/{id}                      # Rename/move
DELETE /files/{id}                      # Delete
POST   /files/{id}/share                # Share file
DELETE /files/{id}/share/{share_id}     # Revoke share
GET    /files/{id}/versions             # Version history
```

### Passwords `/api/v1/passwords`
```
GET    /vault                           # List vault items
POST   /vault                           # Create item
GET    /vault/{id}                      # Get item (decrypted client-side)
PATCH  /vault/{id}                      # Update item
DELETE /vault/{id}                      # Delete item
POST   /vault/{id}/share                # Secure share
GET    /vault/strength                  # Password strength report
```

### News `/api/v1/news`
```
GET    /articles                        # List articles
GET    /articles/{id}                   # Get article
POST   /articles/{id}/bookmark          # Bookmark
DELETE /articles/{id}/bookmark          # Remove bookmark
GET    /topics                          # Detected topics
GET    /sentiment                       # Sentiment trends
```

### Collaboration `/api/v1/collab`
```
GET    /workspaces                      # List workspaces
POST   /workspaces                      # Create workspace
PATCH  /workspaces/{id}                 # Update workspace
DELETE /workspaces/{id}                 # Delete workspace
GET    /workspaces/{id}/members         # List members
POST   /workspaces/{id}/members         # Invite member
PATCH  /workspaces/{id}/members/{uid}   # Change role
DELETE /workspaces/{id}/members/{uid}   # Remove member
GET    /comments                        # List comments (by resource)
POST   /comments                        # Create comment
PATCH  /comments/{id}                   # Update comment
DELETE /comments/{id}                   # Delete comment
GET    /notifications                   # List notifications
PATCH  /notifications/{id}/read         # Mark read
```

### Admin `/api/v1/admin`
```
GET    /users                           # List users
GET    /users/{id}                      # User details
PATCH  /users/{id}                      # Update user
DELETE /users/{id}                      # Suspend user
GET    /analytics                       # Platform analytics
GET    /audit-logs                      # Audit trail
POST   /announcements                   # Send announcement
```

---

## 5. Authentication Flow

```
┌─────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ Browser │     │  Next.js │     │ FastAPI  │     │    DB    │
│ (Client)│     │ (Server) │     │ Backend  │     │PostgreSQL│
└────┬────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │                │
     │── POST /login ──│── POST /auth ──│───────────────│
     │ (email+pass)    │   /api/v1/     │                │
     │                 │   /auth/login  │── Verify ──────│
     │                 │                │   password hash│
     │                 │                │<── user_row ───│
     │                 │                │                │
     │                 │                │── Generate ────│
     │                 │                │   access_token │
     │                 │                │   refresh_token│
     │                 │                │── Store ───────│
     │                 │                │   refresh hash │
     │                 │                │                │
     │<── Set HTTP ────│<── 200 OK ─────│<───────────────│
     │ Only Cookie     │  { access,     │                │
     │ (refresh_token) │    user }      │                │
     │                 │                │                │
     │── Store ────────│                │                │
     │   access_token  │                │                │
     │   in memory     │                │                │
     │   (Zustand)     │                │                │
```

**Token Strategy:**
- **Access Token:** JWT, 15 min TTL, signed with RS256 (public/private key pair)
- **Refresh Token:** Opaque, 7 day TTL, stored as bcrypt hash in DB, HttpOnly cookie
- **Rotation:** Every refresh issues a new refresh token, old one revoked
- **Replay Detection:** `jti` claim in JWT + Redis blacklist for immediate revocation

**OAuth Flow:** PKCE + State parameter. Callback exchanges auth code for tokens.

---

## 6. UI Design System

### Design Tokens

```typescript
// Colors
--color-bg-primary: #ffffff / #0a0a0f
--color-bg-secondary: #f8f9fa / #12121a
--color-bg-tertiary: #f0f0f5 / #1a1a2e
--color-bg-glass: rgba(255,255,255,0.7) / rgba(10,10,15,0.7)
--color-border: #e5e7eb / #2a2a3e
--color-text-primary: #0a0a0f / #f0f0f5
--color-text-secondary: #6b7280 / #9ca3af
--color-accent: #6366f1 / #818cf8      // Indigo
--color-accent-secondary: #8b5cf6 / #a78bfa  // Violet
--color-success: #10b981 / #34d399
--color-warning: #f59e0b / #fbbf24
--color-error: #ef4444 / #f87171
--color-info: #3b82f6 / #60a5fa

// Typography
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif
--font-mono: 'JetBrains Mono', 'Fira Code', monospace
--font-size-xs: 0.75rem
--font-size-sm: 0.875rem
--font-size-base: 1rem
--font-size-lg: 1.125rem
--font-size-xl: 1.25rem
--font-size-2xl: 1.5rem
--font-size-3xl: 2rem
--font-size-4xl: 2.5rem

// Spacing: 4px base
--space-1: 0.25rem  // 4px
--space-2: 0.5rem   // 8px
--space-3: 0.75rem  // 12px
--space-4: 1rem     // 16px
--space-5: 1.25rem  // 20px
--space-6: 1.5rem   // 24px
--space-8: 2rem     // 32px
--space-10: 2.5rem  // 40px
--space-12: 3rem    // 48px
--space-16: 4rem    // 64px

// Radii
--radius-sm: 0.375rem
--radius-md: 0.5rem
--radius-lg: 0.75rem
--radius-xl: 1rem
--radius-2xl: 1.5rem

// Shadows
--shadow-sm, --shadow-md, --shadow-lg, --shadow-xl, --shadow-2xl
// Dark mode: colored shadows with low opacity on accent
```

### Component Architecture

```
Atoms (design primitives)
├── Button (variants: primary, secondary, ghost, danger, outline)
│   └── sizes: xs, sm, md, lg, xl
├── Input (text, search, password, number, email, url, tel)
│   └── states: default, focus, error, disabled, loading
├── Icon (Lucide icons, 24x24, customizable strokeWidth)
├── Badge (variants: default, success, warning, error, info, premium)
├── Avatar (image, initials fallback, status dot, group)
├── Spinner (size variants, color inheritance)
├── Skeleton (loading placeholder)
├── Text (variant: h1-h6, p, span, small; weight, color)
├── Divider
└── Tooltip

Molecules (composed atoms)
├── Card (header, content, footer; clickable, hover, selected)
├── Modal (header, body, footer; sizes: sm, md, lg, xl, full)
├── Drawer (left, right, bottom; sizes)
├── DropdownMenu (items, separators, icons, disabled, check)
├── CommandPalette (⌘K, command+search, keyboard navigation)
├── Toast (success, error, warning, info; undo action)
├── Tabs (line, pill, underline variants)
├── Accordion
├── Select (native-like, searchable)
├── Switch (toggle)
├── Checkbox
├── RadioGroup
├── Calendar (date picker, range picker)
├── Table (sortable, filterable, selectable rows)
├── FormField (label, input, error, helper text)
├── Breadcrumb
├── Pagination
└── ProgressBar

Organisms (feature composites)
├── Sidebar (collapsible, icons, labels, badges, active state)
├── Dock (macOS-style pinned apps, hover expand)
├── TopBar (breadcrumb, search, actions, avatar)
├── SearchBar (global search, recent, results)
├── WorkspaceLayout (sidebar + main + right panel)
├── SplitView (resizable, horizontal/vertical)
├── KanbanBoard (columns, cards, drag-drop)
├── CalendarView (month/week/day/agenda)
├── RichTextEditor (Notion-like, slash commands, /menu)
├── Chart (line, bar, area, pie, candlestick)
├── WidgetGrid (draggable, resizable, customizable)
├── FileUploader (drag-drop, preview, progress)
├── ActivityFeed
└── NotificationCenter

Templates (page-level)
├── AuthLayout (centered card, logo, social buttons)
├── DashboardLayout (sidebar + header + content)
├── SettingsLayout (sidebar tabs + content)
└── LandingLayout (marketing header + sections + footer)
```

---

## 7. AI Engine Architecture

```
┌────────────────────────────────────────────────────────────┐
│                     AI Engine (Sidecar)                     │
│                                                             │
│  ┌───────────┐  ┌──────────┐  ┌──────────────────────────┐ │
│  │ LangGraph  │  │ LiteLLM  │  │  RAG Pipeline             │ │
│  │ Orchestr.  │  │ Router   │  │                           │ │
│  │            │  │          │  │  ┌─────┐ ┌──────┐ ┌───┐  │ │
│  │ Supervisor │  │ OpenAI   │  │  │Chunk│ │Embed │ │Retr│  │ │
│  │ Researcher │  │ Anthropic│  │  └─────┘ └──────┘ └───┘  │ │
│  │ Writer     │  │ Local    │  │                           │ │
│  │ Coder      │  │ OpenRouter│  └──────────────────────────┘ │
│  │ Analyst    │  └──────────┘                               │
│  └───────────┘                                              │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Memory System                                        │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │   │
│  │  │Episodic  │  │Semantic  │  │Working (Context)  │   │   │
│  │  └──────────┘  └──────────┘  └──────────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Tools                                                │   │
│  │  Python REPL | Calculator | Search | Weather          │   │
│  │  Code Interpreter | File System | DB Query           │   │
│  │  Trading Analysis | Chart Generator | Email          │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  Communication: gRPC stream (backend) + WebSocket (client)  │
└─────────────────────────────────────────────────────────────┘
```

**Multi-Agent Supervisor Pattern:**
- **Supervisor Agent:** Routes user intent to specialized sub-agents
- **Researcher Agent:** Web search, document retrieval, fact-checking
- **Writer Agent:** Content creation, rewriting, formatting
- **Coder Agent:** Code generation, review, debugging
- **Analyst Agent:** Data analysis, chart generation, insights
- **Finance Agent:** Market data, portfolio analysis
- Each agent has its own tools + memory context

---

## 8. Security Architecture

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Client  │───▶│  Next.js │───▶│ FastAPI  │───▶│Database  │
│          │    │  (Proxy) │    │          │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │               │
     │ JWT Bearer    │ Cookies       │ Rate Limit    │ Encrypted
     │ (access)      │ (refresh)     │ RBAC          │ at rest
     │               │               │ Input Validate│
     │               │               │ CORS          │
     │               │               │ Helmet        │
     │               │               │ SQL Inj Guard │
     │               │               │ Audit Log     │
```

**Defense in Depth:**
1. **Transport:** HTTPS-only, HSTS, CSP headers
2. **Authentication:** Short-lived JWTs, rotated refresh tokens, 2FA (TOTP)
3. **Authorization:** RBAC at middleware + domain guard clauses
4. **Input Validation:** Pydantic strict mode everywhere
5. **Rate Limiting:** Token bucket per endpoint, per user, per IP
6. **Database:** Parameterized queries (SQLAlchemy), encrypted at rest, VPC
7. **Secrets:** Never in code; HashiCorp Vault or K8s secrets
8. **Audit:** Immutable log of all sensitive operations
9. **Encryption:** AES-256-GCM at rest for PII, passwords, vault items
10. **XSS:** React's built-in escaping, CSP, no dangerouslySetInnerHTML

---

## 9. Performance Strategy

| Concern | Solution |
|---------|----------|
| API Latency | Redis caching, DB connection pooling, async endpoints |
| Static Assets | CDN (Cloudflare), immutable caching, brotli compression |
| Images | next/image, WebP/AVIF, responsive srcset, lazy loading |
| Bundle Size | Dynamic imports, code splitting, tree shaking |
| React Rendering | RSC, memo, useMemo, virtualization (react-window) |
| DB Queries | Indexed, paginated, N+1 prevention (selectinload) |
| Background Jobs | Celery + Redis for heavy tasks (OCR, AI, CSV import) |
| Real-time | WebSocket with binary frames + compression |
| Startup | Turborepo caching, lazy module loading |

---

## 10. Caching Strategy

```
┌──────────────────────────────────────────────┐
│                 Cache Layers                  │
│                                              │
│  Browser Cache (SWR for API routes)          │
│      ↓                                       │
│  TanStack Query (in-memory, stale-while-reval)│
│      ↓                                       │
│  Next.js (RSC cache, ISR for static pages)   │
│      ↓                                       │
│  Redis (session, rate-limit, hot data)       │
│      ↓                                       │
│  PostgreSQL (shared buffers, query cache)    │
└──────────────────────────────────────────────┘
```

---

## 11. Observability

| Pillar | Tool | Purpose |
|--------|------|---------|
| Logs | Loki + promtail | Centralized structured logging |
| Metrics | Prometheus + Grafana | System + business KPIs |
| Traces | OpenTelemetry + Jaeger | Distributed tracing |
| Alerts | Alertmanager | PagerDuty / Slack |
| Uptime | Uptime Kuma | External monitoring |
| Error Tracking | Sentry | Frontend + backend exception tracking |

---

## 12. Implementation Roadmap

### Phase 0 — Foundation (Week 1-2)
- [x] Architecture document
- [ ] Monorepo scaffolding (Turborepo, pnpm)
- [ ] Backend project setup (FastAPI, SQLAlchemy, Alembic)
- [ ] Frontend project setup (Next.js 15, Tailwind, shadcn/ui)
- [ ] UI System package (Design tokens, atoms, molecules)
- [ ] Docker Compose for local dev (Postgres, Redis, MinIO)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Authentication module (register, login, OAuth, JWT, 2FA)

### Phase 1 — Core (Week 3-4)
- [ ] Dashboard (widgets, analytics, activity)
- [ ] Notes (rich text, markdown, tags, folders, backlinks, versions)
- [ ] Tasks (kanban, calendar, priority, subtasks, pomodoro)
- [ ] Calendar (events, Google sync, scheduling)
- [ ] Workspace & collaboration base (members, roles, comments)

### Phase 2 — Intelligence (Week 5-6)
- [ ] AI Assistant (chat, streaming, memory)
- [ ] RAG pipeline (chunking, embeddings, pgvector)
- [ ] Multi-agent system (supervisor + sub-agents)
- [ ] AI features for Notes (summarize, rewrite, translate)
- [ ] AI features for Documents (OCR, summary, extraction)
- [ ] News Intelligence (scraping, summarization, sentiment)

### Phase 3 — Advanced (Week 7-8)
- [ ] Finance module (accounts, transactions, budgets, subscriptions)
- [ ] Trading module (journal, analytics, risk, economic calendar)
- [ ] Automation engine (workflow builder, triggers, actions)
- [ ] Cloud Storage (upload, preview, versioning, sharing)
- [ ] Password Manager (vault, encryption, sharing)

### Phase 4 — Scale (Week 9-10)
- [ ] API Marketplace (plugin system, SDK, webhooks)
- [ ] Performance optimization (caching, lazy loading, virtualization)
- [ ] Kubernetes manifests, Helm charts
- [ ] Terraform infrastructure provisioning
- [ ] Monitoring stack (Prometheus, Grafana, Loki, Sentry)
- [ ] Load testing + hardening

### Phase 5 — Enterprise (Week 11-12)
- [ ] SSO (SAML, OIDC)
- [ ] Advanced RBAC + custom roles
- [ ] Audit logs + compliance
- [ ] Data export / GDPR
- [ ] White-labeling options
- [ ] On-premise deployment option

---

## 13. Technology Evaluation & Decisions

| Decision | Choice | Alternatives Considered | Reason |
|----------|--------|------------------------|--------|
| Monorepo | Turborepo | Nx, Lerna | Simpler config, faster caching |
| Backend | FastAPI | Node/Express, Go, Rust | Python AI/ML ecosystem |
| ORM | SQLAlchemy 2.0 | Prisma, Drizzle, SQLModel | Async, mature, composable |
| Validation | Pydantic v2 | Zod, Marshmallow | Performance, native in FastAPI |
| UI Framework | shadcn/ui | MUI, Radix, Chakra | Unstyled + Tailwind, copy-paste model |
| State | Zustand | Redux, Jotai | Minimal boilerplate, TS-native |
| Server State | TanStack Query | SWR, RTK Query | Caching, invalidation, devtools |
| Rich Text | Tiptap (ProseMirror) | Slate, Quill, Lexical | Extensible, collaboration-ready |
| AI Framework | LangGraph | LangChain, AutoGen, CrewAI | Stateful graphs, tool calling |
| LLM Router | LiteLLM | Direct SDK | Provider-agnostic, cost tracking |
| Charts | Recharts + TradingView | Chart.js, D3, ECharts | React-native, TradingView for trading |
| Task Queue | Celery + Redis | BullMQ, RabbitMQ | Mature Python ecosystem |
| Search | pgvector | Elasticsearch | Simpler infra, good enough, no extra service |
| Streaming | WebSocket | SSE, gRPC | Bidirectional, browser-native |

---

## 14. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| AI cost explosion | High | LiteLLM cost tracking, budget alerts, local models for simple tasks |
| LLM hallucination | High | RAG with source citation, confidence scoring, user verification step |
| Database migration complexity | Medium | Alembic with automated testing, staging DB, rollback scripts |
| WebSocket scaling | Medium | Redis pub/sub + horizontal scaling with sticky sessions |
| Third-party API rate limits | Medium | Queue with retries, caching, webhook fallbacks |
| Feature scope creep | High | Strict phase gating, "MVP first" mindset, feature flags |
| Security breach | Critical | Regular penetration testing, dependency scanning (Dependabot), audit logs |

---

## 15. Cost Projections (Monthly, 10k users)

| Service | Estimated Cost | Notes |
|---------|---------------|-------|
| LLM API | $5,000 | GPT-4o + Claude Sonnet, caching reduces |
| PostgreSQL | $200 | Managed (RDS or Supabase) |
| Redis | $50 | Upstash or self-hosted |
| S3 Storage | $100 | ~5TB storage + egress |
| CDN | $50 | Cloudflare |
| Compute | $400 | 4 x medium instances |
| Monitoring | $100 | Sentry + Grafana Cloud |
| **Total** | **~$5,900** | Scales linearly with users |
```

---

## Next Steps

The architecture above is the blueprint. Upon your approval, I will begin generating production-quality code following this exact structure, starting with:

1. **Monorepo initialization** (Turborepo, pnpm, shared configs)
2. **Backend foundation** (FastAPI, SQLAlchemy models, Alembic migrations)
3. **Frontend foundation** (Next.js 15, design system, authentication UI)
4. **Authentication flow** (full register/login/oauth/2fa backend + frontend)
5. **Docker Compose** for local development environment

Each phase builds on the previous, and all code will be ready for immediate `npm install && npm run dev`.
