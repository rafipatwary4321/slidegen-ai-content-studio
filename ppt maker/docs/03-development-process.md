# Development Process

## How this project was built with Cursor AI

SlideGen AI Content Studio was developed iteratively inside **Cursor IDE**, using AI-assisted coding with a deliberate phased approach.

---

## Core workflow

```
Prompt → Cursor generates/edits code → Local test → Fix → Commit
```

Each phase had a clear goal. New features were only added after the previous layer was **runnable on localhost**.

---

## Phase order

### 1. Frontend first

- Next.js 14 App Router scaffold
- Landing page, dashboard shell, sidebar, auth pages
- Upload box, persona/theme selectors, outline preview
- Tailwind styling and responsive layout

**Rule:** UI should render and navigate even before the backend exists.

### 2. Backend second

- FastAPI app with route modules
- Document parser (PDF, DOCX, TXT via pypdf / python-docx)
- Pydantic schemas for all API contracts
- JSON file persistence for local dev without PostgreSQL

**Rule:** Every endpoint returns valid JSON; errors use FastAPI `detail`.

### 3. Integration third

- `lib/api/client.ts` wired to all PPT endpoints
- NextAuth credentials calling backend auth routes
- End-to-end flow: upload → analyze → outline → export PPTX
- `npm run dev:all` to run both servers concurrently

**Rule:** Test the full PPT path before expanding scope.

### 4. Expansion fourth

- 25 category definitions (frontend + backend registry)
- Content Studio marketplace UI
- Universal Generator Engine + Intent Classifier
- Prompt-to-Design API and editor scaffold
- GitHub-ready repo hygiene

**Rule:** Expand architecture in code; stabilize UI before re-enabling advanced features.

---

## Stable-before-feature rule

After the Content Studio expansion, the project hit complexity issues:

- Corrupted `.next` cache when build ran during dev
- Unfinished studio UI depending on backend APIs
- Auth middleware blocking the entire dashboard

**Stabilization pass (v1.1.0):**

1. Disable unfinished UI (editor, brand kit, AI generation)
2. Keep marketplace browse + PPT generator working
3. Add `npm run dev:clean` for reliable localhost
4. Limit auth middleware to history routes only
5. Document everything before the next GitHub push

**Lesson:** Ship a working subset. Keep advanced code in the repo; gate it in the UI until verified.

---

## How prompts were used effectively

| Practice | Why it works |
|----------|--------------|
| **One goal per prompt** | “Fix PPT export” not “fix everything” |
| **List requirements as bullets** | Cursor follows structured specs better |
| **Say “do not explain, update files”** | Reduces prose, increases code output |
| **Ask for file list at the end** | Easier to review diffs |
| **Run `npm run build` after big changes** | Catches type errors early |
| **Stabilize before new features** | Prevents broken localhost |

---

## Local verification checklist

Before any commit:

```bash
npm run build        # must pass
npm run lint         # no errors
npm run dev:clean    # both servers start
```

Manual checks:

- http://127.0.0.1:3000 — landing
- http://127.0.0.1:3000/dashboard — marketplace
- http://127.0.0.1:3000/dashboard/new — PPT UI
- http://127.0.0.1:8000/health — API healthy

---

## Documentation process

This `docs/` folder documents the full journey from first PPT idea to stable v1.1.0 — intended as a **GitHub portfolio artifact** showing product vision, architecture, Cursor workflow, and release process.

See also: [04-cursor-prompts.md](./04-cursor-prompts.md), [06-github-process.md](./06-github-process.md)
