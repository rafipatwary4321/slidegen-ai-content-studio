# SlideGen AI Content Studio

**Repository:** [`slidegen-ai-content-studio`](https://github.com/YOUR_USERNAME/slidegen-ai-content-studio)

AI-powered content platform that turns documents and prompts into polished creative output — starting with presentations and expanding to 25+ content categories.

---

## Short description

SlideGen AI Content Studio is a full-stack SaaS application built with **Next.js** and **FastAPI**. Upload a document to generate a native PowerPoint deck, or browse a Netflix-style marketplace of 25+ creative formats. Built iteratively with **Cursor AI** and documented end-to-end for portfolio review.

---

## Vision

What began as a simple **AI PPT maker** evolved into a universal **AI Content Studio** — better than a template picker because AI generates structure, content, and design intent from your input.

**North star:** Describe what you want → AI routes to the right generator → preview → export.

**Today (v1.1.0):** Marketplace browse + full PPT pipeline are production-stable. Advanced studio generation is architected in the backend and temporarily gated in the UI.

→ [Full vision doc](./docs/01-project-vision.md)

---

## Tech stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14, React 18, TypeScript, Tailwind CSS, Zustand |
| Backend | FastAPI, Pydantic, python-pptx, pypdf, python-docx |
| AI | OpenAI API (optional; heuristics fallback) |
| Auth | NextAuth credentials |
| Database | PostgreSQL + Prisma optional; JSON file store for local dev |

---

## Current features

| Feature | Route | Status |
|---------|-------|--------|
| Landing page | `/` | ✅ Working |
| Category marketplace | `/dashboard` | ✅ Search, featured, browse all 25 categories |
| PPT generator | `/dashboard/new` | ✅ Upload → analyze → outline → revise → PPTX |
| Presentation history | `/dashboard/history` | ✅ Requires sign-in |
| Category browse | `/dashboard/studio/[id]` | ✅ Info only — generation disabled |
| Auth | `/auth/signin`, `/auth/signup` | ✅ Working |

**Temporarily disabled (code remains):** Prompt-to-Design API flow, studio editor, brand kit, category AI generation.

---

## 25+ content categories

| # | Category | # | Category |
|---|----------|---|----------|
| 1 | Presentations ✅ | 14 | ID Cards |
| 2 | News Photocards | 15 | Flyers |
| 3 | Breaking News Cards | 16 | Brochures |
| 4 | Event Posters | 17 | Infographics |
| 5 | Facebook Posts | 18 | Resume Builder |
| 6 | Instagram Posts | 19 | Invitation Cards |
| 7 | Instagram Stories | 20 | Ad Creatives |
| 8 | Facebook Covers | 21 | Product Promotions |
| 9 | YouTube Thumbnails | 22 | NGO Campaign Materials |
| 10 | YouTube Community Posts | 23 | Real Estate Templates |
| 11 | Political Posters | 24 | Restaurant Marketing |
| 12 | Educational Posters | 25 | Podcast Covers |
| 13 | Certificates | | |

→ [Feature roadmap](./docs/05-feature-roadmap.md)

---

## How the app works

### PPT generator (active)

```
Upload PDF/DOCX/TXT
    → AI document analysis (OpenAI or heuristics)
    → Slide outline + persona + theme
    → Optional natural-language revision
    → Native .pptx export
```

Sign-in is optional for generate/export; required to save to history.

### Content Studio (architected)

```
Describe intent in marketplace
    → Intent classifier picks category
    → Universal Generator Engine produces layers
    → Visual editor + multi-format export
```

Studio generation UI is disabled in v1.1.0 for stability. Backend routes and registry are in place.

→ [System architecture](./docs/02-system-architecture.md)

---

## Folder structure

```
slidegen-ai-content-studio/
├── app/                        # Next.js App Router pages
│   ├── dashboard/              # Marketplace, PPT flow, studio routes
│   └── auth/                   # Sign in / sign up
├── components/
│   ├── studio/                 # Marketplace, prompt box, category UI
│   ├── presentation/           # PPT upload, outline, export
│   └── layout/                 # Sidebar, headers
├── lib/
│   ├── api/client.ts           # Typed FastAPI client
│   └── content-studio/         # Categories, store, templates
├── backend/
│   └── app/
│       ├── routes/             # REST endpoints
│       └── services/           # PPT + content generation logic
├── docs/                       # Portfolio documentation
│   ├── 01-project-vision.md
│   ├── 02-system-architecture.md
│   ├── 03-development-process.md
│   ├── 04-cursor-prompts.md
│   ├── 05-feature-roadmap.md
│   └── 06-github-process.md
├── scripts/                    # dev:clean, backend launcher
├── README.md
├── CHANGELOG.md
├── TODO.md
├── .env.example
└── .gitignore
```

---

## Local setup

### Prerequisites

- Node.js 18+
- Python 3.11+
- npm

### Install and run

```bash
npm install
cp .env.example .env.local          # macOS/Linux
copy .env.example .env.local        # Windows

cp backend/.env.example backend/.env   # optional — for OpenAI
npm run dev:clean                      # clears .next + starts both servers
```

| Service | URL |
|---------|-----|
| Frontend | http://127.0.0.1:3000 |
| API health | http://127.0.0.1:8000/health |

### Environment variables

**Frontend** (`.env.local`):

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXTAUTH_SECRET` | Yes (prod) | Random string, min 32 chars |
| `NEXTAUTH_URL` | Yes (prod) | e.g. `http://localhost:3000` |
| `NEXT_PUBLIC_API_BASE_URL` | No | Default `http://localhost:8000` |

**Backend** (`backend/.env`):

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Recommended | OpenAI API key |
| `OPENAI_MODEL` | No | Default `gpt-4o-mini` |
| `DATABASE_URL` | No | PostgreSQL; omit for JSON store |

### Scripts

| Command | Description |
|---------|-------------|
| `npm run dev:clean` | Clear `.next` cache, start frontend + backend |
| `npm run dev:all` | Next.js (:3000) + FastAPI (:8000) |
| `npm run build` | Production build |
| `npm run lint` | ESLint |

---

## GitHub process

First-time push:

```bash
git init
git add .
git commit -m "feat: stable v1.1.0 — SlideGen AI Content Studio"
git remote add origin https://github.com/YOUR_USERNAME/slidegen-ai-content-studio.git
git branch -M main
git push -u origin main
```

Future updates: `git status` → `git add .` → `git commit -m "message"` → `git push`

**Never commit:** `.env.local`, `backend/.env`, `node_modules/`, `.next/`, uploads, exports.

→ [Full GitHub guide](./docs/06-github-process.md)

---

## Roadmap

| Phase | Focus |
|-------|-------|
| **Phase 1** | PPT ✅, news photocard, poster, social post, certificate |
| **Phase 2** | Flyers, infographics, resume, ad creatives, invitations |
| **Phase 3** | Canva-like editor, marketplace, teams, billing, white-label |

→ [Detailed roadmap](./docs/05-feature-roadmap.md) · [Active tasks](./TODO.md)

---

## Documentation

| Doc | Contents |
|-----|----------|
| [01 — Project vision](./docs/01-project-vision.md) | PPT origin → Content Studio transformation |
| [02 — System architecture](./docs/02-system-architecture.md) | Frontend, backend, generator engine, export |
| [03 — Development process](./docs/03-development-process.md) | Cursor AI workflow, phased build, stability rules |
| [04 — Cursor prompts](./docs/04-cursor-prompts.md) | Major prompts used to build the project |
| [05 — Feature roadmap](./docs/05-feature-roadmap.md) | Phase 1–3 plan and 25 categories |
| [06 — GitHub process](./docs/06-github-process.md) | Init, commit, push, update workflow |

---

## API reference (active in UI)

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/v1/upload` | Document upload |
| POST | `/api/v1/documents/analyze` | AI analysis |
| POST | `/api/v1/outlines/generate` | Slide outline |
| POST | `/api/v1/outlines/revise` | Prompt revision |
| POST | `/api/v1/exports/pptx` | PPTX export |
| POST | `/api/v1/presentations` | Save to history |
| GET | `/api/v1/presentations` | List history |
| POST | `/api/v1/auth/signup`, `/auth/signin` | Authentication |

Content studio routes (`/content/*`) exist in backend but are not wired in the stable UI.

---

## License

Private — all rights reserved.
