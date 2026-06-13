# TODO

> Roadmap phases: [docs/05-feature-roadmap.md](./docs/05-feature-roadmap.md)  
> GitHub workflow: [docs/06-github-process.md](./docs/06-github-process.md)

## Unfinished (disabled in stable UI)

- [ ] Re-enable Prompt-to-Design (`/content/classify-intent`, `/content/prompt-to-design`)
- [ ] Re-enable category AI generation (`/content/generate`)
- [ ] Re-enable Canva-like studio editor
- [ ] Re-enable brand kit page
- [ ] Raster export — PNG/JPG/PDF from canvas layers
- [ ] Bulk certificate ZIP generation
- [ ] Expand per-category template library

## Medium priority

- [ ] S3 storage implementation
- [ ] Async export workers (`EXPORT_ASYNC`)
- [ ] PostgreSQL production migration guide
- [ ] E2E tests (marketplace + PPT flows)
- [ ] API tests for content studio routes
- [ ] GitHub Actions CI (`npm run build` + backend import check)

## Low priority

- [ ] Full-width editor layout
- [ ] UI i18n
- [ ] Rate limiting on AI endpoints
- [ ] Docker Compose dev stack

## Completed (stable milestone)

- [x] Landing page
- [x] Category marketplace (browse + search)
- [x] PPT generator basic flow
- [x] Presentation history
- [x] `npm run dev:clean` for reliable localhost
- [x] GitHub-ready `.gitignore`, `.env.example`
- [x] Portfolio `docs/` folder (vision, architecture, prompts, roadmap, GitHub process)
- [x] Build + lint verified
