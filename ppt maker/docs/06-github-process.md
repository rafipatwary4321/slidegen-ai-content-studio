# GitHub Process

## Repository

| Item | Value |
|------|-------|
| **Name** | `slidegen-ai-content-studio` |
| **Visibility** | Public (portfolio) or Private |
| **Default branch** | `main` |

---

## First-time setup

Run these commands **inside the project folder** (`ppt maker/`), not the parent `Cursor/` directory.

```bash
cd "path/to/ppt maker"

# 1. Initialize repository (only once)
git init

# 2. Verify secrets are NOT tracked
git status
# Confirm .env.local does NOT appear

# 3. Stage all files
git add .

# 4. First commit
git commit -m "feat: stable v1.1.0 — SlideGen AI Content Studio portfolio release"

# 5. Create GitHub repo at github.com/new
#    Name: slidegen-ai-content-studio

# 6. Connect remote
git remote add origin https://github.com/YOUR_USERNAME/slidegen-ai-content-studio.git

# 7. Set main branch and push
git branch -M main
git push -u origin main
```

---

## Pre-commit checklist

```bash
npm run build          # must pass
npm run lint           # no errors
git status             # review staged files
```

**Never commit:**

- `.env.local` / `backend/.env`
- `node_modules/`, `.next/`, `backend/.venv/`
- `backend/data/*.json`
- `backend/storage/`, `backend/output/`

**Safe to commit:**

- `.env.example`, `backend/.env.example`
- All source code, `docs/`, `README.md`, `CHANGELOG.md`, `TODO.md`

---

## Future update workflow

After making changes locally:

```bash
# 1. Check what changed
git status
git diff

# 2. Stage changes
git add .

# 3. Commit with a clear message
git commit -m "fix: describe what changed and why"

# 4. Push to GitHub
git push
```

### Commit message format

```
type: short description

Types: feat | fix | docs | chore | refactor | test
```

Examples:

```
feat: re-enable Prompt-to-Design in marketplace hero
fix: resolve PPTX export download on Windows
docs: update architecture diagram for export pipeline
chore: add GitHub Actions CI workflow
```

---

## Branch strategy (recommended)

| Branch | Purpose |
|--------|---------|
| `main` | Stable, deployable |
| `develop` | Integration branch for features |
| `feature/*` | Individual features |

For portfolio simplicity, committing directly to `main` is acceptable during early development.

---

## GitHub repository settings

1. **About section:** Add description + link to live demo (if deployed)
2. **Topics:** `nextjs`, `fastapi`, `openai`, `ppt-generator`, `ai-content-studio`, `cursor-ai`
3. **README:** Auto-displayed from root `README.md`
4. **Secrets:** Add `OPENAI_API_KEY`, `NEXTAUTH_SECRET` only in GitHub Actions secrets — never in code

---

## Portfolio presentation tips

This repo is designed as a **development portfolio**. Highlight in your README or GitHub About:

- Full-stack Next.js + FastAPI architecture
- Real OpenAI integration with fallbacks
- 25-category Content Studio design
- Cursor AI-assisted development process (`docs/04-cursor-prompts.md`)
- Stable-before-feature engineering discipline

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Black screen on localhost | `npm run dev:clean` |
| `.env.local` in `git status` | Check `.gitignore`; run `git rm --cached .env.local` |
| Pushed secrets by accident | Rotate keys immediately; use `git filter-repo` or BFG |
| Parent repo tracks wrong folder | `git init` inside `ppt maker/` only |
