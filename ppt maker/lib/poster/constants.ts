import type { PosterDesignToneId, PosterTypeId } from "@/lib/poster/types";

export const POSTER_TYPES: { id: PosterTypeId; label: string }[] = [
  { id: "event", label: "Event Poster" },
  { id: "political", label: "Political Poster" },
  { id: "educational", label: "Educational Poster" },
  { id: "business", label: "Business Poster" },
  { id: "awareness", label: "Awareness Campaign" },
  { id: "product", label: "Product Promotion" }
];

export const POSTER_LANGUAGES = [
  { id: "en" as const, label: "English" },
  { id: "bn" as const, label: "Bengali" }
];

export const POSTER_ASPECT_RATIOS = [
  { id: "1:1" as const, label: "1:1 Square" },
  { id: "4:5" as const, label: "4:5 Portrait" },
  { id: "9:16" as const, label: "9:16 Story" },
  { id: "A4" as const, label: "A4 Print" }
];

export const POSTER_DESIGN_TONES: { id: PosterDesignToneId; label: string; description: string }[] = [
  { id: "premium-corporate", label: "Premium Corporate", description: "Navy, clean hierarchy, refined CTA" },
  { id: "bold-political", label: "Bold Political", description: "High contrast, rally energy" },
  { id: "modern-youth", label: "Modern Youth", description: "Vibrant gradients, dynamic layout" },
  { id: "academic-clean", label: "Academic Clean", description: "Structured, readable, minimal" },
  { id: "luxury-event", label: "Luxury Event", description: "Gold accents, elegant event styling" }
];

export const TONE_PALETTES: Record<
  PosterDesignToneId,
  { bg: string; surface: string; accent: string; text: string; muted: string; cta: string }
> = {
  "premium-corporate": {
    bg: "#0f172a",
    surface: "#1e293b",
    accent: "#38bdf8",
    text: "#f8fafc",
    muted: "#94a3b8",
    cta: "#0ea5e9"
  },
  "bold-political": {
    bg: "#1a0505",
    surface: "#2d0a0a",
    accent: "#dc2626",
    text: "#ffffff",
    muted: "#fca5a5",
    cta: "#b91c1c"
  },
  "modern-youth": {
    bg: "#1e1033",
    surface: "#2d1b4e",
    accent: "#a855f7",
    text: "#faf5ff",
    muted: "#d8b4fe",
    cta: "#ec4899"
  },
  "academic-clean": {
    bg: "#f8fafc",
    surface: "#ffffff",
    accent: "#1d4ed8",
    text: "#0f172a",
    muted: "#475569",
    cta: "#2563eb"
  },
  "luxury-event": {
    bg: "#1c1408",
    surface: "#2a1f0c",
    accent: "#d4af37",
    text: "#faf5e6",
    muted: "#e8d5a8",
    cta: "#b8860b"
  }
};

export function posterTypeLabel(id: PosterTypeId): string {
  return POSTER_TYPES.find((t) => t.id === id)?.label ?? id;
}

export function designToneLabel(id: PosterDesignToneId): string {
  return POSTER_DESIGN_TONES.find((t) => t.id === id)?.label ?? id;
}

/** Maps marketplace category IDs to poster form type */
export const CATEGORY_TO_POSTER_TYPE: Record<string, PosterTypeId> = {
  "event-posters": "event",
  "political-posters": "political",
  "educational-posters": "educational",
  "flyers": "business",
  "ngo-campaign-materials": "awareness",
  "product-promotions": "product"
};
