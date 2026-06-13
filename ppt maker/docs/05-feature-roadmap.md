# Feature Roadmap

## SlideGen AI Content Studio — phased plan

Current stable release: **v1.1.0** (PPT generator + marketplace browse)

---

## Phase 1 — Core generators (priority)

| Feature | Status | Notes |
|---------|--------|-------|
| **PPT generator** | ✅ Live | Upload → analyze → outline → revise → PPTX |
| **News photocard** | 🔧 Backend ready | UI browse only; generation disabled |
| **Poster generator** | 🔧 Backend ready | Event + political posters in registry |
| **Social media post** | 🔧 Backend ready | Instagram, Facebook formats defined |
| **Certificate generator** | 🔧 Backend ready | Bulk quantity param in intent classifier |

**Phase 1 goal:** Re-enable UI generation for these five categories on the existing `ContentGenerationService`.

---

## Phase 2 — Marketing & professional formats

| Feature | Status |
|---------|--------|
| Flyers | Category defined |
| Infographics | Category defined |
| Resume / CV builder | Category defined |
| Ad creatives | Category defined |
| Invitation cards | Category defined |

**Phase 2 goal:** Template library per category + raster PNG/PDF export.

---

## Phase 3 — Platform & SaaS

| Feature | Status |
|---------|--------|
| Canva-like editor | Scaffold in repo; UI disabled |
| Full marketplace | Browse live; generation TBD |
| Team collaboration | Not started |
| Billing (Stripe) | Not started |
| White-label system | Not started |

**Phase 3 goal:** Production SaaS with multi-tenant workspaces and branded exports.

---

## 25+ content categories (full list)

| # | Category | Phase |
|---|----------|-------|
| 1 | Presentations | 1 ✅ |
| 2 | News Photocards | 1 |
| 3 | Breaking News Cards | 1 |
| 4 | Event Posters | 1 |
| 5 | Facebook Posts | 1 |
| 6 | Instagram Posts | 1 |
| 7 | Instagram Stories | 2 |
| 8 | Facebook Covers | 2 |
| 9 | YouTube Thumbnails | 2 |
| 10 | YouTube Community Posts | 2 |
| 11 | Political Posters | 1 |
| 12 | Educational Posters | 2 |
| 13 | Certificates | 1 |
| 14 | ID Cards | 2 |
| 15 | Flyers | 2 |
| 16 | Brochures | 2 |
| 17 | Infographics | 2 |
| 18 | Resume Builder | 2 |
| 19 | Invitation Cards | 2 |
| 20 | Ad Creatives | 2 |
| 21 | Product Promotions | 2 |
| 22 | NGO Campaign Materials | 2 |
| 23 | Real Estate Templates | 2 |
| 24 | Restaurant Marketing | 2 |
| 25 | Podcast Covers | 2 |

---

## Technical milestones

| Milestone | Target |
|-----------|--------|
| Re-enable Prompt-to-Design UI | Phase 1 |
| Raster PNG/JPG/PDF export | Phase 1 |
| Bulk certificate ZIP | Phase 1 |
| GitHub Actions CI | Phase 2 |
| PostgreSQL production guide | Phase 2 |
| S3 storage | Phase 2 |
| Docker Compose | Phase 3 |

See [TODO.md](../TODO.md) for the active task list.
