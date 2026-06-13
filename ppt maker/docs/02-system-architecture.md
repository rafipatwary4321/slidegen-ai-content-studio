# System Architecture

## Overview

SlideGen AI Content Studio is a **full-stack monorepo** with a Next.js frontend and FastAPI backend. Two product surfaces share infrastructure:

1. **PPT Generator** — document → analysis → outline → PPTX (active in UI)
2. **Content Studio** — category marketplace + universal generation (backend ready; UI stabilized)

```
┌─────────────────────────────────────────────────────────────┐
│                     Next.js 14 Frontend                      │
│  Landing │ Marketplace │ PPT Generator │ Auth │ History     │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST /api/v1
┌──────────────────────────▼──────────────────────────────────┐
│                     FastAPI Backend                          │
│  Documents │ Outlines │ Exports │ Content │ Auth            │
└──────────────────────────┬──────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
   OpenAI API      JSON / Prisma       Local storage
   (optional)      persistence         (uploads, pptx)
```

---

## Frontend architecture

| Layer | Location | Role |
|-------|----------|------|
| **App Router** | `app/` | Pages: landing, dashboard, PPT flow, studio routes |
| **Components** | `components/` | UI: studio, presentation, forms, layout |
| **API client** | `lib/api/client.ts` | Typed fetch to FastAPI |
| **Content metadata** | `lib/content-studio/` | 25 categories, templates, Zustand store |
| **Auth** | `lib/auth.ts` + NextAuth | Credentials via backend |
| **Middleware** | `middleware.ts` | Protects history + saved presentations only |

### Key routes (stable)

| Route | Purpose |
|-------|---------|
| `/` | Landing page |
| `/dashboard` | Category marketplace |
| `/dashboard/new` | PPT generator |
| `/dashboard/history` | Saved presentations (auth) |
| `/dashboard/studio/[categoryId]` | Category browse (generation disabled) |

---

## Backend architecture

| Layer | Location | Role |
|-------|----------|------|
| **Routes** | `backend/app/routes/` | REST endpoints |
| **Services** | `backend/app/services/` | Business logic |
| **Models** | `backend/app/models/` | Pydantic schemas |
| **Jobs** | `backend/app/jobs/` | Export hooks (sync + async stub) |

### PPT pipeline services

```
upload → file_parser_service → analysis_service → outline_service
                                              ↓
                                    pptx_service → output/pptx/
```

- **openai_service** — structured JSON from OpenAI
- **document_heuristics** — fallback when OpenAI unavailable
- **theme_layout_service** — slide styling
- **presentation_store** — JSON or Prisma persistence

---

## Universal Generator Engine

The **ContentGenerationService** (`content_generation_service.py`) is the shared engine for all 25 categories.

**Input:** `ContentGenerateRequest` (category, prompt, aspect ratio, language, brand kit)

**Process:**
1. Resolve category spec from registry
2. Build canvas dimensions from aspect ratio
3. Call OpenAI for layer JSON (or heuristic fallback)
4. Return `StudioProjectModel` with layers

**Special case:** `presentations` + upload workflow delegates to `AIOrchestrationService` (existing PPT analysis).

---

## Generator Registry Pattern

Categories are registered in two places that stay in sync:

| Layer | File | Contents |
|-------|------|----------|
| Frontend | `lib/content-studio/categories.ts` | UI metadata: name, icon, gradient, exports |
| Backend | `backend/app/services/content/categories.py` | `CategorySpec`: id, default aspect, system hints |

```python
@dataclass(frozen=True)
class CategorySpec:
    id: str
    name: str
    default_aspect: str
    exports: tuple[str, ...]
    system_hint: str
```

Adding a category = one frontend entry + one backend `CategorySpec`. The universal engine handles the rest.

---

## Prompt-to-Design workflow

Architected end-to-end; **UI temporarily uses local search** in stable v1.1.0.

```
User prompt
    ↓
IntentClassifierService (OpenAI + keyword heuristics)
    ↓
IntentClassifyResponse (category, confidence, parameters)
    ↓
[Low confidence] → manual category picker
    ↓
PromptToDesignService → ContentGenerationService
    ↓
StudioProjectModel → editor / export
```

**API endpoints:**
- `POST /api/v1/content/classify-intent`
- `POST /api/v1/content/prompt-to-design`
- `POST /api/v1/content/generate`
- `POST /api/v1/content/export`

---

## Export pipeline

| Format | Handler | Status |
|--------|---------|--------|
| **PPTX** | `pptx_service.py` | Production — used by PPT UI |
| **ZIP** | `content_export_service.py` | Backend ready |
| **PNG/JPG/PDF** | `content_export_service.py` | Layer manifest stub; raster TBD |

PPT export flow: `POST /exports/pptx` → file in `backend/output/pptx/` → `GET /exports/pptx/{id}/download`

---

## Data & security

| Concern | Approach |
|---------|----------|
| Users | bcrypt + `backend/data/users.json` or Prisma |
| Presentations | JSON file or PostgreSQL |
| Uploads | `backend/storage/uploads/` (gitignored) |
| Secrets | `.env.local`, `backend/.env` (never committed) |
