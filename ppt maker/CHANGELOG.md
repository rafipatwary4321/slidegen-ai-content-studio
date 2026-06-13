# Changelog

All notable changes to SlideGen AI Content Studio.

## [1.1.1] — 2025-06-14

**Portfolio documentation** — GitHub-ready repository organization.

### Added
- `docs/` folder with six portfolio documents (vision, architecture, dev process, Cursor prompts, roadmap, GitHub process)
- README rewritten for `slidegen-ai-content-studio` portfolio presentation
- `.gitignore` updated with `dist/` and `build/`

### Unchanged
- Application code and stable v1.1.0 feature set — no new app features

## [1.1.0] — 2025-06-14

**Stable milestone** — core app verified for local dev and GitHub commit.

### Working
- Landing page, category marketplace (search, featured, browse all 25 categories)
- PPT generator: upload → analyze → outline → revise → export PPTX
- Presentation history (auth required)
- `npm run dev:clean` to avoid corrupted `.next` cache
- Build and lint pass

### Stabilized
- Disabled unfinished studio generation, editor, and brand kit in UI
- Marketplace uses local category search (no Prompt-to-Design API dependency)
- Auth middleware limited to history and saved presentations only
- PPT generate/export works without sign-in; save requires account

### Repository
- `.gitignore` covers env files, deps, uploads, exports, runtime JSON
- `.env.example` templates with no real secrets

## [1.0.0] — 2025-06-14

Initial scaffold: Content Studio architecture, 25 categories, backend content API, PPT pipeline, NextAuth.

## [Unreleased]

See [TODO.md](./TODO.md).
