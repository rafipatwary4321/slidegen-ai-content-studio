# Project Vision

## SlideGen AI Content Studio

**Repository:** `slidegen-ai-content-studio`

---

## Original idea: AI PPT maker

SlideGen AI began as a focused **AI-powered presentation generator**. The core problem: turning unstructured documents (PDF, DOCX, TXT) into polished slide decks without manual formatting.

The original product promise:

- Upload a document
- Let AI analyze structure and intent
- Generate a slide outline with persona and theme
- Revise with natural-language prompts
- Export a real `.pptx` file

This remains the **production-ready core** of the project today.

---

## Transformation: AI Content Studio

As the product matured, the vision expanded from “PPT only” to a **universal AI content platform** — closer to Canva + Gamma + Adobe Express, but AI-native from the ground up.

The Content Studio layer adds:

- A **category marketplace** with 25+ creative formats
- Shared **generation architecture** for all content types
- **Prompt-to-Design** — describe what you want; AI picks the right generator
- A path toward visual editing, brand kits, and multi-format export

The PPT pipeline is not replaced — it becomes the flagship category (`presentations`) inside a larger studio.

---

## Goal: better than a simple template studio

Template-only tools give users static layouts. SlideGen AI aims higher:

| Template studio | SlideGen AI Content Studio |
|-----------------|---------------------------|
| Pick a template, fill placeholders | Describe intent; AI generates structure and content |
| One format at a time | 25+ categories with shared generation logic |
| Manual export | Automated PPTX, PNG, PDF, ZIP pipelines |
| No document intelligence | Full document analysis for presentations |

The stable release (v1.1.0) delivers the **PPT generator** and **marketplace browsing**. Advanced studio generation and the visual editor are architected but temporarily disabled for stability.

---

## Target users

| Segment | Use case |
|---------|----------|
| **Students** | Turn notes and reports into presentation outlines |
| **Professionals** | Pitch decks, strategy updates, board presentations |
| **Marketers** | Social posts, posters, ad creatives, event materials |
| **Newsrooms** | Photocards, breaking news cards, editorial graphics |
| **Educators** | Classroom posters, certificates, infographics |
| **Small businesses** | Flyers, menus, real estate listings, invitations |
| **Developers / builders** | Reference architecture for AI content SaaS |

---

## North-star experience

1. Land on a clean marketplace
2. Search or describe what to create
3. AI routes to the correct category and generator
4. Preview and refine in a visual editor
5. Export in the right format for the channel

**Today:** steps 1–2 (browse/search) and the full PPT path (upload → analyze → outline → export) are live.

**Next:** re-enable Prompt-to-Design, category generation, and the Canva-like editor on the existing backend architecture.
