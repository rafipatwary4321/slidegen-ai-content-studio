import type { NewsCategoryId, NewsDesignStyleId, NewsToneId } from "@/lib/news-photocard/types";

export const NEWS_CATEGORIES: { id: NewsCategoryId; label: string }[] = [
  { id: "politics", label: "Politics" },
  { id: "campus", label: "Campus" },
  { id: "sports", label: "Sports" },
  { id: "international", label: "International" },
  { id: "business", label: "Business" },
  { id: "entertainment", label: "Entertainment" }
];

export const NEWS_LANGUAGES = [
  { id: "en" as const, label: "English" },
  { id: "bn" as const, label: "Bengali" }
];

export const NEWS_ASPECT_RATIOS = [
  { id: "1:1" as const, label: "1:1 Square" },
  { id: "4:5" as const, label: "4:5 Portrait" },
  { id: "9:16" as const, label: "9:16 Story" }
];

export const NEWS_TONES: { id: NewsToneId; label: string; description: string }[] = [
  { id: "breaking-news", label: "Breaking News", description: "Urgent alert strip, bold headline" },
  { id: "premium-editorial", label: "Premium Editorial", description: "Magazine layout, refined typography" },
  { id: "youth-media", label: "Youth Media", description: "Dynamic, vibrant social-native style" },
  { id: "corporate-press", label: "Corporate Press", description: "Clean masthead, structured blocks" }
];

export const NEWS_DESIGN_STYLES: { id: NewsDesignStyleId; label: string; swatch: string }[] = [
  { id: "dark-red", label: "Dark Red", swatch: "#b91c1c" },
  { id: "black", label: "Black", swatch: "#0a0a0a" },
  { id: "white", label: "White", swatch: "#f7f7f7" },
  { id: "gold", label: "Gold", swatch: "#d4af37" }
];

export const PREVIEW_PALETTES: Record<
  NewsDesignStyleId,
  { bg: string; surface: string; accent: string; text: string; muted: string; badge: string; gold: string }
> = {
  "dark-red": {
    bg: "#140505",
    surface: "#1f0a0a",
    accent: "#b91c1c",
    text: "#ffffff",
    muted: "#fca5a5",
    badge: "#dc2626",
    gold: "#d4af37"
  },
  black: {
    bg: "#0a0a0a",
    surface: "#141414",
    accent: "#ffffff",
    text: "#f5f5f5",
    muted: "#a3a3a3",
    badge: "#262626",
    gold: "#c9a227"
  },
  white: {
    bg: "#f7f7f7",
    surface: "#ffffff",
    accent: "#111111",
    text: "#111111",
    muted: "#525252",
    badge: "#e5e5e5",
    gold: "#b8860b"
  },
  gold: {
    bg: "#1c1408",
    surface: "#2a1f0c",
    accent: "#d4af37",
    text: "#faf5e6",
    muted: "#e8d5a8",
    badge: "#92700c",
    gold: "#ffd700"
  }
};

export function categoryLabel(id: NewsCategoryId): string {
  return NEWS_CATEGORIES.find((c) => c.id === id)?.label ?? id;
}

export function toneLabel(id: NewsToneId): string {
  return NEWS_TONES.find((t) => t.id === id)?.label ?? id;
}
