/**
 * Shared API contract between Next.js frontend and FastAPI backend.
 * Keep paths in sync with backend/app/main.py route prefixes.
 */
export const API_V1 = "/api/v1" as const;

export const API_ROUTES = {
  health: "/health",
  auth: {
    signup: `${API_V1}/auth/signup`,
    signin: `${API_V1}/auth/signin`
  },
  upload: `${API_V1}/upload`,
  documents: {
    analyze: `${API_V1}/documents/analyze`
  },
  outlines: {
    generate: `${API_V1}/outlines/generate`,
    revise: `${API_V1}/outlines/revise`
  },
  notes: {
    generate: `${API_V1}/notes/generate`
  },
  exports: {
    pptx: `${API_V1}/exports/pptx`,
    download: (exportId: string) => `${API_V1}/exports/pptx/${exportId}/download`
  },
  presentations: {
    list: `${API_V1}/presentations`,
    one: (id: string) => `${API_V1}/presentations/${id}`,
    regenerate: (id: string) => `${API_V1}/presentations/${id}/regenerate`
  },
  content: {
    classifyIntent: `${API_V1}/content/classify-intent`,
    promptToDesign: `${API_V1}/content/prompt-to-design`,
    generate: `${API_V1}/content/generate`,
    export: `${API_V1}/content/export`
  }
} as const;

export type ApiRouteKey = keyof typeof API_ROUTES;
