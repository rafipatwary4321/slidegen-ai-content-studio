# Cursor AI Prompts

Major prompts used to build SlideGen AI Content Studio. Copy and adapt these for similar projects.

---

## 1. Frontend starter

```
Build a Next.js 14 App Router frontend for SlideGen AI — an AI presentation generator.

Include:
- Landing page with hero, features, use cases
- Dashboard layout with sidebar
- New presentation page with upload box
- Auth pages (sign in / sign up)
- Tailwind CSS dark theme
- TypeScript throughout
```

---

## 2. Frontend polish

```
Polish the SlideGen AI frontend to premium SaaS quality.

- Glass panels, gradient backgrounds
- Responsive grid layouts
- Loading skeletons and error banners
- Consistent button and form components
- Page headers with eyebrow + title + description
```

---

## 3. Backend starter

```
Create a FastAPI backend for SlideGen AI.

Include:
- Route modules: auth, health, uploads, documents, outlines, exports, presentations
- Pydantic schemas for all request/response models
- CORS middleware
- JSON file persistence fallback when DATABASE_URL is unset
- requirements.txt with fastapi, uvicorn, pydantic, pypdf, python-docx, openai, python-pptx
```

---

## 4. Document parser

```
Implement real document parsing — no mock data.

- PDF via pypdf
- DOCX via python-docx
- TXT as plain text
- Validate file type and size (max 25MB)
- Return extracted text + metadata
```

---

## 5. OpenAI integration

```
Replace demo analysis with real OpenAI integration.

- Structured JSON responses for document analysis
- Include: title, persona, theme, outline, speaker notes, chart suggestions
- JSON fence parsing with validation
- Heuristics fallback when OPENAI_API_KEY is unset
- Environment variables for model and truncation limits
```

---

## 6. Frontend-backend connection

```
Wire the Next.js frontend to the FastAPI backend.

- Typed API client in lib/api/client.ts
- Connect upload → analyze → outline → revise → export flow
- NextAuth credentials calling backend /auth/signin and /auth/signup
- Error handling for FastAPI detail responses
- NEXT_PUBLIC_API_BASE_URL environment variable
```

---

## 7. PPT export

```
Implement native PPTX export with python-pptx.

Flow: title slide → agenda → content slides → conclusion
Apply theme styling via theme_layout_service
Return download URL from /exports/pptx/{id}/download
Frontend: ExportPptxButton downloads blob
```

---

## 8. Presentation history

```
Add presentation history.

- Save presentation after generation (outline, notes, persona, theme)
- List presentations per user
- Detail page for saved deck
- Prisma schema optional; JSON fallback for local dev
```

---

## 9. 25+ category expansion

```
Transform SlideGen AI into a premium AI Content Studio with 25 categories.

Categories: Presentations, News Photocards, Breaking News, Event Posters,
Facebook/Instagram/YouTube formats, Political/Educational Posters,
Certificates, ID Cards, Flyers, Brochures, Infographics, Resume,
Invitations, Ad Creatives, Product Promos, NGO Campaigns, Real Estate,
Restaurant Marketing, Podcast Covers.

Shared generation logic via ContentGenerationService and category registry.
Keep existing PPT functionality intact.
```

---

## 10. Universal generator engine

```
Refactor architecture so categories share reusable generation logic.

Backend:
- CategorySpec registry in content/categories.py
- ContentGenerationService with OpenAI layer JSON + fallback
- content_schemas.py Pydantic models

Frontend:
- lib/content-studio/ types, categories, constants, store
- API client: generateContent()
```

---

## 11. Category marketplace

```
Create a Category Marketplace homepage.

Sections:
- Hero with search + prompt input
- Featured categories (Presentations, News, Breaking News, Event Posters, Social, Certificates)
- Browse all 25 categories with icon, title, description
- Netflix-inspired horizontal scrolling
- Premium SaaS UI

Do not add new features — organize marketplace only.
```

---

## 12. Prompt-to-Design

```
Implement Prompt-to-Design Mode.

Backend:
- Intent Classifier (OpenAI + heuristics)
- Detect generator, extract parameters
- Route to ContentGenerationService
- POST /content/classify-intent and /content/prompt-to-design

Frontend:
- Universal AI prompt box
- Show detected category before generation
- Allow confirm or change category
- Low confidence → manual category picker
```

---

## 13. GitHub preparation

```
Prepare SlideGen AI for a clean GitHub update.

- Update README.md, CHANGELOG.md, TODO.md
- Create .env.example files (no real secrets)
- Update .gitignore for node_modules, .next, venv, uploads, exports
- Remove duplicate/dead components
- Exclude runtime JSON data files
- Verify npm run build passes
```

---

## 14. Stabilization

```
Return project to stable working state. Do not add new features.

Keep working:
- Landing page, dashboard, new presentation, category marketplace browse, PPT flow

Disable unfinished features breaking the app:
- Prompt-to-Design API in UI
- Studio editor, brand kit, category AI generation

Fix localhost: clear .next cache, add npm run dev:clean
```

---

## Prompt tips learned from this project

1. End prompts with **“Do not explain. Update files directly.”** for faster iteration.
2. After large changes, prompt: **“Run npm run build and fix any errors.”**
3. When localhost breaks, prompt: **“Verify app is stable — fix only what’s broken.”**
4. Before GitHub push, prompt: **“Prepare for safe commit — list files that must not be committed.”**
